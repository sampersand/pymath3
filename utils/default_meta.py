from . import logger, from_stack
from collections import OrderedDict
class _WrappedObject():
	def __init__(self, parent):
		self._parent = parent
	def __getattribute__(self, attr):
		parent = super().__getattribute__('_parent')
		return super(type(parent), parent).__getattribute__(attr)

class _AttrDict(dict):
	def __init__(self, *args, **kwargs):
		super().__init__(*args, **kwargs)

	@property
	def __self__(self):
		return _WrappedObject(self)

	@staticmethod
	def __set_name__(caller, name):
		pass

	def __getattribute__(self, attr):
		if attr in self:
			assert attr != '__self__'
			return self[attr]
		return super().__getattribute__(attr)

class _PreparedDict(OrderedDict):
	@staticmethod
	def process_new_defaults(new):
		return new
	def __setitem__(self, name, value):
		if name == '__defaults__' and '__defaults__' in self:
			if __debug__ and not isinstance(value, dict):
				logger.warning("Recieved non-dict type for __defaults__: {}".format(type(value)))
			self['__defaults__'].__self__.update(self.process_new_defaults(value))
		else:
			super().__setitem__(name, value)

class DefaultMeta(type):
	_defaults_dict = _AttrDict
	_prepared_dict = _PreparedDict

	__meta_defaults__ = _AttrDict()

	@classmethod
	def _get_defaults(metacls, bases):
		defaults = metacls._defaults_dict()

		assert isinstance(bases, tuple)
		assert isinstance(metacls, type)
		assert isinstance(defaults, dict)

		for base in bases:
			if hasattr(base, '__defaults__'):
				if __debug__ and not isinstance(base.__defaults__, dict):
					logger.warning("Class {}'s __defaults__ (type: {}) is not an instance of dict".format(
						base.__qualname__, type(base.__defaults__).__qualname__))
				assert isinstance(base.__defaults__, dict)
				defaults.update(base.__defaults__)
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


class NestedDefaultMeta(DefaultMeta):
	def _default_repr__(self):
		non_default_values = {}
		assert '__init__' in dir(self)
		for name, default_value in self.__defaults__.__init__.items():
			assert hasattr(self, name)
			self_value = getattr(self, name)
			if self_value is not default_value:
				non_default_values[name] = self_value
		return '{}({})'.format(type(self).__qualname__,
			', '.join('{}={!r}'.format(name, value) for name, value in non_default_values.items()))


	class _NestedPreparedDict(_PreparedDict):
		@classmethod
		def flatten(cls, e):
			return e if not isinstance(e, dict) else _AttrDict({k : cls.flatten(v) for k, v in e.items()})
		# @staticmethod
		@classmethod
		def process_new_defaults(cls, new):
			return cls.flatten(new)


	_prepared_dict = _NestedPreparedDict

	__meta_defaults__ = _AttrDict({
		'__repr__' : _default_repr__,
	})

class foo(metaclass=NestedDefaultMeta):
	__defaults__ = {
		'__init__': {
			'a': 1,
			'b': 2
			},
		'__call__': {
			'arg1': 3
		},
		'__str__': {
		'a': 1
		}
	}
	def __init__(self, a = __defaults__.__init__.a):
		self.a = a
	# __defaults__ = {'a': 9}
class bar(foo):
	def __init__(self, a = __defaults__.a, b = __defaults__.b):
		super().__init__()
		self.b = b
	__repr__ = __meta_defaults__['__repr__']
b = bar()
print(b.__defaults__)
print(repr(b))









quit()