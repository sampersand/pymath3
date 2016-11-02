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

	def __init__(self, name = Variable._default_name, value = Variable._default_value):
		''' Initializes self. 

		This differs from Variable solely due to the fast that this can accept positional arguments,
		and some of the arguments (such as name) can be inferred from the declaration context.

		Arguments:
			name  -- The name of this variable. Can be inferred
			         (default: Variable._default_name)
			value -- The value of this variable. Can't be inferred
			         (default: Variable._default_value)
		Returns:
			None
		'''

		super().__init__(name = name, value = value)

	def __repr__(self):
		if self.hasname() and self.hasvalue():
			return '{}({!r}, {!r})'.format(type(self).__qualname__, self.name, self.value)
		elif self.hasname():
			assert not self.hasvalue()
			return '{}({!r})'.format(type(self).__qualname__, self.name)
		elif self.hasvalue():
			assert not self.hasname()
			return '{}(value={!r})'.format(type(self).__qualname__, self.value)
		else:
			assert not self.hasname() and not self.hasvalue()
			return super().__repr__()

__slots__ = ('_value', '_name')