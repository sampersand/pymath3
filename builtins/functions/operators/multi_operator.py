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
