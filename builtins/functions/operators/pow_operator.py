from functools import reduce
from . import logger
from . import import_module, NonCommutativeOperator
if __debug__:
	from . import SeededFunction
class PowOperator(NonCommutativeOperator): # 'x ** y'.
	NAME = '**'

	@staticmethod
	def BASE_FUNC(l, r):
		return l ** r

	# @staticmethod
	# def _weed_out(args):
	# 	assert args
	# 	if args[0] in {0, 1}:
	# 		return args[0]
	# 	return [x for x in args if not x.hasvalue() or x.value != 1]


	def deriv_function(self, b, p, *, du, _ln = []):
		'''b**p * lnb * d(p) '''


		consts = (b.isconst(du) << 1) + p.isconst(du) #wheee binary flags
		if consts == 0b11:
			return 0
		elif consts == 0b10:
			if not _ln:
				_ln.append(import_module('pymath3.extensions').ln)
			return (b ** p) * _ln[0](b) * p.__derive__(du)
		elif consts == 0b01:
			return p * b ** (p - 1) * b.__derive__(du)
		else:
			assert consts == 0b00 #aka neither is constant
			raise NotImplementedError

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

	def _format_get_parens(self, args, fancy): #for giggles
		if len(args) == 2 and args[1].hasvalue() and fancy:
			b, p = args
			p = p.value
			assert isinstance(p, (int, float))
			if self._needs_parens(b): argstr = '(%s)' % b
			else: argstr = str(b)
			yield argstr + ''.join(self._construct_pow(p))
		else:
			yield from super()._format_get_parens(args, fancy)


	def _format_condense(self, args, fancy):
		return args


	def _format_weed_out(self, args, fancy):
		i = -1
		while i < len(args) - 1:
			i += 1
			if not args[i].hasvalue():
				continue
			if args[i].value == 1:
				args = args[:i]
				break
			if args[i].value == 0:
				if i == 0:
					args = [args[i]]
				else:
					args = args[:i-1]
					break
		return args

		# yield from (x for x in args[1:] if not x.hasvalue() or x.value != 1)
























