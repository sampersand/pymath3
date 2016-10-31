# from . import logger
from inspect import signature, isfunction
class auto_type():
	subclasses = None
auto = type('auto_type', (),
	{'__repr__': lambda self: '<{}>'.format(type(self).__qualname__),
	'__slots__': ()})()


def _update_positional(func, __defaults__):
	if not func.__defaults__:
		return
	s = signature(func)
	param = s.parameters
	defaults = []

	for arg_name in (n for n, v in s.parameters.items() if v.kind == v.POSITIONAL_OR_KEYWORD):
		if param[arg_name].default == param[arg_name].empty:
			continue

		to_append = param[arg_name].default
		if to_append is auto:
			to_append = __defaults__[arg_name]
		defaults.append(to_append)

	func.__defaults__ = tuple(defaults)

def _update_keywords(func, __defaults__):
	if not func.__kwdefaults__:
		return

	for kw_name, val in func.__kwdefaults__.items():
		if val is auto:
			func.__kwdefaults__[kw_name] = __defaults__[kw_name]

def _default_retriever(func, defaults):
	return defaults[func.__name__]

def convert(__defaults__, *, _retriever = _default_retriever):

	if __debug__ and _retriever is not _default_retriever:
		logger.debug('Recieved non-default _retriever: {}'.format(_retriever))
	if not callable(_retriever):
		logger.warning('Passed _retriever is not callable')
	if not isinstance(__defaults__, dict):
		logger.warning('Passed __defaults__ is non-dict type {}'.format(type(__defaults__)))

	assert callable(_retriever), _retriever
	assert hasattr(__defaults__, '__getitem__')

	def capture(func, func_defaults = None):
		if __debug__ and func_defaults is not None:
			logger.debug('Recieved non-default func_defaults: {}'.format(func_defaults))
		if not isfunction(func):
			logger.warning("Attempting to convert non-function type {}".format(type(func)))
		if func_defaults is None:
			assert hasattr(func, '__name__')
		assert isfunction(func), type(func)


		if func_defaults is None:
			func_defaults = _retriever(func, __defaults__)


		if not isinstance(func_defaults, dict):
			logger.warning('Computed func_defaults is non-dict type {}'.formaT(type(func_defaults)))
		assert hasattr(func_defaults, '__getitem__')

		_update_positional(func, func_defaults)
		_update_keywords(func, func_defaults)

		return func
	return capture




