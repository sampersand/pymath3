from . import NonCommutativeOperator, MulOperator, reduce
def _gen_iter(a):
	try:
		return iter(a)
	except TypeError:
		return a,
class TrueDivOperator(NonCommutativeOperator): # 'x / y'.
	NAME = '/'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a / b, args))


	def _format_weed_out(self, args, fancy):
		if any(arg.hasvalue() and arg.value == 0 for arg in args[1:]):
			raise ZeroDivisionError('One of the denominators is zero: {}'.format(args))
		yield args[0]
		if args[0].hasvalue() and args[0].value == 0:
			return
		yield from (x for x in args[1:] if not x.hasvalue() or x.value != 1)

	def deriv_function(self, args, du):
		assert len(args) > 1, args
		n = args[0]
		d = args[1] if len(args) == 2 else self(*args[1:])
		if n.isconst(du): #shortcut
			return -n/(d**2) * d.__derive__(du)
		else:
			from . import operators
			mul = operators['__mul__']
			t = mul(d, *_gen_iter(n.__derive__(du)))
			# t = d * n.__derive__(du) - n * d.__derive__(du)
			b = d ** 2
			# print([str(x) for x in t.call_args])
			# print('du', n.__derive__(du).call_args[0])
			return t / b
		return args

		1/x/ln(X)
		1/(xlnx)
		(xlnx)**-1
		-(xlnx)^-2*(lnx + 1)






