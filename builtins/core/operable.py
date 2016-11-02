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
		super().__init__(*args, **kwargs)


	def _do(self, func, *args):
		global operators
		if not operators:
			operators = importlib.import_module('pymath3.builtins.functions.operator').operators
		return operators[func](self, *args)

	def __add__(self, other):
		return self._do('__add__', other)






















