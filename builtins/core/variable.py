from . import logger
from .named_valued_obj import NamedValuedObj
from .user_obj import UserObj
class Variable(NamedValuedObj):
	pass
class UserVariable(UserObj, Variable):
	def __init__(self, name = 'Variable.defaults.name', value = 'Variable.defaults.value'):
		'''
		'''
		return super().__init__(name = name, value = value)
	def __repr__(self):
		''' Returns the string defined by gen_repr with the varg 'name' and kwarg 'value' '''
		if self.hasname() and self.isknown():
			return self.gen_repr(self.name, self.value)
		elif self.hasname():
			return self.gen_repr(self.name)
		else:
			return self.gen_repr(value = (self.value, self.defaults.value))

