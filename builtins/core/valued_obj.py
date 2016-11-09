from . import logger, Derivable
from .operable import Operable
from copy import deepcopy
class ValuedObj(Operable, Derivable):
	''' Represents an object that can have a value.

	This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
	warning will be logged.

	See Constant and Variable for builtin subclasses for this.
	'''

	_DEFAULT_VALUE = None
	_ALLOWED_VALUE_TYPES = (int, float, bool, complex, type(None))

	def __init__(self, *args, value = None, **kwgs):
		''' Initializes self with 'value'
		
		This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
		warning will be logged.

		Arguments:
			*args    -- Ignored
			value    -- The value of this class. (default: None)
			**kwgs -- Ignored
		Returns:
			None
		'''

		__class__.checktype(self)

		if value is None:
			value = self._DEFAULT_VALUE
		self.value = value
		super().__init__(*args, **kwgs)


	value = property(doc = "The resulting value of this class")

	@value.getter
	def value(self):
		return self._value

	@value.setter
	def value(self, newvalue):
		if not isinstance(newvalue, self._ALLOWED_VALUE_TYPES):
			logger.warning("Attempted to set value to unknown type '{}'. Allowed types: {}".format(
				type(newvalue).__qualname__,
				', '.join('%r' % x.__qualname__ for x in self._ALLOWED_VALUE_TYPES)))
		self._value = newvalue

	@value.deleter
	def value(self):
		self._value = self._DEFAULT_VALUE


	@property
	def solid_value(self):
		return deepcopy(self.value)

	def hasvalue(self):
		''' Return true if this this class has a value. '''
		return self.value != self._DEFAULT_VALUE

	def __str__(self):
		''' Returns a string representation of this class.

		Returns:
			str(self.value)   -- If 'self.hasvalue()' evaluates to True
			super().__str__() -- If 'self.hasvalue()' doesn't evaluate to True
		'''

		if self.hasvalue():
			return str(self.value)

		assert not self.hasvalue()

		return super().__str__()

	def _gen_repr(self, args, kwgs):
		assert 'value' not in kwgs, kwgs
		if self.hasvalue():
			kwgs['value'] = repr(self.value)
		return (args, kwgs)

	def isconst(self, du):
		assert self is not du
		return self.hasvalue()

	# def __eq__(self, other):
	# 	if self is other:
	# 		return True

	# 	if hasattr(other, 'hasvalue'):
	# 		if self.hasvalue() ^ other.hasvalue():
	# 			return False

	# 	if not hasattr(other, 'value'):
	# 		return False

	# 	return self.value == other.value


	def __derive__(self, du):
		return int(not self.isconst(du))


__all__ = ('ValuedObj', )















