from functools import reduce

from . import Constant, logger
from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator
from .seeded_function import SeededFunction

# 8: <, <=, >, >=, !=, ==
# 7: |
# 6: ^
# 5: &
# 4: <<, >>
# 3: +, -
# 2: *, @, /, //, %
# 1: +x, -x, ~x
# 0: **


# class ROperator(Operator):
# 	__slots__ = ('_oper', )

# 	def __init__(self, *, oper):
# 		self._oper = oper

# 	def __getattr__(self, attr):
# 		return self._oper._base_func
# 		return getattr(self._oper, attr)

# 	def format(self, *args):
# 		return self._oper.format(*reversed(args))

# 	@Operator.base_func.getter
# 	def base_func(self):
# 		def capture(*args):
# 			assert hasattr(l, 'hasvalue')
# 			assert hasattr(r, 'hasvalue')
# 			assert l.hasvalue()
# 			assert r.hasvalue()
# 			assert hasattr(l, 'value')
# 			assert hasattr(r, 'value')
# 			return type(self._oper).BASE_FUNC(r.value, l.value)
# 		return capture


def setparens():
	add = AddOperator
	sub = SubOperator
	mul = MulOperator
	mmul = MMulOperator
	mod = ModOperator
	truediv = TrueDivOperator
	floordiv = FloorDivOperator
	unary = UnaryOperator
	neg = NegOperator
	pos = PosOperator
	invert = InvertOperator
	pow = PowOperator

	add.paren_classes = set()
	sub.paren_classes = {add, sub}
	mul.paren_classes = {mmul, mod} | sub.paren_classes
	mmul.paren_classes = {mul, mod} | sub.paren_classes #idk about this
	mod.paren_classes = {mul, mmul} | sub.paren_classes
	truediv.paren_classes = {mod, mmul, mul, truediv, floordiv} | sub.paren_classes
	floordiv.paren_classes = truediv.paren_classes
	unary.paren_classes = truediv.paren_classes | {unary}
	pow.paren_classes = unary.paren_classes | {pow}
setparens()


def gen_opers():
	ret = {}
	ret['__add__'] = AddOperator()
	ret['__sub__'] = SubOperator()
	ret['__mul__'] = MulOperator()
	ret['__truediv__'] = TrueDivOperator()
	ret['__floordiv__'] = FloorDivOperator()
	ret['__pow__'] = PowOperator()
	ret['__mod__'] = ModOperator()

	ret['__neg__'] = NegOperator()
	ret['__pos__'] = PosOperator()
	ret['__invert__'] = InvertOperator()

	# ret['__radd__'] = ROperator(oper = ret['__add__'])
	# ret['__rsub__'] = ROperator(oper = ret['__sub__'])
	# ret['__rmul__'] = ROperator(oper = ret['__mul__'])
	# ret['__rtruediv__'] = ROperator(oper = ret['__truediv__'])
	# ret['__rfloordiv__'] = ROperator(oper = ret['__floordiv__'])
	# ret['__rpow__'] = ROperator(oper = ret['__pow__'])
	# ret['__rmod__'] = ROperator(oper = ret['__mod__'])

	return ret
operators = gen_opers()























