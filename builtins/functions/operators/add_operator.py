from . import reduce
from . import CommutativeOperator, MulOperator, SeededOperator
class AddOperator(CommutativeOperator): # 'x + y'.
	SPACES = (' ', ' ')
	NAME = '+'

	@staticmethod
	def BASE_FUNC(l, r):
		return l + r

	def deriv_function(self, l, r, *, du):
		return self(l.__derive__(du), r.__derive__(du))

	@staticmethod
	def _format_weed_out(args, fancy):
		for x in args:
			if str(x) == '0': #this is bad
				continue
			yield x
		# return (x for x in args if not x.hasvalue() or x.value != 0)

	@staticmethod
	def _format_conjoin(args, fancy):
		if fancy:
			for arg in args:
				if isinstance(arg, SeededOperator):
					if isinstance(arg.base, MulOperator):
						if len(arg) == 2: # aka only 2*x not 2*x*y, as that's too hard
							pass
		return args