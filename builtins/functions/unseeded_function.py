from types import LambdaType, FunctionType, MethodType

from . import logger
from . import MathObj, NamedObj, UserObj, tq
from .seeded_function import SeededFunction

class UnseededFunction(NamedObj):
	
	SEEDED_TYPE = SeededFunction
	_DEFAULT_ARGLEN = None
	_DEFAULT_BASE_FUNC = None
	_DEFAULT_ARGS_STR = None
	_DEFAULT_BODY_STR = None
	_ALLOWED_BASE_FUNC_TYPES = (LambdaType, FunctionType, MethodType)
	def __init__(self, *,
			base = None,
			arglen = None,
			body_str = None,
			args_str = None,
			**kwargs):
		super().__init__(**kwargs)
		self.base = base if base	is not None else self._DEFAULT_BASE_FUNC
		self.body_str  = body_str  if body_str	is not None else self._DEFAULT_ARGLEN
		self.args_str  = args_str  if args_str	is not None else self._DEFAULT_BODY_STR
		self._arglen   = arglen    if arglen	is not None else self._DEFAULT_ARGS_STR
		if not callable(self.base):
			logger.warning("base of type '{}' is not callable!".format(tq(self.base)))
	def __call__(self, *args):
		return self.SEEDED_TYPE(base = self, call_args = args)

	base = property(doc = "The function this UnseededFunction is built around.")

	@base.getter
	def base(self):
		return self._base_func

	@base.setter
	def base(self, new_base):
		if not isinstance(new_base, self._ALLOWED_BASE_FUNC_TYPES):
			logger.warning("Attempted to set BASE_FUNC to unknown type '{}'. Allowed types: {}".format(
				type(new_base).__qualname__,
				', '.join('%r' % x.__qualname__ for x in self._ALLOWED_BASE_FUNC_TYPES)))
		self._base_func = new_base

	@property
	def arglen(self):
		if self._arglen is not self._DEFAULT_ARGLEN:
			return self._arglen
		assert self.base is not None, self.base
		return self.base.__code__.co_argcount


	def _gen_repr(self, args, kwargs):
		assert 'base' not in kwargs, kwargs
		assert 'arglen' not in kwargs, kwargs
		assert 'args_str' not in kwargs, kwargs
		assert 'body_str' not in kwargs, kwargs

		if self.base is not self._DEFAULT_BASE_FUNC:
			kwargs['base'] = '<some function>'#self.base
		if self.arglen is not self._DEFAULT_ARGLEN:
			kwargs['arglen'] = self.arglen
		if self.args_str is not self._DEFAULT_ARGS_STR:
			kwargs['args_str'] = self.args_str
		if self.body_str is not self._DEFAULT_BODY_STR:
			kwargs['body_str'] = self.body_str
		return (args, kwargs)

	__slots__ = ('body_str', 'args_str', '_name')

class UserUnseededFunction(UserObj, UnseededFunction, is_pymath_userobj=True):
	def __init__(self, func, name = UnseededFunction._DEFAULT_NAME):
		super().__init__(base = func, name = name)


	def _gen_repr(self, args, kwargs):
		assert not args, args
		assert not kwargs, kwargs
		if self.base is not self._DEFAULT_BASE_FUNC:
			args = (self.base,)
		if self.hasname():
			kwargs['name'] = self.name
		return (args, kwargs)

	def __matmul__(self, other):
		return self(*other)










