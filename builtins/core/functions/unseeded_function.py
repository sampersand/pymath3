from typing import Callable, Union, Dict, AnyStr

from . import MathObj, NamedObj
from .seeded_function import SeededFunction

BASE_FUNC_TYPE = Callable[[MathObj, type(...)], MathObj]
class UnseededFunction(NamedObj):
	__this_defaults__ = {
		'seeded_type' : SeededFunction,
		'func_arglen' : None,
		'base_func' : None,
		'func_args' : None,
		'func_body' : None,
	}
	__this_defaults__['func_strs'] = (__this_defaults__['func_args'], __this_defaults__['func_body'])
	__update_defaults__(__this_defaults__, __defaults__) # just to be explicit
	print(__defaults__, __defaults__.func_arglen)

	def __init__(self,
			base_func: Union[BASE_FUNC_TYPE, __defaults__.base_func] = None,
			func_strs: Union[Dict[AnyStr, AnyStr], __defaults__.func_strs] = None,
			arglen: Union[int, __defaults__.func_arglen] = None,
			**kwargs):
		super().__init__(**kwargs)
		self.base_func = base_func
		self.func_strs = func_strs
		self.arglen = arglen

	def __call__(self, *args):
		return self.__defaults__.seeded_type(unseeded_base = self, base_args = args)

	base_func = property(doc = "The function this UnseededFunction is built around.")

	@base_func.getter
	def base_func(self) -> Union[BASE_FUNC_TYPE, __defaults__.base_func]:
		return self._base_func

	@base_func.setter
	def base_func(self, new_base_func: BASE_FUNC_TYPE) -> None:
		self._base_func = new_base_func


