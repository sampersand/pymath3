from . import MathObj, NamedObj
from .seeded_function import SeededFunction

class UnseededFunction(NamedObj):
	
	seeded_type = SeededFunction
	_default_func_arglen = None
	_default_base_func = None
	_default_args_str = None
	_default_body_str = None

	def __init__(self,
			base_func = _default_base_func,
			arglen = _default_func_arglen,
			body_str = _default_body_str,
			args_str = _default_args_str,
			**kwargs):
		super().__init__(**kwargs)
		self.base_func = base_func
		self.body_str = body_str
		self.args_str = args_str
		self.arglen = arglen

	def __call__(self, *args):
		return self.seeded_type(unseeded_base = self, base_args = args)

	base_func = property(doc = "The function this UnseededFunction is built around.")

	@base_func.getter
	def base_func(self):
		return self._base_func

	@base_func.setter
	def base_func(self, new_base_func):
		self._base_func = new_base_func


