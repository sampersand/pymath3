from . import UnaryOperator
class InvertOperator(UnaryOperator): # '~x'.
	NAME = '~'
	BASE_FUNC = staticmethod(lambda a: ~a)
