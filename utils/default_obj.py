from inspect import stack

def _get_var_from_stack(varname, stack_level):
	frame_info = stack()[stack_level]
	f_locals = frame_info.frame.f_locals

	if varname not in f_locals:
		assert len(frame_info.code_context) == 1
		raise AttributeError('Cannot findvarnameat context\n\n{}\n(level = {})'.format(
			frame_info.code_context[0], stack_level))

	return f_locals[varname]
class _attr_dict(dict):
	def __getattr__(self, attr):
		if attr not in self:
			self.update(_get_var_from_stack('__this_defaults__', -2))
		return self[attr]

class DefaultMeta(type):
	''' A Meta-class that standardizes default values

	To define defaults, a class should define '__this_defaults__' in it's body somewhere; to access
	said defaults, '__defaults__' can be used.
	
	An example is a helpful way to illustrate:

		class Foo(metaclass=DefaultMeta):
			__this_defaults__ = {'spam': 'eggs', 'ham': True}

			def __init__(self, spam = __defaults__.spam, ham = __defaults__.ham):
				...

	By default, '__defaults__' is an empty dict. If the parent classes have the '__defaults__'
	attribute defined, all such '__default__'s are combined together

	Children will also take on all the defaults of their parents.

		class Bar(Foo):
			# __defaults__ is implicitly created from parent classes' __default___'s.
			# in this case, __defaults__ == {'spam': 'eggs', 'ham': True}
			__this_defaults__ = {'toast': 'jam'}
			def __init__(self, spam = __defaults__.spam, toast = __defaults__.toast):
				...

	Note: This also works with annotations!
	'''
	@classmethod
	def __prepare__(metacls, name, bases, **kwargs):
		ret = super().__prepare__(metacls, name, bases, **kwargs)

		__defaults__ = _attr_dict()

		for base in bases:
			if hasattr(base, '__defaults__'):
				__defaults__.update(base.__defaults__)

		ret['__defaults__'] = __defaults__
		ret['__update_defaults__'] = metacls._static__update_defaults__
		return ret

	@staticmethod
	def _static__update_defaults__(__this_defaults__, __defaults__ = None, stack_level = -2):
		if __defaults__ is None:
			__defaults__ = _get_var_from_stack('__defaults__', stack_level)

		__defaults__.update(__this_defaults__)


	def __init__(cls, name, bases, attrs, **kwargs):
		type.__init__(cls, name, bases, attrs, **kwargs)
		if '__repr__' not in attrs:
			cls.__repr__ = DefaultMeta._static__repr__

	@staticmethod
	def _static__repr__(self):
		non_default_values = {}
		for name, default_value in self.__defaults__.items():
			assert hasattr(self, name)
			self_value = getattr(self, name)
			if self_value is not default_value:
				non_default_values[name] = self_value
		return '{}({})'.format(type(self).__qualname__,
			', '.join('{}={!r}'.format(name, value) for name, value in non_default_values.items()))
class Diner(metaclass=DefaultMeta):
	__this_defaults__ = {'spam': 'eggs', 'ham': True}
	__update_defaults__(__this_defaults__)
	
	def __init__(self, spam = __defaults__.spam, ham = __defaults__.ham):
		self.spam = spam
		self.ham = ham

d = Diner(ham = False)
print(repr(d))


















