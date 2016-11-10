from . import UnaryOperator
class InvertOperator(UnaryOperator): # '~x'.
	NAME = '~'

	@staticmethod
	def BASE_FUNC(a):
		return ~a
