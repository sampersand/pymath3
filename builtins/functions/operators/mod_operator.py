from . import CommutativeOperator
class ModOperator(CommutativeOperator): # 'x % y'.
	NAME = '%'

	@staticmethod
	def BASE_FUNC(l, r):
		return l % r
