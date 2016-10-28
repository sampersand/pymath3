from typing import Union, Any, Generic, TypeVar

from . import logger
from .operable import Operable

T = TypeVar('T')

class ValuedObj(Operable):#, Generic[T]):
	''' Represents an object that can have a value.

	This class is meant to be subclassed, and shouldn't be instanced directly.

	See Constant and Variable for builtin subclasses for this.
	
	If attempting to directly instantiate a ValuedObj, a warning will be logged.
	'''

	DEFAULT_VALUE = None

	def __init__(self, value: Union[T, type(DEFAULT_VALUE)] = DEFAULT_VALUE, **kwargs: Any) -> None:
		''' Initializes self with 'value'
		
		If attempting to directly instantiate a ValuedObj, a warning will be logged.

		Arguments:
			value    -- The value of this class. (default: ValuedObj.DEFAULT_VALUE)
			**kwargs -- Extra kwargs, will be ignored for this class.
		'''

		if __debug__:
			if type(self) == ValuedObj:
				logger.warning("Should not instantiate {} directly!".format(type(self).__qualname__))
		self.value = value

		super().__init__(**kwargs)


	value = property(doc = "The resulting value of this class")

	@value.getter
	def value(self) -> Union[T, type(DEFAULT_VALUE)]:
		return self._value

	@value.setter
	def value(self, val: T) -> None:
		self._value = val

	@value.deleter
	def value(self) -> None:
		self._value = self.DEFAULT_VALUE

	def isknown(self) -> bool:
		''' Return true if this this class has a value. '''
		return self.value != self.DEFAULT_VALUE

	def __str__(self) -> str:
		''' Returns a string representation of this class.

		Returns:
			str(self.value)   -- If 'self.isknown()' evaluates to True
			super().__str__() -- If 'self.isknown()' doesn't evaluate to True
		'''
		if self.isknown():
			return str(self.value)
		if __debug__:
			assert not self.isknown()
		return super().__str__()

	def __repr__(self) -> str:
		''' Returns the string defined by gen_repr with the kwarg 'value'. '''
		return self.gen_repr(value = (self.value, self.DEFAULT_VALUE))



__all__ = ('ValuedObj', )