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

	__this_defaults__ = {
		'value': 0,
		'allowed_types': (int, float, bool, complex)
	}
	__update_defaults__(__this_defaults__, __defaults__) # just to be explicit

	__slots__ = __gen_slots__()

	def __init__(self,
				value: __defaults__.allowed_types = __defaults__.value,
				**kwargs: Union[Any, Any]) -> None:
		''' Instantiates self.

		If value is not of __defaults__.allowed_types, a warning will be logged.

		Arguments:
			value    -- The value of this class. (defaults: Constant.DEFAULT_VALUE)
			**kwargs -- Extra kwargs, will be ignored for this class.
		Returns:
			None
		'''

		if not isinstance(value, self.__defaults__.allowed_types):
			logger.warning('Recieved invalid type for value: {}. Allowed types: {}'.format(
				type(value),
				self.__defaults__.allowed_types))
		super().__init__(value = value, **kwargs)

class UserConstant(UserObj, Constant):
	''' The user class for Constant.

	This class is provided for ease of use (such as not having to
	pass keywords to the constructor) but shouldn't be used when robustness is necessary.
	'''

	def __init__(self, value: __defaults__.allowed_types = __defaults__.value) -> None:
		''' Initiates self.
		
		This function passes 'value' to Constant's constructor, and nothing else.

		Arguments:
			value -- The value of this class. (default: __defaults__.value)
		Returns:
			None
		'''
		super().__init__(value = value)

	def __repr__(self):
		''' Returns the string defined by gen_repr with the varg 'value'. '''
		return self.gen_repr(self.value)







