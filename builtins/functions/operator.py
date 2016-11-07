from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator
class Operator(UnseededFunction):
	SEEDED_TYPE = SeededOperator

	NAME = None
	CLASSES_THAT_NEED_PARENS = ()
	SPACES = ('', '')
	BASE_FUNC = None

	if __debug__:
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

	@UnseededFunction.name.getter
	def name(self):
		assert self._name is self._DEFAULT_NAME
		return type(self).NAME


	def _needs_parens(self, ocls):
		assert isinstance(self, Operator)
		return any(issubclass(ocls, tocheckcls) for tocheckcls in self.CLASSES_THAT_NEED_PARENS)

	def _gen_format_args(self, args):
		for arg in args:
			if isinstance(arg, SeededOperator) and not arg.hasvalue():
				assert isinstance(arg.unseeded_base, Operator)
				if self._needs_parens(type(arg.unseeded_base)): #only thing that needs parens are SeededOperator
					yield '(' + str(arg) + ')'
					continue
			yield str(arg)

	def format(self, *args):
		raise NotImplementedError

class MultiOperator(Operator):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		assert self.arglen == 2

	@Operator.base_func.getter
	def base_func(self):
		def capture(l, r):
			assert hasattr(l, 'hasvalue')
			assert hasattr(r, 'hasvalue')
			assert l.hasvalue()
			assert r.hasvalue()
			assert hasattr(l, 'value')
			assert hasattr(r, 'value')
			return type(self).BASE_FUNC(l.value, r.value)
		return capture


	def format(self, *args):
		'''
		this entire func is used to make sure things have parens or not
		'''
		return '{}{}{}'.format(self.SPACES[0], self.NAME, self.SPACES[1]).join(self._gen_format_args(args))

class AddOperator(MultiOperator):
	''' Operator representing the mathematical operation 'x + y'. '''
	CLASSES_THAT_NEED_PARENS = ()
	SPACES = (' ', ' ')
	NAME = '+'
	BASE_FUNC = lambda a, b: a + b

class SubOperator(AddOperator):
	''' Operator representing the mathematical operation 'x - y'. '''

	NAME = '-'
	BASE_FUNC = lambda a, b: a + b



class MulOperator(MultiOperator):
	''' Operator representing the mathematical operation 'x * y'. '''
	CLASSES_THAT_NEED_PARENS = (AddOperator, )
	NAME = '*'
	BASE_FUNC = lambda a, b: a * b

class MMulOperator(MulOperator):
	''' Operator representing the mathematical operation 'x @ y'. '''
	NAME = '@'
	BASE_FUNC = lambda a, b: a @ b

class TrueDivOperator(MulOperator):
	''' Operator representing the mathematical operation 'x / y'. '''
	NAME = '/'
	BASE_FUNC = lambda a, b: a / b

class FloorDivOperator(MulOperator):
	''' Operator representing the mathematical operation 'x // y'. '''
	NAME = '//'
	BASE_FUNC = lambda a, b: a // b

class ModOperator(MulOperator):
	''' Operator representing the mathematical operation 'x % y'. '''

	NAME = '%'
	BASE_FUNC = lambda a, b: a % b


class UnaryOperator(Operator):
	CLASSES_THAT_NEED_PARENS = (AddOperator, MulOperator)
	SPACES = ('', '')

	@Operator.base_func.getter
	def base_func(self):
		def capture(l):
			assert hasattr(l, 'hasvalue')
			assert l.hasvalue()
			assert hasattr(l, 'value')
			return type(self).BASE_FUNC(l.value)
		return capture

	def format(self, *args):
		assert len(args) == 1
		fargs = self._gen_format_args(args)

		return '{}{}{}{}'.format(self.SPACES[0], self.NAME, self.SPACES[1], next(fargs))

class NegOperator(UnaryOperator):
	''' Operator representing the mathematical operation '-x'. '''
	NAME = '-'
	BASE_FUNC = lambda a: -a


class PosOperator(UnaryOperator):
	''' Operator representing the mathematical operation '+x'. '''
	NAME = '+'
	BASE_FUNC = lambda a: +a


class InvertOperator(UnaryOperator):
	''' Operator representing the mathematical operation '~x'. '''
	NAME = '~'
	BASE_FUNC = lambda a: ~a


class PowOperator(MultiOperator):
	''' Operator representing the mathematical operation 'x ** y'. '''
	CLASSES_THAT_NEED_PARENS = (AddOperator, MulOperator, UnaryOperator)
	SPACES = (' ', ' ')
	NAME = '**'
	BASE_FUNC = lambda a, b: a ** b

class ROperator(Operator):
	__slots__ = ('_oper', )
	def __init__(self, *, oper):
		self._oper = oper

	def __getattr__(self, attr):
		return getattr(self._oper, attr)

# 8: <, <=, >, >=, !=, ==
# 7: |
# 6: ^
# 5: &
# 4: <<, >>
# 3: +, -
# 2: *, @, /, //, %
# 1: +x, -x, ~x
# 0: **


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

	ret['__radd__'] = ROperator(oper = ret['__add__'])
	return ret
operators = gen_opers()























