from .unseeded_function import UnseededFunction
class Operator(UnseededFunction):
	def __init__(self, priority, **kwargs):
		self.priority = priority
		super().__init__(**kwargs)

	def format(self, *args):
		ret = self
class AddOperator(Operator):
	def __init__(self):
		super().__init__(priority = 1, name = '+')



def gen_opers():
	ret = {}
	ret['__add__'] = AddOperator()
	return ret