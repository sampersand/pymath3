from . import logger
from .valued_obj import ValuedObj
from .user_obj import UserObj
class Constant(ValuedObj):
	''' A class representing a mathematical constant, such as '4' or 'pi'

	This class can be directly instantiated, but still requires keyword arguments. The User-class
	UserConstant can be substituted if ease of use is required. However, Constant is much more 
	robust.
	'''
	__slots__ = ('_value', )
	_default_value = 0

class UserConstant(UserObj, Constant, is_pymath_userobj=True):
	''' The UserObj for Constant

	See UserObj for more information on User objects.
	'''
	def __init__(self, value = Constant._default_value):
		''' Initiates self.
		
		This function passes 'value' to Constant's constructor, and nothing else.

		Arguments:
			value -- The value of this class. (default: Constant._default_value)
		Returns:
			None
		'''
		super().__init__(value = value)


	def __repr__(self):
		if self.hasvalue():
			return '{}({!r})'.format(type(self).__qualname__, self.value)
		return super().__repr__()
