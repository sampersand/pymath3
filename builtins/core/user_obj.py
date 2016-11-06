from .math_obj import MathObj
class UserObj(MathObj):
	'''
	Base class for all objects that should be directly instanced by the user.

	These classes _CAN_ accept positional args in their __init__ function, but should immediately
	pass them as keyword arguments to the class they are subclassing.

	This class can also use regex to find optional values, but this can be disabled.

	Subclasses of this should not be extended. To inherit, extend the non-user class they are
	referincing.

	This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
	warning will be logged.
	'''

	def __init__(self, *args, **kwargs):
		__class__.checktype(self)
		super().__init__(*args, **kwargs)

	def _gen_repr(self, args, kwargs):
		return MathObj._gen_repr(self, args, kwargs) #bypasses any supers

	@staticmethod
	def __init_subclass__(*, is_pymath_userobj = False, **kwargs):
		if not is_pymath_userobj:
			raise TypeError("UserObj's children cannot be subclassed!")

	__slots__ = ()