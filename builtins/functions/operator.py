from functools import reduce

from . import Constant, logger
from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator
from .seeded_function import SeededFunction
class Operator(UnseededFunction):
	SEEDED_TYPE = SeededOperator
	NAME, BASE_FUNC = None, None

	if __debug__:
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

	@UnseededFunction.name.getter
	def name(self):
		assert self._name is self._DEFAULT_NAME
		return type(self).NAME


	def _collapse_call_args(self, soper):
		logger.info('TODO: fix _collapse_call_args to work with power')
		START = 0
		call_args = soper.call_args

		if isinstance(call_args[START], SeededFunction) and call_args[START].unseeded_base is soper.unseeded_base\
			and isinstance(call_args[START].unseeded_base, MultiOperator):
				if START == 0:
					call_args = call_args[START].call_args + call_args[1:]
				else:
					assert START == -1, 'only other defined one atm'
					call_args = call_args[:-1] + call_args[START].call_args


	#str functions


	def format(self, args):
		'''
		10 - x - y - 1 - 4 - z - 5 #start
		10 - x - y - 5 - z - 5 #collapse
		0 - x - y - z  #condensed
		-x - y - z  #weed out

		'''
		args = tuple(args)

		collapsed_args = self._format_collapse(args)
		condensed_args = self._format_condense(collapsed_args)
		weeded_out_args = self._format_weed_out(condensed_args)
		ret = self._format_complete(weeded_out_args)
		assert isinstance(ret, str), ret
		return ret



	def _format_collapse(self, args):
		'''
		Turn 
			-(10, x, y, 1, 4, z, 5)
		Into
			-(10, x, y, 5, z, 5)
		'''
		return args

	def _format_condense(self, args):
		'''
		Turn 
			-(10, x, y, 5, z, 5)
		Into
			-(0, x, y, z)
		'''
		return args
	
	def _format_weed_out(self, args):
		'''
		Turn 
			-(0, x, y, z)
		Into
			-(x, y, z)
		'''
		return args


	def _format_complete(self, args):
		'''
		Turn 
			-(x, y, z)
		Into
			x - y - z
		'''
		return self.NAME.join(str(arg) for arg in args)




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


class MultiOperator(Operator):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		# assert self.arglen == 2, self.arglen

	@Operator.base_func.getter
	def base_func(self):
		def capture(*args):
			assert all(hasattr(a, 'hasvalue') for a in args), [x for x in args if not hasattr(x, 'hasvalue')]
			assert all(a.hasvalue() for a in args), [x for x in args if not x.hasvalue()]
			assert all(hasattr(a, 'value') for a in args), [x for x in args if not hasattr(a, 'value')]
			return type(self).BASE_FUNC(*(a.value if a.hasvalue() else a for a in args))
		return capture

	_sort_args = staticmethod(lambda args: args)


	# def _format_done(self, args):
	# 	return '{}{}{}'.format(self.SPACES[0], self.NAME, self.SPACES[1]).join(self._gen_format_args(args))

class CommutativeOperator(MultiOperator):
	_sort_args = staticmethod(lambda args: sorted(args, key = lambda a: not a.hasvalue()))

	# def _condense(self, args):
	# 	pos = 0
	# 	while pos < len(args) and args[pos].hasvalue():
	# 		pos += 1
	# 	if pos > 1:
	# 		return [self(*args[0:pos])] + list(args[pos:])
	# 	return args


class AddOperator(CommutativeOperator): # 'x + y'.
	CLASSES_THAT_NEED_PARENS = ()
	SPACES = (' ', ' ')
	NAME = '+'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a + b, args))

	# @staticmethod
	# def _weed_out(args):
	# 	return (x for x in args if not x.hasvalue() or x.value != 0)

class SubOperator(MultiOperator): # 'x - y'.
	CLASSES_THAT_NEED_PARENS = (AddOperator,)
	SPACES = AddOperator.SPACES
	NAME = '-'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a + b, args))

class MulOperator(CommutativeOperator): # 'x * y'.
	CLASSES_THAT_NEED_PARENS = (AddOperator, )
	NAME = '*'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a * b, args))

	# @staticmethod
	# def _weed_out(args):
	# 	assert len(args) < 2 or (not args[0].hasvalue() or not args[1].hasvalue()), args #shoulda been done in _condense
	# 	if args[0].value == 0:
	# 		return (Constant(value = 0), )
	# 	return (x for x in args if not x.hasvalue() or x.value != 1)

