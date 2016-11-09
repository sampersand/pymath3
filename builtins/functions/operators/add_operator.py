from . import reduce
from . import CommutativeOperator
class AddOperator(CommutativeOperator): # 'x + y'.
	SPACES = (' ', ' ')
	NAME = '+'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a + b, args))
	def deriv_function(self, args, du):
		return self(*(e.__derive__(du) for e in args))

	@staticmethod
	def _format_weed_out(args):
		return tuple(x for x in args if not x.hasvalue() or x.value != 0)