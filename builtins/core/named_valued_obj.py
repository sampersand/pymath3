from . import logger
from .math_obj import MathObj
from .named_obj import NamedObj
from .valued_obj import ValuedObj

class NamedValuedObj(NamedObj, ValuedObj):
	''' Represents an object that can have both a name and a value.

	This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
	warning will be logged.
	'''

	def __init__(self, *args, **kwgs):
		'''Initialize self.

		This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
		warning will be logged.

		Arguments:
			*args    -- Ignored
			**kwgs -- Ignored
		Returns:
			None
		'''

		__class__.checktype(self)
		super().__init__(*args, **kwgs)


	def __str__(self):
		''' Returns a string representation of this class.

		Returns:
			ValuedObj.__str__(self) -- If 'self.known()' evaluates to True
			NamedObj.__str__(self)  -- If 'self.known()' evaluates to False
		'''
		if self.hasvalue():
			return ValuedObj.__str__(self)

		assert not self.hasvalue()
		assert True #assert super() type is NamedObj

		return NamedObj.__str__(self)

	def isconst(self, du):
		assert not du.hasvalue()
		assert self is not du or not self.hasvalue()
		return self is not du or self.hasvalue() or not self.hasname() or self.name != du.name















