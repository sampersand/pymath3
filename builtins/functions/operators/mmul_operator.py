class MMulOperator(MultiOperator): # 'x @ y'.

	NAME = '@'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a @ b, args))

