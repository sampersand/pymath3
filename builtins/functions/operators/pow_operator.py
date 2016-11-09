from functools import reduce
from . import logger
from . import MultiOperator, import_module, NonCommutativeOperator
if __debug__:
	from . import SeededFunction
class PowOperator(NonCommutativeOperator): # 'x ** y'.
	NAME = '**'
	BASE_FUNC = staticmethod(lambda *args: reduce(lambda a, b: a ** b, args))

	# @staticmethod
	# def _weed_out(args):
	# 	assert args
	# 	if args[0] in {0, 1}:
	# 		return args[0]
	# 	return [x for x in args if not x.hasvalue() or x.value != 1]


	def deriv_function(self, args, du, _ln = []):
		'''b**p * lnb * d(p) '''
		assert isinstance(args, SeededFunction)
		if __debug__:
			logger.debug("can use 'self(*args)', but using 'args' instead as it is a SeededFunction")
		assert len(args) == 2

		b, p = args
		consts = (b.isconst(du) << 1) + p.isconst(du)
		if consts == 0b11:
			return 0
		elif consts == 0b10:
			if not _ln:
				_ln.append(import_module('pymath3.extensions').ln)
			return args * _ln[0](b) * p.__derive__(du)
		elif consts == 0b01:
			return p * b ** (p - 1) * b.__derive__(du)
		else:
			assert consts == 0b00 #aka neither is constant
			raise NotImplementedError


		ab = self(*args)
		lna = _ln[0](args[0])
		db = args[1].__derive__(du)
		return ab + lna + db

	POWS = ['⁰', '¹', '²', '³', '⁴', '⁵', '⁶', '⁷', '⁸', '⁹', '·', '⁺', '⁻']
	@staticmethod
	def _construct_pow(val):
		assert isinstance(val, (int, float))

		val = str(val)
		assert not (set(val) - set('0123456789.-+')), val
		for x in val:
			if x in '0123456789':
				yield PowOperator.POWS[int(x)]
			elif x == '.':
				yield PowOperator.POWS[-3]
			elif x == '-':
				yield PowOperator.POWS[-1]
			elif x == '+':
				yield PowOperator.POWS[-2]

	def _format_get_parens(self, args): #for giggles
		if len(args) == 2 and args[1].hasvalue():
			b, p = args
			p = p.value
			assert isinstance(p, (int, float))
			if self._needs_parens(b): argstr = '(%s)' % b
			else: argstr = str(b)
			yield argstr + ''.join(self._construct_pow(p))
		else:
			yield from super()._format_get_parens(args)


	def _format_condense(self, args):
		return args


	@staticmethod
	def _format_weed_out(args):
		i = 0
		while i < len(args) - 1:
			if args[i].value == 1:
				args = args[:i]
				break
			if args[i].value == 0:
				if i == 0:
					args = [args[i]]
				else:
					args = args[:i-1]
					break
			i += 1
		print([str(x) for x in args])
		return args

		# yield from (x for x in args[1:] if not x.hasvalue() or x.value != 1)
























