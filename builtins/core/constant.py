from . import logger
from .valued_obj import ValuedObj
from .user_obj import UserObj
class Constant(ValuedObj):
	''' A class representing a mathematical constant, such as '4' or 'pi'

	This class can be directly instantiated, but still requires keyword arguments. The User-class
	UserConstant can be substituted if ease of use is required. However, Constant is much more 
	robust.
	'''

	_default_value = 0
	_allowed_types = (int, float, bool, complex)

	def __init__(self, value = _default_value, **kwargs):
		''' Instantiates self.

		If value is not of __defaults__.allowed_types, a warning will be logged.

		Arguments:
			value    -- The value of this class. (defaults: Constant.DEFAULT_VALUE)
			**kwargs -- Extra kwargs, will be ignored for this class.
		Returns:
			None
		'''

		if not isinstance(value, self._allowed_types):
			logger.warning("Value is unknown type '{}'. Allowed types: {}".format(
				type(value).__qualname__,
				', '.join('%r' % x.__qualname__ for x in self._allowed_types)))
		super().__init__(value = value, **kwargs)

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