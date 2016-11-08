class PowOperator(MultiOperator): # 'x ** y'.
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


