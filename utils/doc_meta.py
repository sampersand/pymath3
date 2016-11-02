from inspect import isfunction
from . import logger, from_stack, tq
class DocMeta(type):
	def __init__(cls, name, bases, attrs, **kwargs):
		super().__init__(name, bases, attrs, **kwargs)

# def setdoc_unstable(parent, *, TODO: 'THIS'):
# 	__docs__ = from_stack('__docs__', 2) if __docs__ is None else __docs__
# 	### Check parent
# 	warntype(parent, type, 'parent')
# 	assert isinstance(parent, type)

def setdoc(*, __docs__ = None, formats = {}): #also called 'setdoc_unstable'
	if __docs__ is None:
		__docs__ = from_stack('__docs__', 2)
	return setdoc_func(__docs__, formats = formats)
def setdoc_func(__docs__, *, formats = {}):
	def capture(func):
		if not isfunction(func):
			raise TypeError("'func' must be a function, not {}".format(tq(func)))
		assert hasattr(func, '__name__') # functions should have names...
		func_name = func.__name__
		assert isinstance(func_name, str), type(func_name)
		return setdoc_stable(__docs__, func, func_name, formats)
	return capture
def setdoc_stable(__docs__, func, func_name, formats = {}):

	### check docs
	if not isinstance(__docs__, dict):
		logger.debug("Unexpected type '{}' for __docs__".format(tq(__docs__)))
	if not hasattr(__docs__, '__getitem__'):
		raise AttributeError("__docs__ needs to define a '__getitem__' function")
	assert hasattr(__docs__, '__getitem__')

	### check func_name
	if not isinstance(func_name, str):
		logger.debug("Unexpected type '{}' for func_name".format(tq(func_name)))
	if func_name not in __docs__:
		raise KeyError("func_name '{}' is not in __docs__".format(func_name))
	
	##check formats
	if not isinstance(formats, dict):
		logger.debug("Unexpected type '{}' for formats".format(tq(formats)))
	#checking for mappings would go here


	## create default_doc and check it
	default_doc = __docs__[func_name]
	if not isinstance(default_doc, str):
		logger.warning("Unexpected type '{}' for __docs__[func_name]".format(tq(default_doc)))


	assert hasattr(default_doc, 'format') #str should by default

	func_doc = default_doc.format(**formats)

	try:
		func.__doc__ = func_doc
	except AttributeError as err:
		logger.error("Unable to set __doc__ for func '{}' (func_name={})".format(func, func_name))

	return func




class parentclass(metaclass=DocMeta):
	def somefunc(self, a):
		'''documentation for somefunc'''
		return a
class foo(parentclass):
	__docs__ = {
		'somefunc': 'blargh'
	}


	@setdoc()
	def somefunc(self, a):
		return a + 1

print(foo.somefunc.__doc__, 'a')












# quit()
#