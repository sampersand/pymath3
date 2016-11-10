from . import BinaryOperator
class MMulOperator(BinaryOperator): # 'x @ y'.
	NAME = '@'

	@staticmethod
	def BASE_FUNC(l, r):
		return l @ r

