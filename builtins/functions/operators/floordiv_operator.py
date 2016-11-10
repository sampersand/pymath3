from . import NonCommutativeOperator, TrueDivOperator, reduce
class FloorDivOperator(NonCommutativeOperator): # 'x // y'.
	NAME = '//'

	@staticmethod
	def BASE_FUNC(l, r):
		return l // r

	_format_weed_out = TrueDivOperator._format_weed_out
