from functools import reduce
from itertools import combinations
from . import CommutativeOperator


class MulOperator(CommutativeOperator): # 'x * y'.
	NAME = '*'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a * b, args))

	def deriv_function(self, args, du):
		ret = None
		for nonderivs in combinations(args, len(args) -1):
			toderive = set(args) - set(nonderivs)
			assert len(toderive) == 1
			res = self(*nonderivs, toderive.pop().__derive__(du))
			if ret is None:
				ret = res
			else:
				ret += res
		return ret

	@staticmethod
	def _format_weed_out(args):
		if any(arg.value == 0 for arg in args):
			return (0,)
		return tuple(x for x in args if not x.hasvalue() or x.value != 1)

	_FORMAT_JOINER = ''















