from . import logger
from . import NamedObj, ValuedObj

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
		assert True #assert super() type is NamedObj
		return super().__str__()

	def __repr__(self) -> str:
		''' Returns the string defined by gen_repr with kwargs 'name' and 'value'. '''
		return self.gen_repr(name  = (self.name, self.DEFAULT_NAME),
							 value = (self.value, self.DEFAULT_VALUE))
