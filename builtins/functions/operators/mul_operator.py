from functools import reduce
from itertools import combinations
from . import CommutativeOperator


class MulOperator(CommutativeOperator): # 'x * y'.
	NAME = '*'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a * b, args))

	def DERIV_FUNCTION(self, *args, du):
		ret = None
		for nonderivs in combinations(args, len(args) -1):
				
			assert len(set(args) - set(nonderivs)) == 1
			res = self(*nonderivs, (set(args) - set(nonderivs)).pop().__derive__(du))
			if ret is None:
				ret = res
			else:
				ret += res
		return ret
		# return AddOperator(*self._DERIV_FUNCITON(args, du))

	# @staticmethod
	# def _weed_out(args):
	# 	assert len(args) < 2 or (not args[0].hasvalue() or not args[1].hasvalue()), args #shoulda been done in _condense
	# 	if args[0].value == 0:
	# 		return (Constant(value = 0), )
	# 	return (x for x in args if not x.hasvalue() or x.value != 1)

