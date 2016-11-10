from . import NonCommutativeOperator, MulOperator, reduce
def _gen_iter(a):
	try:
		return iter(a)
	except TypeError:
		return a,
class TrueDivOperator(NonCommutativeOperator): # 'x / y'.
	NAME = '/'

	@staticmethod
	def BASE_FUNC(l, r):
		return l / r

	def _format_weed_out(self, args, fancy):
		if any(arg.hasvalue() and arg.value == 0 for arg in args[1:]):
			raise ZeroDivisionError('One of the denominators is zero: {}'.format(args))
		yield args[0]
		if args[0].hasvalue() and args[0].value == 0:
			return
		yield from (x for x in args[1:] if not x.hasvalue() or x.value != 1)

	def deriv_function(self, num, denom, *, du):
		if num.isconst(du): #shortcut
			return -num/(denom**2) * denom.__derive__(du)
		else:
			return (denom * num.__derive__(du) - num * denom.__derive__(du)) / denom ** 2















