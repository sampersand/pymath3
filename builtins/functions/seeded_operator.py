from .seeded_function import SeededFunction
class SeededOperator(SeededFunction):
	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		if __debug__:
			from .operator import Operator
			assert isinstance(self.unseeded_base, Operator)
	def __str__(self):
		if self.hasvalue():
			return super().__str__()
		return self.unseeded_base.format(*self)
