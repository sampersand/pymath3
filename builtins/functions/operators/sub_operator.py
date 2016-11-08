from . import NonCommutativeOperator, AddOperator
from . import SeededOperator
class SubOperator(NonCommutativeOperator): # 'x - y'.
	SPACES = AddOperator.SPACES
	NAME = '-'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a - b, args))

	def _format_get_parens(self, args):
		assert args
		if isinstance(args[0], SeededOperator) and isinstance(args[0].unseeded_base, AddOperator):
			yield str(args[0])
			args = args[1:]
		for arg in args:
			if self._needs_parens(arg):
				yield '(%s)' % arg
			else:
				yield str(arg)

	deriv_function = AddOperator.deriv_function
