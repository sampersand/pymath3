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

class UserConstant(UserObj, Constant):
	''' The user class for Constant.

	This class is provided for ease of use (such as not having to
	pass keywords to the constructor) but shouldn't be used when robustness is necessary.
	'''

	def __init__(self, value = Constant._default_value):
		''' Initiates self.
		
		This function passes 'value' to Constant's constructor, and nothing else.

		Arguments:
			value -- The value of this class. (default: __defaults__.value)
		Returns:
			None
		'''
		super().__init__(value = value)