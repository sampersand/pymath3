from . import logger
from .operable import Operable

class ValuedObj(Operable):
	''' Represents an object that can have a value.

	This class is meant to be subclassed, and shouldn't be instanced directly.

	See Constant and Variable for builtin subclasses for this.
	
	A warning will be logged if a ValuedObj is attempted to be instanced directly.
	'''

	_default_value = None
	_allowed_value_types = (int, float, bool, complex, type(None))

	def __init__(self, *args, value = _default_value, **kwargs):
		''' Initializes self with 'value'
		
		A warning will be logged if a ValuedObj is attempted to be instanced directly.

		Arguments:
			*args    -- Ignored
			value    -- The value of this class. (default: None)
			**kwargs -- Ignored
		Returns:
			None
		'''

		if __debug__ and type(self) == ValuedObj:
			logger.warning("Should not instantiate {} directly!".format(type(self).__qualname__))

		super().__init__(*args, **kwargs)

		if value is None:
			value = self._default_value
		self.value = value


	value = property(doc = "The resulting value of this class")

	@value.getter
	def value(self):
		return self._value

	@value.setter
	def value(self, newvalue):
		if not isinstance(newvalue, self._allowed_value_types):
			logger.warning("Attempted to set value to unknown type '{}'. Allowed types: {}".format(
				type(newvalue).__qualname__,
				', '.join('%r' % x.__qualname__ for x in self._allowed_value_types)))
		self._value = newvalue

	@value.deleter
	def value(self):
		self._value = self._default_value

	def hasvalue(self):
		''' Return true if this this class has a value. '''
		return self.value != self._default_value

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
	def __repr__(self):
		if self.hasvalue():
			return '{}(value={!r})'.format(type(self).__qualname__, self.value)
		assert not self.hasvalue()
		return super().__repr__()

__all__ = ('ValuedObj', )



