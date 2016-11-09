from . import import_module
from .seeded_function import SeededFunction
class SeededOperator(SeededFunction):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		if __debug__:
			from .operators import Operator
			assert isinstance(self.unseeded_base, Operator)

		if self.call_args:
			self.unseeded_base._collapse_call_args(self)

	def __str__(self):
		if self.hasvalue():
			return super().__str__()
		return self.unseeded_base.format(self)

	def __derive__(self, other):
		return self.unseeded_base.deriv_function(args = self, du = other)












		