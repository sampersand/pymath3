from .math_obj import MathObj
from itertools import repeat
class _UserMeta(type):
	def __getitem__(cls, item, args = None, kwgs = None):
		amnt = item
		args = () if args is None else args
		kwgs = {} if kwgs is None else kwgs

		if isinstance(item, tuple):
			if not (0 < len(item) < 4):
				raise IndexError('item has to be "["amnt[, args[, kwgs]]"]", not ' + str(item))
			amnt, args, kwgs = list(item) + [args, kwgs][len(item) - 1:]
		elif not isinstance(amnt, int):
			raise TypeError('Iter amount has to be an int')
		return repeat(cls(*args, **kwgs), amnt)

class UserObj(MathObj, metaclass=_UserMeta):
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

	def __init__(self, *args, **kwgs):
		__class__.checktype(self)
		super().__init__(*args, **kwgs)


	@staticmethod
	def __init_subclass__(*, is_pymath_userobj = False, **kwgs):
		if not is_pymath_userobj:
			raise TypeError("UserObj's children cannot be subclassed!")

	__slots__ = ()