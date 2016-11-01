from .math_obj import MathObj
class Operable(MathObj):
	def _do(self, func, *args):
		from pymath3.builtins.functions import operators
		return operators[func](self, *args)
	def __add__(self, other):
		return self._do('__add__', other)