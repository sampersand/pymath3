from . import Operator
class BinaryOperator(Operator):

	def __init__(self, **kwgs):
		super().__init__(**kwgs)
		assert self.arglen == 2, self.arglen

	@Operator.base.getter
	def base(self):
		def capture(l, r):
			assert hasattr(l, 'hasvalue')
			assert hasattr(r, 'hasvalue')
			assert l.hasvalue()
			assert r.hasvalue()
			assert hasattr(l, 'value')
			assert hasattr(r, 'value')
			return type(self).BASE_FUNC(l.value, r.value)
		return capture

	_sort_args = staticmethod(lambda args: args)


	# def _format_done(self, args):
	# 	return '{}{}{}'.format(self.SPACES[0], self.NAME, self.SPACES[1]).join(self._gen_format_args(args))
