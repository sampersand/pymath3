from . import logger
from . import NamedValuedObj
class Variable(NamedValuedObj):
	pass
class UserVariable(Variable):
	def __init__(self, name = Variable.DEFAULT_NAME, value = Variable.DEFAULT_VALUE):
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
			return self.gen_repr(value = (self.value, self.DEFAULT_VALUE))

