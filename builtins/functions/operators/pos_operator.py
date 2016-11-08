from . import UnaryOperator
class PosOperator(UnaryOperator): # '+x'.
	NAME = '+'
	BASE_FUNC = staticmethod(lambda a: +a)

