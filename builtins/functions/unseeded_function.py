from . import MathObj, NamedObj
from .seeded_function import SeededFunction

class UnseededFunction(NamedObj):
	
	SEEDED_TYPE = SeededFunction
	_DEFAULT_ARGLEN = None
	_DEFAULT_BASE_FUNC = None
	_DEFAULT_ARGS_STR = None
	_DEFAULT_BODY_STR = None

	def __init__(self, *,
			base_func = None,
			arglen = None,
			body_str = None,
			args_str = None,
			**kwargs):
		super().__init__(**kwargs)
		self.base_func = base_func if base_func	is not None else self._DEFAULT_BASE_FUNC
		self.body_str  = body_str  if body_str	is not None else self._DEFAULT_ARGLEN
		self.args_str  = args_str  if args_str	is not None else self._DEFAULT_BODY_STR
		self._arglen   = arglen    if arglen	is not None else self._DEFAULT_ARGS_STR

	def __call__(self, *args):
		return self.SEEDED_TYPE(unseeded_base = self, call_args = args)

	base_func = property(doc = "The function this UnseededFunction is built around.")

	@base_func.getter
	def base_func(self):
		return self._base_func

	@base_func.setter
	def base_func(self, new_base_func):
		self._base_func = new_base_func

	@property
	def arglen(self):
		if self._arglen is not self._DEFAULT_ARGLEN:
			return self._arglen
		assert self.base_func is not None, self.base_func
		return self.base_func.__code__.co_argcount


	def _gen_repr(self, args, kwargs):
		assert 'base_func' not in kwargs, kwargs
		assert 'arglen' not in kwargs, kwargs
		assert 'args_str' not in kwargs, kwargs
		assert 'body_str' not in kwargs, kwargs

		if self.base_func is not self._DEFAULT_BASE_FUNC:
			kwargs['base_func'] = '<some function>'#self.base_func
		if self.arglen is not self._DEFAULT_ARGLEN:
			kwargs['arglen'] = self.arglen
		if self.args_str is not self._DEFAULT_ARGS_STR:
			kwargs['args_str'] = self.args_str
		if self.body_str is not self._DEFAULT_BODY_STR:
			kwargs['body_str'] = self.body_str
		return super()._gen_repr(args, kwargs)

	__slots__ = ('body_str', 'args_str', '_name')
















