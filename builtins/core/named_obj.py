from . import logger
from .math_obj import MathObj
class NamedObj(MathObj):
	''' Represents an object that can have a name.

	This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
	warning will be logged.
	'''

	_DEFAULT_NAME = None
	_ALLOWED_NAME_TYPES = (str, bytes, type(None))

	def __init__(self, *args, name = None, **kwargs):
		'''Initialize self.

		This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
		warning will be logged.

		Arguments:
			*args    -- Ignored
			name     -- The name of this class. (default: None)
			**kwargs -- Ignored
		Returns:
			None
		'''

		__class__.checktype(self)
		if name is None:
			name = self._DEFAULT_NAME
		self.name = name
		super().__init__(*args, **kwargs)


	name = property(doc = "The name of this class")

	@name.getter
	def name(self):
		return self._name

	@name.setter
	def name(self, newname):
		if hasattr(self, '_name'):
			logger.info('Overriding name {} with {}'.format(self.name, newname))
		if not isinstance(newname, self._ALLOWED_NAME_TYPES):
			logger.warning("Name is unknown type '{}'. Allowed types: {}".format(
				type(newname).__qualname__,
				', '.join('%r' % x.__qualname__ for x in self._ALLOWED_NAME_TYPES)))
		self._name = newname

	def hasname(self):
		''' Return true if this this class has a name. '''
		return self.name != self._DEFAULT_NAME

	def __str__(self):
		''' Returns a string representation of this class.

		Returns:
			str(self.name)    -- If 'self.hasname()' evaluates to True
			super().__str__() -- If 'self.hasname()' doesn't evaluate to True
		'''
		if self.hasname():
			return str(self.name)

		assert __debug__ or not self.hasname()

		return super().__str__()


	def _gen_repr(self, args, kwargs):
		assert 'name' not in kwargs, kwargs
		if self.hasname():
			kwargs['name'] = repr(self.name)
		return (args, kwargs)

	# def __eq__(self, other):
	# 	if self is other:
	# 		return True
	# 	if hasattr(other, 'hasname'):
	# 		if self.hasname() ^ other.hasname():
	# 			return False
	# 	if not hasattr(other, 'name'):
	# 		return False
	# 	return self.name == other.name



__all__ = ('NamedObj', )








