from typing import Callable, Union

from . import MathObj, NamedObj
from .seeded_function import SeededFunction
BASE_FUNC_TYPE = Callable[[MathObj, type(...)], MathObj]

class UnseededFunction(NamedObj):
	SEEDED_TYPE = SeededFunction
	DEFAULT_BASE_FUNC = None
	DEFAULT_FUNC_STRS = {}

	def __init__(self,
			base_func: Union[BASE_FUNC_TYPE, 'defaults.BASE_FUNC'] = defaults.BASE_FUNC,
			func_strs = DEFAULT_FUNC_STRS,
			argl = DEFAULT_ARGL
			**kwargs):
		if base_func != self.defaults.BASE_FUNC:
			# this allows for later subclassing of basefunc.
			self.base_func = base_func
		self.func_strs = func_strs
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
