from . import logger, from_stack, convert as formal_convert, auto, immutable
from collections import OrderedDict, Iterable


class _WrappedObject():
	def __init__(self, parent, *args, **kwargs):
		super().__init__(*args, **kwargs)
		super().__setattr__('_parent', parent)
	@property
	def locked(self):
		return hasattr(self, '_parent')
	def __getattribute__(self, attr):
		parent = super().__getattribute__('_parent')
		if attr == '_parent':
			return parent
		return super(type(parent), parent).__getattribute__(attr)

class _DefaultDict(immutable, dict, lock=False):
	# def __init__(self, inp_dict = None, *args, **kwargs):
	# 	super().__init__(inp_dict, *args, **kwargs)
	# 	dict.__init__(self, inp_dict)

	@property
	def __self__(self):
		return _WrappedObject(self)

	@staticmethod
	def __set_name__(caller, name):
		pass

	def __contains__(self, attr):
		return super().__contains__(attr)

	def __getattribute__(self, attr):
		if attr in self:
			assert attr != '__self__'
			return self[attr]
		return super().__getattribute__(attr)
	
	def update(self, d):
		self.assert_unlocked()
		_PreparedDict.verify_default_dict_attrs(d)
		for name in d:
			if name in dict(self):
				logger.info('{} (prev={}) is being overriden with {}'.format(name, d[name], self[name]))
		super().update(d)
class _PreparedDict(OrderedDict):
	REQUIRED_ATTRS_FOR_NEW_DEFAULTS = ('__iter__', '__getitem__', '__setitem__')
	@staticmethod
	def verify_default_dict_attrs(inp):
		for req_attr in _PreparedDict.REQUIRED_ATTRS_FOR_NEW_DEFAULTS:
			if not hasattr(inp, req_attr):
				raise TypeError("Missing attribute '{}' in '{}'".format(req_attr, type(inp).__qualname__))
		return True

	@staticmethod
	def process_new_defaults(new):
		return new

	def __setitem__(self, name, value):
		assert isinstance(name, str)
		if name == '__defaults__':
			self.verify_default_dict_attrs(value)

		if name == '__class_defaults__' and '__defaults__' in self:
			if not isinstance(value, dict):
				logger.info("Recieved non-dict type for __defaults__: {}".format(type(value)))
			self['__defaults__'].__self__.update(self.process_new_defaults(value))
		super().__setitem__(name, value)

	def __delitem__(self, value):
		assert isinstance(value, str)
		if value == '__defaults__':
			logger.error('NameError: Cannot delete __defaults__ attribute; this is being surpressed!')
			raise NameError('Cannot delete __defaults__ attribute')
		else:
			super().__delitem__(value)

class DefaultMeta(type):
	_defaults_dict = _DefaultDict
	_prepared_dict = _PreparedDict

	__meta_defaults__ = _DefaultDict()

	@classmethod
	def _get_defaults(metacls, bases):
		defaults = metacls._defaults_dict()

		assert isinstance(bases, tuple)
		assert isinstance(metacls, type)
		assert isinstance(defaults, dict)

		for base in reversed(bases): #reversed so the furthest away in the MRO is overriden
			if hasattr(base, '__defaults__'):
				if not isinstance(base.__defaults__, dict):
					logger.warning("Class {}'s __defaults__ (type: {}) is not an instance of dict".format(
						base.__qualname__, type(base.__defaults__).__qualname__))
				assert isinstance(base.__defaults__, dict)
				defaults.__self__.update(base.__defaults__)
		assert not defaults.locked
		return defaults

	@classmethod
	def __prepare__(metacls, name, bases, **kwargs):
		super_prepare = super().__prepare__(metacls, name, bases, **kwargs)
		prepared = metacls._prepared_dict(super_prepare)

		assert isinstance(prepared, dict)
		assert '__defaults__' not in prepared # this will be generated

		prepared['__defaults__'] = metacls._get_defaults(bases)
		prepared['__meta_defaults__'] = metacls.__meta_defaults__
		return prepared
	def __init__(cls, name, bases, attrs, **kwargs):
		super().__init__(name, bases, attrs, **kwargs)

		assert not cls.__defaults__.locked
		cls.__defaults__.acquire()
		assert cls.__defaults__.locked
	
	def __setattr__(self, attr, value):
		self.assert_unlocked()
		super().__setattr__(attr, value)

class NestedDefaultMeta(DefaultMeta):
	def _default_repr__(self, converter = None):
		assert hasattr(self, '__defaults__')
		assert hasattr(self, '__meta_defaults__')
		if converter is None:
			if '__converter__' in self.__defaults__:
				converter = self.__defaults__['__converter__']
			else:
				converter = self.__meta_defaults__['__converter__']

		assert callable(converter)

		non_default_values = {}
		if '__init__' not in self.__defaults__:
			raise AttributeError('No __init__ in self - cannot construct a default repr!')

		assert '__init__' in self.__defaults__

		for attr_name, default_value in self.__defaults__['__init__'].items():
			attr_name = converter(attr_name)
			if not hasattr(self, attr_name):
				raise AttributeError("Class {} defines {} in __init__ default, but doesn't have the attribute".format(type(self).__qualname__, attr_name))
			assert hasattr(self, attr_name)
			self_value = getattr(self, attr_name)
			if self_value is not default_value:
				non_default_values[attr_name] = self_value
		return '{}({})'.format(type(self).__qualname__,
			', '.join('{}={!r}'.format(attr_name, value) for attr_name, value in non_default_values.items()))

	def convert(func = None, *, defaults = None):
		if defaults is None:
			defaults = from_stack('__defaults__', 2)
		if func is None:
			assert defaults is not None
			return lambda func: formal_convert(defaults = defaults, func = func)
		return convert(func = func, defaults = defaults)

	class _NestedPreparedDict(_PreparedDict):
		@classmethod
		def flatten(cls, e):
			return e if not isinstance(e, dict) else _DefaultDict({k : cls.flatten(v) for k, v in e.items()})
		# @staticmethod
		@classmethod
		def process_new_defaults(cls, new):
			return cls.flatten(new)
	class _NestedAttrDict(_DefaultDict):
		def update(self, values):
			for key, value in values.items():
				if key in self and hasattr(self[key], 'update'):
					self[key].update(value)
				else:
					self[key] = value
	_defaults_dict = _NestedAttrDict
	_prepared_dict = _NestedPreparedDict

	__meta_defaults__ = _DefaultDict({
		'__repr__' : _default_repr__,
		'auto': auto,
		'convert': convert,
		'__converter__': lambda attrname: attrname
	})
	__meta_defaults__.update(DefaultMeta.__meta_defaults__)


__all__ = ('DefaultMeta', 'NestedDefaultMeta')






