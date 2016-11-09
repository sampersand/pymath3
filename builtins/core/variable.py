from . import logger
from .named_valued_obj import NamedValuedObj
from .user_obj import UserObj
class Variable(NamedValuedObj):
	''' Represents a mathematical variable

	This functions similarly to NamedValudObj - the main difference is this can be used in
	differenciation, whilst NamedValudObj cannot.

	This class also has a 'User' version available: UserVariable.

	This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
	warning will be logged.
	'''

class UserVariable(UserObj, Variable, is_pymath_userobj=True):
	''' The UserObj for Variable

	See UserObj for more information on User objects.
	'''

	def __init__(self, name = None, value = None):
		''' Initializes self. 

		This differs from Variable solely due to the fast that this can accept positional arguments,
		and some of the arguments (such as name) can be inferred from the declaration context.

		Arguments:
			name  -- The name of this variable. Can be inferred
			         (default: UserVariable._DEFAULT_NAME)
			value -- The value of this variable. Can't be inferred
			         (default: UserVariable._DEFAULT_VALUE)
		Returns:
			None
		'''
		super().__init__(name = name, value = value)

	def _gen_repr(self, args, kwgs):
		assert not args and not kwgs
		# return super()
		if self.hasname():
			args = (self.name, )
		if self.hasvalue():
			if not args:
				kwgs = {'value': self.value}
			else:
				args = (self.name, self.value)
		return (args, kwgs)

	__slots__ = ('_value', '_name')









