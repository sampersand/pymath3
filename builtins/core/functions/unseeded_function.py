from typing import Callable, Union, Dict, AnyStr

from . import MathObj, NamedObj, DefaultMeta
from .seeded_function import SeededFunction
BASE_FUNC_TYPE = Callable[[MathObj, type(...)], MathObj]

class UnseededFunction(NamedObj, metaclass=DefaultMeta):

	DEFAULT_SEEDED_TYPE = SeededFunction
	DEFAULT_FUNC_ARGLEN = None
	DEFAULT_BASE_FUNC = None
	DEFAULT_FUNC_ARGS = None
	DEFAULT_FUNC_BODY = None
	DEFAULT_FUNC_STRS = (DEFAULT_FUNC_ARGS, DEFAULT_FUNC_BODY)

	def __init__(self,
			base_func: Union[BASE_FUNC_TYPE, 'type(print(defaults)))', 'type(defaults.base_func)'] = None,
			func_strs: Union[Dict[AnyStr, AnyStr], 'defaults.func_strs'] = None,
			arglen: Union[int, 'defaults,func_strs']  = None,
			**kwargs):
		self.set_values(base_func = base_func, func_strs = func_strs, arglen = arglen)
		super().__init__(**kwargs)

	def __call__(self, *args):
		return self.SEEDED_TYPE(unseeded_base = self, base_args = args)

	base_func = property(doc = "The function this UnseededFunction is built around.")
	@base_func.getter
	def base_func(self) -> Union[BASE_FUNC_TYPE, defaults.BASE_FUNC]:
		return self._base_func

	@base_func.setter
	def base_func(self, new_base_func: BASE_FUNC_TYPE) -> None:
		self._base_func = new_base_func


