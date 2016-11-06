from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator
class Operator(UnseededFunction):
	SEEDED_TYPE = SeededOperator

	PRIORITY = None
	NAME = None

	if __debug__:
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)
			assert hasattr(type(self), 'PRIORITY') and type(self).PRIORITY is not None

	@classmethod
	def format(cls, *args):
		if self.arglen:
			pass
		return ''

	@UnseededFunction.name.getter
	def name(self):
		assert self._name is self._DEFAULT_NAME
		return type(self).NAME


class BinaryOperator(Operator):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		assert self.arglen == 2

	@classmethod
	def _space(cls):
		return ' ' if cls.NAME in set('+-') else ''

	@classmethod
	def _possibly_put_parens(cls, o):
		if isinstance(o, SeededOperator): #could only possibly need parens if it was a SeededOperator
			if o.unseeded_base.PRIORITY > cls.PRIORITY:
				return '({})'.format(o)
		return o

	@classmethod
	def format(cls, l, r):
		l = cls._possibly_put_parens(l)
		r = cls._possibly_put_parens(r)
		return '{0}{1}{2}{1}{3}'.format(l, cls._space(), cls.NAME, r)

class AddOperator(BinaryOperator):
	PRIORITY = 3
	NAME = '+'

	@BinaryOperator.base_func.getter
	def base_func(self):
		def adder(l, r):
			assert hasattr(l, 'hasvalue')
			assert hasattr(r, 'hasvalue')
			assert l.hasvalue() and r.hasvalue()
			assert hasattr(l, 'value')
			assert hasattr(r, 'value')
			return l.value + r.value
		return adder

class MulOperator(BinaryOperator):
	PRIORITY = 2
	NAME = '*'
	@BinaryOperator.base_func.getter
	def base_func(self):
		def adder(l, r):
			assert hasattr(l, 'hasvalue')
			assert hasattr(r, 'hasvalue')
			assert l.hasvalue() and r.hasvalue()
			assert hasattr(l, 'value')
			assert hasattr(r, 'value')
			return l.value * r.value
		return adder



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
	ret['__mul__'] = MulOperator()
	return ret
operators = gen_opers()



