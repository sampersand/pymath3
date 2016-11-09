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
			value = scrub(value, name = name, prefer_var = True)
		super().__setitem__(name, value)
	def __getitem__(self, item):
		if item not in self.BUILTIN_OBJNAMES and item not in self and len(item) == 1:
			logger.debug("Making item '{}' into a variable".format(item))
			self[item] = getVariable()._DEFAULT_VALUE
		return super().__getitem__(item)
class SystemMeta(type):
	'''
	this class is not meant to be taken seriously (for now), and just for me to toy with
	'''
	@classmethod
	def __prepare__(metacls, name, bases, **kwargs):
		return _system_locals(super().__prepare__(name, bases, **kwargs))
