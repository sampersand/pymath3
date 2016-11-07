from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator
class Operator(UnseededFunction):
	SEEDED_TYPE = SeededOperator
	NAME = None

	if __debug__:
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

	@classmethod
	def format(cls, *args):
		if self.arglen:
			pass
		return ''

	@UnseededFunction.name.getter
	def name(self):
		assert self._name is self._DEFAULT_NAME
		return type(self).NAME


class UnaryOperator(Operator):
	pass

class BinaryOperator(Operator):
	CLASSES_THAT_NEED_PARENS = ()
	SPACE = ('', '')
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		assert self.arglen == 2

	@classmethod
	def _needs_parens(cls, ocls):
		assert issubclass(cls, Operator)
		return any(issubclass(ocls, tocheckcls) for tocheckcls in cls.CLASSES_THAT_NEED_PARENS)


	@classmethod
	def format(cls, *args):
		'''
		this entire func is used to make sure things have parens or not
		'''
		return '{}{}{}'.format(cls.SPACE[0], cls.NAME, cls.SPACE[1]).join(cls._gen_format_args(args))

	@classmethod
	def _gen_format_args(cls, args):
		for arg in args:
			if isinstance(arg, SeededOperator) and not arg.hasvalue():
				assert isinstance(arg.unseeded_base, Operator)
				if cls._needs_parens(type(arg.unseeded_base)): #only thing that needs parens are SeededOperator
					yield '(' + str(arg) + ')'
					continue
			yield str(arg)

	@staticmethod
	def _assert_values(l, r):
		return hasattr(l, 'hasvalue') and hasattr(r, 'hasvalue') and \
			   l.hasvalue() and r.hasvalue() and hasattr(l, 'value') and hasattr(r, 'value')


	@Operator.base_func.getter
	def base_func(self):
		def capture(l, r):
			assert self._assert_values(l, r)
			return type(self).BASE_FUNC(l.value, r.value)
		return capture

class AddOperator(BinaryOperator):
	''' Operator representing the mathematical operation 'x + y'. '''
	CLASSES_THAT_NEED_PARENS = ()
	SPACE = (' ', ' ')
	NAME = '+'
	BASE_FUNC = lambda a, b: a + b

class SubOperator(AddOperator):
	''' Operator representing the mathematical operation 'x - y'. '''

	NAME = '-'
	BASE_FUNC = lambda a, b: a + b

class MulOperator(BinaryOperator):
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

class PowOperator(BinaryOperator):
	''' Operator representing the mathematical operation 'x ** y'. '''
	CLASSES_THAT_NEED_PARENS = (AddOperator, MulOperator, UnaryOperator)
	SPACE = (' ', ' ')
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
	return ret
operators = gen_opers()























