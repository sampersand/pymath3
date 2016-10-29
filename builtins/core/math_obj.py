from typing import Tuple, Any, Union
from . import logger

from .default_meta import DefaultMeta
class MathObj(metaclass=DefaultMeta):
	'''
	Base class for all PyMath Objects.

	If attempting to directly instantiate a ValuedObj, a warning will be logged.
	'''

	def __init__(self, **kwargs: Union[Any, Any]) -> None:
		''' Instantiates self.

		If attempting to directly instantiate a MathObj, a warning will be logged.

		Arguments:
			**kwargs -- Extra kwargs, will be ignored for this class.
		Returns:
			None
		'''

		# if args:
		# 	logger.warning("Class type {} is using *args!".format(type(self).__qualname__))
		if __debug__ and type(self) == MathObj:
			logger.warning("Should not instantiate {} directly!".format(type(self).__qualname__))
		super().__init__(**kwargs)

	@classmethod
	def gen_repr(cls, *vargs: Any, **kwargs: Union[str, Tuple[Any, Any]]) -> str:
		''' Genereates a repr for 'cls' based on the vargs and kwargs passed.

		Result is roughly:
			cls(arg1, arg2, ..., kwarg1=value1, kwarg2=value2, ...)

		if *vargs are used when not 'issubclass(cls, UserObj)', a warning will be logged.
		if **kwargs are not passed in the format 'key : (given_value, default_value)', a warning
			will be logged.

		Keyword values should be a tuple of given and default values
			key : (given_value, default_value)

		If given_value == default_value, then 'key' will not be added to the resulting string, 
			
		Arguments:
			cls      -- The class to make a representation for.
			*vargs   -- The positional arguments to be used. This should only be used when
			            'issubclass(cls, UserObj)' is evalued to True.
			**kwargs -- The keyword values to be used. They should be given in the format 
						key : (given_value, default_value). if given_value == default_value,
						'key' is ommitted from the result.
		Returns:
			A string representation of 'cls' built from the passed *vargs and **kwargs.
		'''

		if __debug__:
			assert type(vargs) == tuple, 'python should make *vargs a tuple by default'
			assert type(kwargs) == dict, 'python should make **kwargs a dict by default'
			from .user_obj import UserObj
			if vargs and not issubclass(cls, UserObj):
				logger.warning('*vargs passed to gen_repr for non-UserObj type {}'.format(cls))
			for key, value in kwargs.items():
				if not isinstance(value, (list, tuple)) or len(value) != 2:
					logger.warning("Value isn't (given, default), but {}".format(value))

		args_str = ', '.join(str(arg) for arg in vargs)
		kwargs_str = {}
		for key, (given, default) in kwargs.items():
			if given != default: #should it be 'is not'?
				kwargs_str[key] = given
		kwargs_str = ', '.join('='.join((str(x[0]), str(x[1]))) for x in kwargs_str.items())
		comma = ', ' if args_str and kwargs else ''
		return '{}({}{}{})'.format(cls.__qualname__, args_str, comma, kwargs_str)
	
	def __repr__(self) -> str:
		''' Returns the string defined by gen_repr with no args. '''
		return self.gen_repr()



