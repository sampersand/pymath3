from . import MathObj
class UserObj(MathObj):
	'''
	Base class for all objects that should be directly instanced by the user.

	These classes _CAN_ accept positional args in their __init__ function, but should immediately
	pass them as keyword arguments to the class they are subclassing.

	This class can also use regex to find optional values, but this can be disabled.
	'''
