import importlib
from .math_obj import MathObj
operators = None #will be 'lazily' imported
class Operable(MathObj):
	''' A class representing an operable object, such as a number or function.

	This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
	warning will be logged.
	'''

	def __init__(self, *args, **kwargs):
		''' Instantiates self.

		This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
		warning will be logged.

		Arguments:
			*args    -- Ignored
			**kwargs -- Ignored
		Returns:
			None
		'''

		__class__.checktype(self)
		super().__init__(**kwargs)


	def _do(self, func, *args):
		global operators
		if not operators:
			operators = importlib.import_module('pymath3.builtins.functions.operator').operators
		return operators[func](self, *args)

	def __add__(self, other): return self._do('__add__', other)
	def __sub__(self, other): return self._do('__sub__', other)
	def __mul__(self, other): return self._do('__mul__', other)
	def __truediv__(self, other): return self._do('__truediv__', other)
	def __floordiv__(self, other): return self._do('__floordiv__', other)
	def __pow__(self, other): return self._do('__pow__', other)
	def __mod__(self, other): return self._do('__mod__', other)

	def __radd__(self, other): return self._do('__radd__', other)
	def __rsub__(self, other): return self._do('__rsub__', other)
	def __rmul__(self, other): return self._do('__rmul__', other)
	def __rtruediv__(self, other): return self._do('__rtruediv__', other)
	def __rfloordiv__(self, other): return self._do('__rfloordiv__', other)
	def __rpow__(self, other): return self._do('__rpow__', other)
	def __rmod__(self, other): return self._do('__rmod__', other)




























