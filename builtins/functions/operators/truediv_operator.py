from . import NonCommutativeOperator
class TrueDivOperator(NonCommutativeOperator): # 'x / y'.
	NAME = '/'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a / b, args))

	@staticmethod
	def _weed_out(args):
		assert args
		return [args[0]] + [x for x in args[1:] if not x.hasvalue() or x.value != 1]

