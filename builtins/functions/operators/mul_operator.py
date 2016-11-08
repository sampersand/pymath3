from . import CommutativeOperator
class MulOperator(CommutativeOperator): # 'x * y'.
	NAME = '*'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a * b, args))

	@staticmethod
	def DERIV_FUNCTION(args, du):
		print(args.call_args[0].isconst(du))
		print(args, du)
	# @staticmethod
	# def _weed_out(args):
	# 	assert len(args) < 2 or (not args[0].hasvalue() or not args[1].hasvalue()), args #shoulda been done in _condense
	# 	if args[0].value == 0:
	# 		return (Constant(value = 0), )
	# 	return (x for x in args if not x.hasvalue() or x.value != 1)

