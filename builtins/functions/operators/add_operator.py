from . import reduce
from . import CommutativeOperator, MulOperator, SeededOperator
class AddOperator(CommutativeOperator): # 'x + y'.
	SPACES = (' ', ' ')
	NAME = '+'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a + b, args))
	def deriv_function(self, args, du):
		return self(*(e.__derive__(du) for e in args))

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
					if isinstance(arg.unseeded_base, MulOperator):
						if len(arg) == 2: # aka only 2*x not 2*x*y, as that's too hard
							pass
		return args
			# if 