from . import import_module
from .seeded_function import SeededFunction
MultiOperator = None
class SeededOperator(SeededFunction):

	def __init__(self, **kwargs):
		super().__init__(**kwargs)
		if __debug__:
			from .operator import Operator
			assert isinstance(self.unseeded_base, Operator)
		if self.call_args:
			START = self.unseeded_base._START_END
			if isinstance(self.call_args[START], SeededFunction) and self.call_args[START].unseeded_base is self.unseeded_base:
				global MultiOperator
				if not MultiOperator:
					MultiOperator = import_module('.operator', __package__).MultiOperator
				if isinstance(self.call_args[START].unseeded_base, MultiOperator):
					if START == 0:
						self.call_args = self.call_args[START].call_args + self.call_args[1:]
					else:
						assert START == -1, 'only other defined one atm'
						self.call_args = self.call_args[:-1] + self.call_args[START].call_args

	def __str__(self):
		if self.hasvalue():
			return super().__str__()
		return self.unseeded_base.format(self)
	