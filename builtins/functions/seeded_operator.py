import importlib
from .seeded_function import SeededFunction
MultiOperator = None
class SeededOperator(SeededFunction):

	def __new__(cls, *, unseeded_base, call_args, **kwargs):
		if call_args and isinstance(call_args[0], SeededFunction) and \
			call_args[0].unseeded_base is unseeded_base:
			global MultiOperator
			if not MultiOperator:
				MultiOperator = importlib.import_module('.operator', __package__).MultiOperator
			if isinstance(call_args[0], MultiOperator):
				call_args = call_args[0].call_args + call_args[1:]
				return cls(unseeded_base = unseeded_base, call_args = call_args, **kwargs)
		return super().__new__(cls)

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		if __debug__:
			from .operator import Operator
			assert isinstance(self.unseeded_base, Operator)

	def __str__(self):
		if self.hasvalue():
			return super().__str__()
		return self.unseeded_base.format(*self)
	