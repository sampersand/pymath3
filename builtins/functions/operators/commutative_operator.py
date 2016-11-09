from . import MultiOperator, SeededFunction
class CommutativeOperator(MultiOperator):
	_sort_args = staticmethod(lambda args: sorted(args, key = lambda a: not a.hasvalue()))

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

		return sorted(args, key=self._sort_arg)