class MMulOperator(MultiOperator): # 'x @ y'.

	CLASSES_THAT_NEED_PARENS = MulOperator.CLASSES_THAT_NEED_PARENS
	NAME = '@'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a @ b, args))


class TrueDivOperator(MultiOperator): # 'x / y'.
	CLASSES_THAT_NEED_PARENS = MulOperator.CLASSES_THAT_NEED_PARENS
	NAME = '/'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a / b, args))

	@staticmethod
	def _weed_out(args):
		assert args
		return [args[0]] + [x for x in args[1:] if not x.hasvalue() or x.value != 1]


class FloorDivOperator(MultiOperator): # 'x // y'.
	CLASSES_THAT_NEED_PARENS = MulOperator.CLASSES_THAT_NEED_PARENS
	NAME = '//'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a // b, args))

	_weed_out = TrueDivOperator._weed_out

class ModOperator(MultiOperator): # 'x % y'.

	CLASSES_THAT_NEED_PARENS = MulOperator.CLASSES_THAT_NEED_PARENS
	NAME = '%'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a % b, args))



class UnaryOperator(Operator):
	CLASSES_THAT_NEED_PARENS = (AddOperator, MulOperator)
	SPACES = ('', '')

	@Operator.base_func.getter
	def base_func(self):
		def capture(l):
			assert hasattr(l, 'hasvalue')
			assert l.hasvalue(), l
			assert hasattr(l, 'value')
			return type(self).BASE_FUNC(l.value)
		return capture


	def format(self, arg):
		return self._format_done(arg)

	def _format_done(self, args):
		fargs = self._gen_format_args(args)
		return '{}{}{}{}'.format(self.SPACES[0], self.NAME, self.SPACES[1], next(fargs))

class NegOperator(UnaryOperator): # '-x'.
	NAME = '-'
	BASE_FUNC = staticmethod(lambda a: -a)


class PosOperator(UnaryOperator): # '+x'.
	NAME = '+'
	BASE_FUNC = staticmethod(lambda a: +a)


class InvertOperator(UnaryOperator): # '~x'.
	NAME = '~'
	BASE_FUNC = staticmethod(lambda a: ~a)


class PowOperator(MultiOperator): # 'x ** y'.
	CLASSES_THAT_NEED_PARENS = (AddOperator, MulOperator, UnaryOperator)
	SPACES = (' ', ' ')
	NAME = '**'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a ** b, args))

	def _condense(self, args):
		if len(args) < 2:
			return args
		return args
		# if not args[0].hasvalue():
		# 	pos = 1	
		# 	while pos < len(args) and args[pos].hasvalue():
		# 		pos += 1
		# 	if pos > 2:
		# 		return [args[0]] + [self(*args[1:pos])] + list(args[pos:])
		# 	return args

	@staticmethod
	def _weed_out(args):
		assert args
		if args[0] in {0, 1}:
			return args[0]
		return [x for x in args if not x.hasvalue() or x.value != 1]


class ROperator(Operator):
	__slots__ = ('_oper', )

	def __init__(self, *, oper):
		self._oper = oper

	def __getattr__(self, attr):
		return self._oper._base_func
		return getattr(self._oper, attr)

	def format(self, *args):
		return self._oper.format(*reversed(args))

	@Operator.base_func.getter
	def base_func(self):
		def capture(*args):
			assert hasattr(l, 'hasvalue')
			assert hasattr(r, 'hasvalue')
			assert l.hasvalue()
			assert r.hasvalue()
			assert hasattr(l, 'value')
			assert hasattr(r, 'value')
			return type(self._oper).BASE_FUNC(r.value, l.value)
		return capture

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

	# ret['__radd__'] = ROperator(oper = ret['__add__'])
	# ret['__rsub__'] = ROperator(oper = ret['__sub__'])
	# ret['__rmul__'] = ROperator(oper = ret['__mul__'])
	# ret['__rtruediv__'] = ROperator(oper = ret['__truediv__'])
	# ret['__rfloordiv__'] = ROperator(oper = ret['__floordiv__'])
	# ret['__rpow__'] = ROperator(oper = ret['__pow__'])
	# ret['__rmod__'] = ROperator(oper = ret['__mod__'])

	return ret
operators = gen_opers()























