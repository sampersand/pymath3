from . import logger
from .named_valued_obj import NamedValuedObj
from .user_obj import UserObj
class Variable(NamedValuedObj):
	pass
class UserVariable(UserObj, Variable):
	def __init__(self, name = None, value = None):
		return super().__init__(name = name, value = value)

	def __repr__(self):
		''' Returns the string defined by gen_repr with the varg 'name' and kwarg 'value' '''
		if self.hasname() and self.isknown():
			return '{}({!r}, {!r})'.format(type(self).__qualname__, self.name, self.value)
		elif self.hasname():
			assert not self.isknown()
			return '{}({!r})'.format(type(self).__qualname__, self.name)
		elif self.isknown():
			assert not self.hasname()
			return '{}(value={!r})'.format(type(self).__qualname__, self.value)
		else:
			assert not self.hasname() and not self.isknown()
			return super().__repr__()

