from typing import Any

from . import logger
from .named_obj import NamedObj
from .valued_obj import ValuedObj

class NamedValuedObj(NamedObj, ValuedObj):
	''' Represents an object that can have both a name and a value.

	This class is meant to be subclassed, and shouldn't be instanced directly.

	If attempting to directly instantiate a NamedValuedObj, a warning will be logged.
	'''


	def __init__(self, **kwargs: Any) -> None:
		''' Initializes self 
		
		If attempting to directly instantiate a NamedValuedObj, a warning will be logged.

		Arguments:
			**kwargs -- Extra kwargs, will be ignored for this class.
		'''

		if __debug__:
			if type(self) == NamedValuedObj:
				logger.warning("Should not instantiate {} directly!".format(type(self).__qualname__))
		super().__init__(**kwargs)


	def __str__(self) -> str:
		''' Returns a string representation of this class.

		Returns:
			ValuedObj.__str__(self) -- If 'self.known()' evaluates to True
			NamedObj.__str__(self)  -- If 'self.known()' evaluates to False
		'''
		if self.isknown():
			return ValuedObj.__str__(self)

		if __debug__:
			assert not self.isknown()
		assert True #assert super() type is NamedObj
		return super().__str__()

	def __repr__(self) -> str:
		''' Returns the string defined by gen_repr with kwargs 'name' and 'value'. '''
		return self.gen_repr(name  = (self.name, self.DEFAULT_NAME),
							 value = (self.value, self.DEFAULT_VALUE))
