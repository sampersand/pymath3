from typing import Union, Any

from . import logger
from .valued_obj import ValuedObj
from .user_obj import UserObj
class Constant(ValuedObj):
	''' A class representing a mathematical constant, such as '4' or 'pi'

	This class can be directly instantiated, but still requires keyword arguments. The User-class
	UserConstant can be substituted if ease of use is required. However, Constant is much more 
	robust.
	'''

	DEFAULT_VALUE = 0
	DEFAULT_ALLOWED_TYPES = (int, float, bool, complex)

	def __init__(self,
				value: DEFAULT_ALLOWED_TYPES = DEFAULT_VALUE,
				**kwargs: Union[Any, Any]) -> None:
		''' Instantiates self.

		If value is not of DEFAULT_ALLOWED_TYPES, a warning will be logged.

		Arguments:
			value    -- The value of this class. (defaults: Constant.DEFAULT_VALUE)
			**kwargs -- Extra kwargs, will be ignored for this class.
		Returns:
			None
		'''

		if not isinstance(value, self.DEFAULT_ALLOWED_TYPES):
			logger.warning('Recieved invalid type for value: {}. Allowed types: {}'.format(
				type(value),
				self.DEFAULT_ALLOWED_TYPES))
		super().__init__(value = value, **kwargs)
class UserConstant(UserObj, Constant):
	''' The user class for Constant.

	This class is provided for ease of use (such as not having to
	pass keywords to the constructor) but shouldn't be used when robustness is necessary.
	'''

	def __init__(self, value: Constant.DEFAULT_ALLOWED_TYPES = Constant.DEFAULT_VALUE) -> None:
		''' Initiates self.
		
		This function passes 'value' to Constant's constructor, and nothing else.

		Arguments:
			value -- The value of this class. (defaults: Constant.DEFAULT_VALUE)
		Returns:
			None
		'''
		super().__init__(value = value)

	def __repr__(self):
		''' Returns the string defined by gen_repr with the varg 'value'. '''
		return self.gen_repr(self.value)







