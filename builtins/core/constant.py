from typing import Union, Any

from . import logger
from . import ValuedObj, UserObj
class Constant(ValuedObj):
	''' A class representing a mathematical constant, such as '4' or 'pi'

	This class can be directly instantiated, but still requires keyword arguments. The User-class
	UserConstant can be substituted if ease of use is required. However, Constant is much more 
	robust.
	'''

	DEFAULT_VALUE = 0
	ALLOWED_TYPE_VALUES = (int, float, bool, complex)

	def __init__(self,
				value: ALLOWED_TYPE_VALUES = DEFAULT_VALUE,
				**kwargs: Union[Any, Any]) -> None:
		''' Instantiates self.

		If value is not of ALLOWED_TYPE_VALUES, a warning will be logged.

		Arguments:
			value    -- The value of this class. (default: Constant.DEFAULT_VALUE)
			**kwargs -- Extra kwargs, will be ignored for this class.
		Returns:
			None
		'''

		if not isinstance(value, self.ALLOWED_TYPE_VALUES):
			logger.warning('Recieved invalid type for value: {}. Allowed types: {}'.format(
				type(value),
				self.ALLOWED_TYPE_VALUES))
		super().__init__(value = value, **kwargs)
class UserConstant(UserObj, Constant):
	''' The user class for Constant.

	This class is provided for ease of use (such as not having to
	pass keywords to the constructor) but shouldn't be used when robustness is necessary.
	'''

	def __init__(self, value: Constant.ALLOWED_TYPE_VALUES = Constant.DEFAULT_VALUE) -> None:
		''' Initiates self.
		
		This function passes 'value' to Constant's constructor, and nothing else.

		Arguments:
			value -- The value of this class. (default: Constant.DEFAULT_VALUE)
		Returns:
			None
		'''
		super().__init__(value = value)

	def __repr__(self):
		''' Returns the string defined by gen_repr with the varg 'value'. '''
		return self.gen_repr(self.value)







