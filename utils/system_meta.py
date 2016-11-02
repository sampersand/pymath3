import importlib
MathObj = None
class _system_locals(dict):
	BUILTIN_OBJNAMES = {'__module__', '__qualname__'}
	def __setitem__(self, name, value):
		if name not in self and name not in self.BUILTIN_OBJNAMES:
			print('name:', name)
			global MathObj
			if not MathObj:
				MathObj = importlib.import_module('pymath3.builtins.core.math_obj').MathObj
			value = MathObj.scrub(value, name = name)

		super().__setitem__(name, value)
class SystemMeta(type):
	'''
	this class is not meant to be taken seriously (for now), and just for me to toy with
	'''
	@classmethod
	def __prepare__(metacls, name, bases, **kwargs):
		return _system_locals(super().__prepare__(name, bases, **kwargs))
