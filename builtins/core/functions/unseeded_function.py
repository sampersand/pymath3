from typing import Callable, Union, Dict, AnyStr

from . import MathObj, NamedObj
from .seeded_function import SeededFunction
BASE_FUNC_TYPE = Callable[[MathObj, type(...)], MathObj]

class UnseededFunction(NamedObj):

	defaults = {
		'seeded_type': SeededFunction,
		'base_func': None,
		'func_strs': {
			'args': None,
			'body': None,
		},
		'arglen': None,
	}

	def __init__(self,
			base_func: Union[BASE_FUNC_TYPE, 'defaults.base_func'] = defaults.base_func,
			func_strs: Dict[AnyStr, AnyStr] = DEFAULT_FUNC_STRS,
			arglen = defaults.arglen
			**kwargs):
		if base_func != self.defaults.base_func:
			self.base_func = base_func
		self.func_strs = func_strs
		self.arglen = arglen
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


