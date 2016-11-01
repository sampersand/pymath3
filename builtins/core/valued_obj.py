from . import logger
from .operable import Operable

class ValuedObj(Operable):
	''' Represents an object that can have a value.

	This class is meant to be subclassed, and shouldn't be instanced directly.

	See Constant and Variable for builtin subclasses for this.
	
	If attempting to directly instantiate a ValuedObj, a warning will be logged.
	'''

	_default_value = None
	_allowed_types = (int, float, bool, complex, type(None))

	def __init__(self, *args, value = _default_value, **kwargs):
		''' Initializes self with 'value'
		
		If attempting to directly instantiate a ValuedObj, a warning will be logged.

		Arguments:
			value    -- The value of this class. (default: None)
			**kwargs -- Extra kwargs, will be ignored for this class.
		'''

		if __debug__ and type(self) == ValuedObj:
			logger.warning("Should not instantiate {} directly!".format(type(self).__qualname__))

		super().__init__(*args, **kwargs)
		self.value = value


	value = property(doc = "The resulting value of this class")

	@value.getter
	def value(self):
		return self._value

	@value.setter
	def value(self, newvalue):
		if not isinstance(newvalue, self._allowed_types):
			logger.warning("Attempted to set value to unknown type '{}'. Allowed types: {}".format(
				type(newvalue).__qualname__,
				', '.join('%r' % x.__qualname__ for x in self._allowed_types)))
		self._value = newvalue

	@value.deleter
	def value(self):
		self._value = self._default_value

	def isknown(self):
		''' Return true if this this class has a value. '''
		return self.value != self._default_value

	def __str__(self):
		''' Returns a string representation of this class.

		Returns:
			str(self.value)   -- If 'self.isknown()' evaluates to True
			super().__str__() -- If 'self.isknown()' doesn't evaluate to True
		'''
		if self.isknown():
			return str(self.value)

		assert not self.isknown()

		return super().__str__()


__all__ = ('ValuedObj', )



