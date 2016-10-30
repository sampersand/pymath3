from typing import Union, Any, Generic, TypeVar

from . import logger
from .math_obj import MathObj

T = TypeVar('T')
class NamedObj(MathObj):#, Generic[T]):
	''' Represents an object that can have a name.

	This class is meant to be subclassed, and shouldn't be instanced directly.

	See Constant and Variable for builtin subclasses for this.
	
	If attempting to directly instantiate a NamedObj, a warning will be logged.
	'''
	__this_defaults__ = {'name': None, }
	__update_defaults__(__this_defaults__, __defaults__)

	def __init__(self,
		name: Union[T, __defaults__.name] = __defaults__.name,
		**kwargs: Any) -> None:
		''' Initializes self with 'name'
		
		If attempting to directly instantiate a NamedObj, a warning will be logged.

		Arguments:
			name    -- The name of this class. (default: NamedObj.DEFAULT_NAME)
			**kwargs -- Extra kwargs, will be ignored for this class.
		'''

		if __debug__ and type(self) == NamedObj:
			logger.warning("Should not instantiate {} directly!".format(type(self).__qualname__))

		self.name = name
		super().__init__(**kwargs)


	name = property(doc = "The name of this class")

	@name.getter
	def name(self) -> Union[T, type(__defaults__.name)]:
		return self._name

	@name.setter
	def name(self, val: T) -> None:
		self._name = val

	@name.deleter
	def name(self) -> None:
		self._name = self.__defaults__.name

	def hasname(self) -> bool:
		''' Return true if this this class has a name. '''
		return self.name != self.__defaults__.name

	def __str__(self) -> str:
		''' Returns a string representation of this class.

		Returns:
			str(self.name)    -- If 'self.hasname()' evaluates to True
			super().__str__() -- If 'self.hasname()' doesn't evaluate to True
		'''
		if self.hasname():
			return str(self.name)

		assert __debug__ or not self.hasname()

		return super().__str__()

	def __repr__(self) -> str:
		''' Returns the string defined by gen_repr with the kwarg 'name'. '''
		return self.gen_repr(name = (self.name, self.__defaults__.name))



__all__ = ('NamedObj', )