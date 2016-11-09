from copy import copy
from . import ValuedObj
class Integrable(ValuedObj):
	pass
	def __or__(self, other):
		if not hasattr(other, '__getitem__'):
			return NotImplemented
		assert len(other) == 3 
		val = other[0]
		if __debug__:
			from pymath3.builtins.core.variable import Variable
			assert isinstance(val, Variable), type(val)
		assert not val.hasvalue()
		
		val.value = other[1]
		ret1 = self.solid_value
		val.value = other[2]
		ret2 = self.solid_value
		del val.value
		return ret1 - ret2