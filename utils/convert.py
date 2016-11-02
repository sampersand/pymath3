from . import logger
from inspect import signature, isfunction
class AutoType():
	instance = None
	__slots__ = ()
	def __new__(cls):
		if cls.instance is not None:
			logger.debug('Attempted to re-instantiate {}, using current instance instead!'.
				format(type(cls).__qualname__))
			return cls.instance
		return super().__new__(cls)
	def __init__(self):
		inst = type(self).instance
		assert inst is None or inst is self
		if inst is self:
			return
		type(self).instance = self

	def __repr__(self):
		return '<{}>'.format(type(self).__qualname__)

	def __init_subclass__(self, *args, **kwargs):
		raise TypeError('Cannot extend type {}'.format(type(self)))

auto = AutoType()

def _update_positional(func, defaults):
	assert isfunction(func), 'Need a function to update the positional args of'
	assert hasattr(func, '__defaults__'), 'Functions should have __defaults__...'
	assert isinstance(defaults, dict), 'Passed defaults need to be a dict'
	if not func.__defaults__:
		assert hasattr(func, '__name__')
		logger.debug('Function {} has an empty/None __defaults__'.format(func.__name__))
		return

	s = signature(func)
	params = s.parameters
	new_defaults = []
	assert hasattr(params, 'items')
	assert hasattr(params, '__getitem__')
	empty = s.empty
	for arg_name in (n for n, v in params.items() if v.kind == v.POSITIONAL_OR_KEYWORD):
		assert arg_name in params # They come from params.items...
		arg_default = params[arg_name].default
		assert empty is params[arg_name].empty

		if arg_default is empty:
			assert hasattr(func, '__name__')
			logger.debug('arg_name {}.{} is empty'.format(func.__name__, arg_name))
			continue

		if arg_default is auto:
			if arg_name not in defaults:
				raise AttributeError("Argument '{}' is not in defaults!".format(arg_name))
			arg_default = defaults[arg_name]

		new_defaults.append(arg_default)
	func.__defaults__ = tuple(new_defaults)

def _update_keywords(func, defaults):
	assert isfunction(func), 'Need a function to update the keyword args of'
	assert hasattr(func, '__kwdefaults__'), 'Functions should have __kwdefaults__...'
	assert isinstance(defaults, dict), 'Passed defaults need to be a dict'
	if not func.__kwdefaults__:
		assert hasattr(func, '__name__')
		logger.debug('Function {} has an empty/None __kwdefaults__'.format(func.__name__))
		return
	assert isinstance(func.__kwdefaults__, dict) # python sets this by default...
	for kw_name, val in func.__kwdefaults__.items():
		if val is auto:
			if kw_name not in defaults:
				raise KeyError("Keyword '{}' not in defaults!".format(kw_name))
			func.__kwdefaults__[kw_name] = defaults[kw_name]

# def _default_retriever(func, defaults):
# 	assert isfunction(func), 'Need a function to find the defaults for'
# 	assert isinstance(defaults, dict), 'Passed defaults need to be a dict'

# 	if not hasattr(func, '__name__'):
# 		raise AttributeError('Cannot extract __name__ from func!')

# 	assert hasattr(func, '__name__')
# 	return defaults[func.__name__]

def convert(defaults, func):
	''' Replace all 'autos' of a function with their corresponding values in defaults.
	'''

	if not isinstance(defaults, dict):
		logger.warning('Recieved non-dict for defaults: {}'.format(type(defaults)))
	if not isfunction(func):
		logger.warning("Attempting to convert non-function type {}".format(type(func)))
	
	assert isfunction(func), type(func)
	assert isinstance(defaults, dict)

	if defaults is None:
		defaults = _retriever(func, __defaults__)


	if not isinstance(defaults, dict):
		logger.warning('Computed defaults is non-dict type {}'.formaT(type(defaults)))
	assert hasattr(defaults, '__getitem__')

	_update_positional(func, defaults)
	_update_keywords(func, defaults)

	return func
__all__ = 'convert', 'auto'


