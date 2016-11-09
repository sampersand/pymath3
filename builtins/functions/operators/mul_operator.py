from functools import reduce
from itertools import combinations
from . import CommutativeOperator


class MulOperator(CommutativeOperator): # 'x * y'.
	NAME = '*'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a * b, args))

	@staticmethod
	def possibly_expand(arg):
		if hasattr(arg, '__iter__'):
			return iter(arg)
		return arg,
	def deriv_function(self, args, du):
		ret = 0
		for nonderivs in combinations(args, len(args) -1):
			toderive = set(args) - set(nonderivs)
			assert len(toderive) == 1
			ret += self(*nonderivs, *self.possibly_expand(toderive.pop().__derive__(du)))
		return ret

	def _format_weed_out(self, args, fancy):
		if any(arg.hasvalue() and arg.value == 0 for arg in args):
			return (0,)
		return (x for x in args if not x.hasvalue() or x.value != 1)

	def _get_FORMAT_JOINER(self, fancy):
		return '' if fancy else super()._get_FORMAT_JOINER(fancy)















