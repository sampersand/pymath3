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
	var = imports.get('var', 'pymath3.builtins.core.variable', 'UserVariable')
	if isinstance(arg, var._allowed_value_types):
		return var(value = arg, **kwargs)

	raise TypeError(type(arg))
