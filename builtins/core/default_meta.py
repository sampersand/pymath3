import collections
# from . import logger


class _stand_in_for_attr():
	def __init__(self, attr_name):
		self.attr_name = attr_name

	def __get__(self, instance, parent):
		if instance == None:
			logger.warning('Trying to get the standin attr {} without an instance!'.format(self.attr_name))
		return instance[self.attr_name]

	def __call__(self, *args, **kwargs):
		#idk why this is being called.....
		return self

	def __repr__(self):
		return '<standin for {}>'.format(self.attr_name)

class defaults_dict(dict):
	def __init__(self):
		super().__init__()
		super().__setattr__('_islocked', False)
		super().__setattr__('_standins', {})

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
			logger.warning("Attribtue {} doesn't have a default value")
				#can't specify class type because that would require an argument in the constructor
		assert attr in self
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
	def _create_defaults(self):
		for ele_name in dir(self):
			assert hasattr(self, ele_name)
			if ele_name.startswith('DEFAULT_'):
				self.defaults[ele_name[len('DEFAULT_'):].lower()] = getattr(self, ele_name)
				delattr(self, ele_name)

	def _update_defaults(self, bases):
		for base in bases:
			if hasattr(base, 'defaults'):
				assert isinstance(bases.defaults, defaults_dict)				
				cls.defaults.update(bases.defaults)

	@staticmethod
	def _static_isdefault(self, name, attr = None):
		if __debug__:
			if isinstance(self, type):
				logger.warning("Class instances, rather than class objects, should be passed.")
			if not hasattr(self, 'defaults'):
				logger.warning("{} doesn't have the required attribute 'defaults'.".format(type(self)))

		assert isinstance(self.defaults, defaults_dict)

		if attr == None:
			attr = type(self)._getattr(self, name)

		return attr is self.defaults[name]

	@staticmethod
	def _getattr(meta_inst_inst, name):
		return getattr(meta_inst_inst, name)

class UnderscoreDefaultMeta(DefaultMeta):
	@staticmethod
	def _getattr(meta_inst_inst, name):
		return getattr(meta_inst_inst, '_' + name)
