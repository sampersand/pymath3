from . import NonCommutativeOperator, MulOperator, reduce
class TrueDivOperator(NonCommutativeOperator): # 'x / y'.
	NAME = '/'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a / b, args))


	@staticmethod
	def _format_weed_out(args):
		if any(arg.value == 0 for arg in args[1:]):
			raise ZeroDivisionError('One of the denominators is zero: {}'.format(args))
		yield args[0]
		if args[0].hasvalue() and args[0].value == 0:
			return
		yield from (x for x in args[1:] if not x.hasvalue() or x.value != 1)
