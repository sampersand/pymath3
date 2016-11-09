from . import Operator
class UnaryOperator(Operator):
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
		assert 0, 'todo'
		fargs = self._gen_format_args(args)
		return '{}{}{}{}'.format(self.SPACES[0], self.NAME, self.SPACES[1], next(fargs))
