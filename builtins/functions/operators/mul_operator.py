from functools import reduce
from itertools import combinations
from . import CommutativeOperator


class MulOperator(CommutativeOperator): # 'x * y'.
	NAME = '*'

	@staticmethod
	def BASE_FUNC(l, r):
		return l * r

	@staticmethod
	def possibly_expand(arg):
		if hasattr(arg, '__iter__'):
			return iter(arg)
		return arg,

	def deriv_function(self, l, r, *, du):
		return l.__derive__(du) * r + l * r.__derive__(du)

	def _format_weed_out(self, args, fancy):
		if any(arg.hasvalue() and arg.value == 0 for arg in args):
			return (0,)
		return (x for x in args if not x.hasvalue() or x.value != 1)

	def _get_FORMAT_JOINER(self, fancy):
		return '' if fancy else super()._get_FORMAT_JOINER(fancy)















