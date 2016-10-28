from . import logger
from .named_obj import NamedObj
from .valued_obj import ValuedObj

class NamedValuedObj(NamedObj, ValuedObj):

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

		return super().__str__(self)

	def __repr__(self) -> str:
		''' Returns the string defined by gen_repr(name, value) '''
		return self.gen_repr(name  = (self.name, self.DEFAULT_NAME),
							 value = (self.value, self.DEFAULT_VALUE))
