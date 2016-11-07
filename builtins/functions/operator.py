from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator
class Operator(UnseededFunction):
	SEEDED_TYPE = SeededOperator
	NAME = None

	if __debug__:
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

	@UnseededFunction.name.getter
	def name(self):
		assert self._name is self._DEFAULT_NAME
		return type(self).NAME

	CLASSES_THAT_NEED_PARENS = ()
	SPACES = ('', '')

	@classmethod
	def _needs_parens(cls, ocls):
		assert issubclass(cls, Operator)
		return any(issubclass(ocls, tocheckcls) for tocheckcls in cls.CLASSES_THAT_NEED_PARENS)

	@classmethod
	def _gen_format_args(cls, args):
		for arg in args:
			if isinstance(arg, SeededOperator) and not arg.hasvalue():
				assert isinstance(arg.unseeded_base, Operator)
				if cls._needs_parens(type(arg.unseeded_base)): #only thing that needs parens are SeededOperator
					yield '(' + str(arg) + ')'
					continue
			yield str(arg)

	@classmethod
	def format(cls, *args):
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


	@classmethod
	def format(cls, *args):
		'''
		this entire func is used to make sure things have parens or not
		'''
		return '{}{}{}'.format(cls.SPACES[0], cls.NAME, cls.SPACES[1]).join(cls._gen_format_args(args))

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

	@classmethod
	def format(cls, *args):
		assert len(args) == 1
		fargs = cls._gen_format_args(args)

		return '{}{}{}{}'.format(cls.SPACES[0], cls.NAME, cls.SPACES[1], next(fargs))

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
	return ret
operators = gen_opers()























