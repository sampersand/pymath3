from typing import Union, Any, Generic, TypeVar
from .math_obj import MathObj
T = TypeVar('T')
class ValuedObj(MathObj, Generic[T]):
	''' Represents an object that can have a value.

	This class is meant to be subclassed, and shouldn't be instanced directly.

	See Constant and Variable for builtin subclasses for this.
	'''

	_DEFALUT_VALUE = None

	def __init__(self, value: Union[T, type(_DEFALUT_VALUE)] = _DEFALUT_VALUE, **kwargs: Any) -> None:
		''' Initializes self with 'value'
		
		Value can be omitted, and defaults to None.
		'''
		self.value = value
		super().__init__(**kwargs)


	value = property(doc = "The resulting value of this class")

	@value.getter
	def value(self) -> Union[T, type(_DEFALUT_VALUE)]:
		return self._value

	@value.setter
	def value(self, val: T) -> None:
		self._value = val

	@value.deleter
	def value(self) -> None:
		self._value = self._DEFALUT_VALUE

	def isknown(self) -> bool:
		''' Return true if this this class has a value. '''
		return self.value != self._DEFALUT_VALUE

	def __str__(self) -> str:
		if self.isknown():
			return str(self.value)
		return super().__str__()
	def __repr__(self) -> str:
		return self.gen_repr(value = (self.value, self._DEFALUT_VALUE))
