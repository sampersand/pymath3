from . import CommutativeOperator
class ModOperator(CommutativeOperator): # 'x % y'.
	NAME = '%'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a % b, args))
