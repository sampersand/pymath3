class NegOperator(UnaryOperator): # '-x'.
	NAME = '-'
	BASE_FUNC = staticmethod(lambda a: -a)

