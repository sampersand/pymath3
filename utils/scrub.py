from importlib import import_module
class _importdict(dict):
	def get(self, item, module, module_attr):
		if item not in self:
			self[item] = getattr(import_module(module), module_attr)
		return self[item]
def scrub(arg, *, imports = _importdict(), **kwargs): # this is _not_ exhaustive
	MathObj = imports.get('MathObj', 'pymath3.builtins.core.math_obj', 'MathObj')
	if isinstance(arg, MathObj):
		return arg
	Constant = imports.get('Constant', 'pymath3.builtins.core.constant', 'Constant')
	if isinstance(arg, Constant._ALLOWED_VALUE_TYPES):
		return Constant(value = arg, **kwargs)

	raise TypeError(type(arg))
