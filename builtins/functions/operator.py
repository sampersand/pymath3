from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator
class Operator(UnseededFunction):
	SEEDED_TYPE = SeededOperator

	PRIORITY = None
	NAME = None

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		assert hasattr(type(self), 'PRIORITY') and type(self).PRIORITY is not None

	def format(self, *args):
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

	@property
	def _space(self):
		return ' ' if self.name in set('+-') else ''

	def format(self, l, r):
		return '{0}{1}{2}{1}{3}'.format(l, self._space, self.name, r)

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



