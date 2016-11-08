import logging
logger = logging.getLogger(__name__)
from pymath3.builtins.functions.seeded_function import SeededFunction
from pymath3.builtins.functions.seeded_operator import SeededOperator
from pymath3.builtins.functions.unseeded_function import UnseededFunction
from functools import reduce
from pymath3.utils import import_module


from .operator import Operator

from .unary_operator import UnaryOperator
from .multi_operator import MultiOperator

from .commutative_operator import CommutativeOperator
from .non_commutative_operator import NonCommutativeOperator

from .pos_operator import PosOperator
from .neg_operator import NegOperator
from .invert_operator import InvertOperator

from .add_operator import AddOperator
from .sub_operator import SubOperator

from .mul_operator import MulOperator
from .truediv_operator import TrueDivOperator
from .floordiv_operator import FloorDivOperator
from .mod_operator import ModOperator
from .mmul_operator import MMulOperator

from .pow_operator import PowOperator


def setup():
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
	setparens()
	return gen_opers()
operators = setup()






















