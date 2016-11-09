from . import logger
from . import UnseededFunction, SeededOperator, SeededFunction

class Operator(UnseededFunction):
	SEEDED_TYPE = SeededOperator
	NAME, BASE_FUNC = None, None
	SPACES = ('', '')
	if __debug__:
		def __init__(self, *args, **kwgs):
			super().__init__(*args, **kwgs)

	@UnseededFunction.name.getter
	def name(self):
		assert self._name is self._DEFAULT_NAME
		return type(self).NAME


	def _collapse_call_args(self, soper):
		START = 0 
		from .pow_operator import PowOperator
		if isinstance(self, PowOperator):
			START = -1
		call_args = soper.call_args
		from . import MultiOperator
		if isinstance(call_args[START], SeededFunction) and call_args[START].base is soper.base\
			and isinstance(call_args[START].base, MultiOperator):
				if START == 0:
					call_args = call_args[START].call_args + call_args[1:]
				else:
					assert START == -1, 'only other defined one atm'
					call_args = call_args[:-1] + call_args[START].call_args
		soper.call_args = call_args

	#str functions


	def format(self, args, fancy = True):
		'''
		-(10, 3x, y, 4, 1, z, 5, x)
		-(10, 4, 1, 5, 3x, y, z, x)
		-(0, 3x, y, z, x)
		-(3x, y, z, x)
		-(2x, y, z)
		2x - y - z
		'''
		args = list(args)

		condensed_args = list(self._format_condense(args, fancy))
		collapsed_args = list(self._format_collapse(condensed_args, fancy))
		conjoined_args = list(self._format_conjoin(collapsed_args, fancy))
		weeded_out_args = list(self._format_weed_out(conjoined_args, fancy))
		ret = self._format_complete(weeded_out_args, fancy)
		assert isinstance(ret, str), ret
		return ret



	def _format_condense(self, args, fancy):
		'''
		Turn 
			-(10, 3x, y, 4, 1, z, 5, x)
		Into
			-(10, 4, 1, 5, 3x, y, z, x)
		'''
		return args

	
	def _format_collapse(self, args, fancy):
		'''
		Turn 
			-(10, 4, 1, 5, 3x, y, z, x)
		Into
			-(0, 3x, y, z, x)
		'''
		i = 0
		while i < len(args) -1: #so doesnt conflict with +1
			if args[i].hasvalue() and args[i+1].hasvalue():
				toins = self(args.pop(i), args.pop(i))
				assert toins.hasvalue() #we're collapsing constants... they have to have a value
				args.insert(i, toins)
			else:
				i += 1
		return args


	
	def _format_weed_out(self, args, fancy):
		'''
		Turn 
			-(0, 3x, y, z, x)
		Into
			-(-3x, y, z, x)
		'''
		return args
	
	def _format_conjoin(self, args, fancy):
		'''
		Turn 
			-(-3x, y, z, x)
		Into
			-(-4x, y, z)
		'''
		return args

	def _get_FORMAT_JOINER(self, fancy):
		return '{0}{2}{1}'

	def _format_complete(self, args, fancy):
		'''
		Turn 
			-(-4x, y, z)
		Into
			-4x - y - z
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
		if type(other.base) in self.paren_classes:
			if other.hasvalue():
				return False
			if set(str(other)) - set('0123456789-+.'):
				return True
			return False
		return False

	def deriv_function(self, args, du):
		raise NotImplementedError




