from . import UnaryOperator
class PosOperator(UnaryOperator): # '+x'.
	NAME = '+'

	@staticmethod
	def BASE_FUNC(a):
		return +a