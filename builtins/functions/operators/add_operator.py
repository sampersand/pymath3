class AddOperator(CommutativeOperator): # 'x + y'.
	SPACES = (' ', ' ')
	NAME = '+'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a + b, args))

	# @staticmethod
	# def _weed_out(args):
	# 	return (x for x in args if not x.hasvalue() or x.value != 0)
