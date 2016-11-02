from .unseeded_function import UnseededFunction
from .seeded_operator import SeededOperator
class Operator(UnseededFunction):
	seeded_type = SeededOperator
	def __init__(self, priority, **kwargs):
		self.priority = priority
		super().__init__(**kwargs)

	def format(self, *args):
		if self.arglen:
			pass
		print(self.arglen)
		return ''
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
	def __init__(self):
		super().__init__(priority = 1, name = '+')

	base_func = Operator.base_func
	@base_func.getter
	def base_func(self):
		def adder(l, r):
			assert hasattr(l, 'hasvalue')
			assert hasattr(r, 'hasvalue')
			assert l.hasvalue() and r.hasvalue()
			assert hasattr(l, 'value')
			assert hasattr(r, 'value')
			return l.value + r.value
		return adder




def gen_opers():
	ret = {}
	ret['__add__'] = AddOperator()
	return ret
operators = gen_opers()



