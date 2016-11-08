class CommutativeOperator(MultiOperator):
	_sort_args = staticmethod(lambda args: sorted(args, key = lambda a: not a.hasvalue()))

	# def _condense(self, args):
	# 	pos = 0
	# 	while pos < len(args) and args[pos].hasvalue():
	# 		pos += 1
	# 	if pos > 1:
	# 		return [self(*args[0:pos])] + list(args[pos:])
	# 	return args
