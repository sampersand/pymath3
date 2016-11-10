from . import UnaryOperator
class NegOperator(UnaryOperator): # '-x'.
	NAME = '-'

	@staticmethod
	def BASE_FUNC(a):
		return -a