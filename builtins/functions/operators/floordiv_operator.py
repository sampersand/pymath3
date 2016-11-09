from . import NonCommutativeOperator, TrueDivOperator, reduce
class FloorDivOperator(NonCommutativeOperator): # 'x // y'.
	NAME = '//'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a // b, args))

	_format_weed_out = TrueDivOperator._format_weed_out
