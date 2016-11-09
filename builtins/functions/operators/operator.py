from . import logger
from . import UnseededFunction, SeededOperator, SeededFunction

class Operator(UnseededFunction):
	SEEDED_TYPE = SeededOperator
	NAME, BASE_FUNC = None, None
	SPACES = ('', '')
	if __debug__:
		def __init__(self, *args, **kwargs):
			super().__init__(*args, **kwargs)

	@UnseededFunction.name.getter
	def name(self):
		assert self._name is self._DEFAULT_NAME
		return type(self).NAME


	def _collapse_call_args(self, soper):
		logger.info('TODO: fix _collapse_call_args to work with power')
		START = 0 
		from .pow_operator import PowOperator
		if isinstance(self, PowOperator):
			START = -1
		call_args = soper.call_args
		from . import MultiOperator
		if isinstance(call_args[START], SeededFunction) and call_args[START].unseeded_base is soper.unseeded_base\
			and isinstance(call_args[START].unseeded_base, MultiOperator):
				if START == 0:
					call_args = call_args[START].call_args + call_args[1:]
				else:
					assert START == -1, 'only other defined one atm'
					call_args = call_args[:-1] + call_args[START].call_args
		soper.call_args = call_args

	#str functions


	def format(self, args, fancy = True):
		'''
		10 - x - y - 1 - 4 - z - 5 #start
		10 - x - y - 5 - z - 5 #collapse
		0 - x - y - z  #condensed
		-x - y - z  #weed out

		'''
		args = list(args)

		condensed_args = list(self._format_condense(args, fancy))
		collapsed_args = list(self._format_collapse(condensed_args, fancy))
		conjoined_args = list(self._format_conjoin(collapsed_args, fancy))
		weeded_out_args = list(self._format_weed_out(conjoined_args, fancy))
		# print([str(x) for x in args])
		ret = self._format_complete(weeded_out_args, fancy)
		assert isinstance(ret, str), ret
		return ret



	def _format_collapse(self, args, fancy):
		'''
		Turn 
			-(10, 3x, y, 6, 1, z, 5, x)
		Into
			-(10, 3x, y, 5, z, 5, x)
		'''
		i = 0
		while i < len(args) -1: #so doesnt conflict with +1
			if args[i].hasvalue() and args[i+1].hasvalue():
				toins = self(args.pop(i), args.pop(i))
				args = args[:i] + list(toins) + args[i:]
				i+=len(toins)+1

			else:
				i += 1
		return args


	def _format_condense(self, args, fancy):
		'''
		Turn 
			-(10, 3x, y, 5, z, 5, x)
		Into
			-(0, 3x, y, z, x)
		'''
		return args
	
	def _format_weed_out(self, args, fancy):
		'''
		Turn 
			-(0, 3x, y, z, x)
		Into
			-(3x, y, z, x)
		'''
		return args
	
	def _format_conjoin(self, args, fancy):
		'''
		Turn 
			-(3x, y, z, x)
		Into
			-(2x, y, z)
		'''
		return args

	def _get_FORMAT_JOINER(self, fancy):
		return '{0}{2}{1}'

	def _format_complete(self, args, fancy):
		'''
		Turn 
			-(2x, y, z)
		Into
			2x - y - z
		'''

		joiner = self._get_FORMAT_JOINER(fancy).format(*self.SPACES, self.NAME)
		return joiner.join(self._format_get_parens(args, fancy))

	def _format_get_parens(self, args, fancy):
		for arg in args:
			if self._needs_parens(arg):
				yield '(%s)' % arg
			else:
				yield str(arg)


	def _needs_parens(self, other):
		if not isinstance(other, SeededOperator):
			return False
		return type(other.unseeded_base) in self.paren_classes and not other.hasvalue()

	def deriv_function(self, args, du):
		raise NotImplementedError




