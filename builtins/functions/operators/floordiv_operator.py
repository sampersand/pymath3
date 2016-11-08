from . import NonCommutativeOperator, TrueDivOperator
class FloorDivOperator(NonCommutativeOperator): # 'x // y'.
	NAME = '//'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a // b, args))

	_weed_out = TrueDivOperator._weed_out
