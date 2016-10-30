import collections
from . import logger


class defaults_dict(dict):
	__slots__ = ('_islocked', )
	def __init__(self):
		super().__init__()
		super().__setattr__('_islocked', False)

	def acquire(self):
		if __debug__ and self.locked():
			logger.warning('Trying to lock a locked defaults_dict!')
		assert not self.locked()
		super().__setattr__('_islocked', True)

	def locked(self):
		assert hasattr(self, '_islocked')
		return self._islocked

	def __getattr__(self, attr):

		if __debug__ and attr not in self:
			logger.warning("Attribtue {} doesn't have a default value".format(attr))
				#can't specify class type because that would require an argument in the constructor
		assert attr in self, attr
		return self[attr]

	def __setattr__(self, attr, value):
		self[attr] = value

	def __setitem__(self, item, value):
		if not self.locked():
			return super().__setitem__(item, value)
		raise AttributeError('readonly attribute')

	def __delattr__(self, item):
		del self[item]

	def __delitem__(self, attr):
		if not self.locked():
			return super().__delattr__(attr)
		raise AttributeError('readonly attribute')

class DefaultMeta(type):
	@classmethod
	def __prepare__(metacls, name, bases, **kwargs):
		return collections.OrderedDict({'defaults': defaults_dict()})

	def __init__(cls, name, bases, attributes):
		type.__init__(cls, name, bases, attributes)
		assert hasattr(cls, 'defaults')
		assert isinstance(cls.defaults, defaults_dict)

		cls._create_defaults()
		cls._update_defaults(bases)

		cls.defaults.acquire()

		cls.isdefault = cls._static_isdefault
		cls.set_values = cls._static_set_values

	def _create_defaults(cls):
		for ele_name in dir(cls):
			assert hasattr(cls, ele_name)
			if ele_name.startswith('DEFAULT_'):
				assert ele_name in dir(cls)
				cls.defaults[ele_name[len('DEFAULT_'):].lower()] = getattr(cls, ele_name)
				assert ele_name in dir(cls)
				assert hasattr(cls, ele_name)
				# delattr(cls, ele_name)

	def _update_defaults(cls, bases):
		for base in bases:
			if hasattr(base, 'defaults'):
				assert isinstance(base.defaults, defaults_dict)				
				cls.defaults.update(base.defaults)

	@staticmethod
	def _static_isdefault(self, name, attr = None):
		cls = type(self)
		if __debug__:
			if isinstance(self, type):
				logger.warning("Class instances, rather than class objects, should be passed.")
			if not hasattr(self, 'defaults'):
				logger.warning("{} doesn't have the required attribute 'defaults'.".format(type(self)))

		assert isinstance(self.defaults, defaults_dict)

		if attr == None:
			attr = cls._get_name(name)

		return attr is self.defaults[name]


	@staticmethod
	def _get_name(name):
		return name
	@staticmethod
	def _static_set_values(self, **kwargs):
		cls = type(self)
		for name, attr in kwargs.items():
			if attr is None:
				if __debug__ and name not in self.defaults:
					logger.warning("Passed argument '{}' is None, but has no default value defined!".
						format(name))
				assert name in self.defaults, name
				attr = getattr(self.defaults, name)
			setattr(self, cls._get_name(name), attr)

class DefaultUnderscoredMeta(DefaultMeta):
	__slots__ = ()

	@staticmethod
	def _get_name(name):
		return '_' + name
	



