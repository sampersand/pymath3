from . import scrub, import_module, logger
Variable = None

def getVariable():
	global Variable
	Variable = Variable or import_module('pymath3.builtins.core.variable').Variable
	return Variable

class _system_locals(dict):

	BUILTIN_OBJNAMES = {'__module__', '__qualname__', '__name__'}

	def __setitem__(self, name, value):
		if name in self and isinstance(self[name], getVariable()):
			self[name].value = value
			return
		if name not in self and name not in self.BUILTIN_OBJNAMES:
			if value is None:
				value = getVariable()(value = value, name = name)
	# else:
	# 	assert prefer_var
	# 	global Variable 
	# 	Variable = Variable or import_module('pymath3.builtins.core.variable').Variable
	# 	if isinstance(arg, Variable._ALLOWED_VALUE_TYPES):
	# 		return Variable(value = arg, **kwgs)


			value = scrub(value, name = name)
		super().__setitem__(name, value)


class SystemMeta(type):
	'''
	this class is not meant to be taken seriously (for now), and just for me to toy with
	'''

	@classmethod
	def __prepare__(metacls, name, bases, **kwgs):
		return _system_locals(super().__prepare__(name, bases, **kwgs))









