from . import BinaryOperator, SeededFunction
class NonCommutativeOperator(BinaryOperator):

	@staticmethod
	def _sort_arg(arg):
		if __debug__:
			from pymath3.builtins.core.valued_obj import ValuedObj
			assert isinstance(arg, ValuedObj)
		if arg.hasvalue():
			return 0
		if isinstance(arg, SeededFunction):
			return 2
		return 1

	def _format_condense(self, args, fancy):
		return [args[0]] + sorted(args[1:], key=self._sort_arg)
