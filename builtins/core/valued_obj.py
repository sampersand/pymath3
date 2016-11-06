from . import logger
from .operable import Operable

class ValuedObj(Operable):
	''' Represents an object that can have a value.

	This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
	warning will be logged.

	See Constant and Variable for builtin subclasses for this.
	'''

	_DEFAULT_VALUE = None
	_ALLOWED_VALUE_TYPES = (int, float, bool, complex, type(None))

	def __init__(self, *args, value = None, **kwargs):
		''' Initializes self with 'value'
		
		This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
		warning will be logged.

		Arguments:
			*args    -- Ignored
			value    -- The value of this class. (default: None)
			**kwargs -- Ignored
		Returns:
			None
		'''

		__class__.checktype(self)

		if value is None:
			value = self._DEFAULT_VALUE
		self.value = value
		super().__init__(*args, **kwargs)


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

	def _gen_repr(self, args, kwargs):
		assert 'value' not in kwargs, kwargs
		if self.hasvalue():
			kwargs['value'] = repr(self.value)
		return super()._gen_repr(args, kwargs)

__all__ = ('ValuedObj', )



