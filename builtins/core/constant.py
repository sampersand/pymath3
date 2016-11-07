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
	_DEFAULT_VALUE = 0
	def __str__(self):
		return str(self.value)
class UserConstant(UserObj, Constant, is_pymath_userobj=True):
	''' The UserObj for Constant

	See UserObj for more information on User objects.
	'''
	def __init__(self, value = Constant._DEFAULT_VALUE):
		''' Initiates self.
		
		This function passes 'value' to Constant's constructor, and nothing else.

		Arguments:
			value -- The value of this class. (default: Constant._DEFAULT_VALUE)
		Returns:
			None
		'''
		super().__init__(value = value)


	def _gen_repr(self, args, kwargs):
		assert not args and not kwargs
		if self.hasvalue():
			args = (self.value, )
		return super()._gen_repr(args, kwargs)

	__slots__ = ('_value', )



