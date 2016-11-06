from . import classproperty
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

	@classproperty
	def _space(cls):
		return ' ' if cls.NAME in set('+-') else ''

	@classmethod
	def _possibly_put_parens(cls, o):
		if isinstance(o, SeededOperator): #could only possibly need parens if it was a SeededOperator
			if o.unseeded_base.PRIORITY > cls.PRIORITY:
				return '({})'.format(o)
		return str(o)

	@classmethod
	def format(cls, *args):
		args = (cls._possibly_put_parens(a) for a in args)
		return '{0}{1}{0}'.format(cls._space, cls.NAME).join(args)

	@staticmethod
	def _assert_values(l, r):
		return hasattr(l, 'hasvalue') and hasattr(r, 'hasvalue') and \
			   l.hasvalue() and r.hasvalue() and hasattr(l, 'value') and hasattr(r, 'value')

class AddOperator(BinaryOperator):
	PRIORITY = 3
	NAME = '+'

	@BinaryOperator.base_func.getter
	def base_func(self):
		def capture(l, r):
			assert self._assert_values(l, r)
			return l.value + r.value
		return capture


class AddOperator(BinaryOperator):
	PRIORITY = 3
	NAME = '+'

	@BinaryOperator.base_func.getter
	def base_func(self):
		def capture(l, r):
			assert self._assert_values(l, r)
			return l.value + r.value
		return capture



class MulOperator(BinaryOperator):
	PRIORITY = 2
	NAME = '*'
	@BinaryOperator.base_func.getter
	def base_func(self):
		def capture(l, r):
			assert self._assert_values(l, r)
			return l.value * r.value
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
	ret['__mul__'] = MulOperator()
	return ret
operators = gen_opers()



