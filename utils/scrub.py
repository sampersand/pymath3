from . import import_module
MathObj, Variable, Constant, UserUnseededFunction = None, None, None, None
def scrub(arg, *, prefer_var = False, **kwargs): # this is _not_ exhaustive
	global MathObj
	MathObj = MathObj or import_module('pymath3.builtins.core.math_obj').MathObj
	if isinstance(arg, MathObj):
		return arg
	global UserUnseededFunction
	UserUnseededFunction = UserUnseededFunction or import_module('pymath3.builtins.functions.unseeded_function').UserUnseededFunction
	if isinstance(arg, UserUnseededFunction._ALLOWED_BASE_FUNC_TYPES):
		return UserUnseededFunction(arg, **kwargs)
	if not prefer_var:
		global Constant
		Constant = Constant or import_module('pymath3.builtins.core.constant').Constant
		if isinstance(arg, Constant._ALLOWED_VALUE_TYPES):
			return Constant(value = arg, **kwargs)
	else:
		assert prefer_var
		global Variable 
		Variable = Variable or import_module('pymath3.builtins.core.variable').Variable
		if isinstance(arg, Variable._ALLOWED_VALUE_TYPES):
			return Variable(value = arg, **kwargs)

	raise TypeError(type(arg))
