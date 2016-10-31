from . import logger, from_stack

class _DefaultDict(dict):
	__slots__ = ('_updated_dicts', '_parent', '_name')

	def __init__(self):
		super().__init__()
		self._updated_dicts = []

	def __set_name__(self, parent, name):
		self._parent = parent
		self._name = name
		return self

	def __getitem__(self, item, stack_level = None):
		if item not in self:
			logger.debug("Item '{}' not in type {}, looking for it in __this_defaults__!".format(
				item, type(self).__qualname__))
			self.update(from_stack('__this_defaults__', stack_level or -2))
		return super().__getitem__(item)


	def update(self, other):
		if not isinstance(other, dict):
			raise TypeError('Cannot update type {} with a non-dict type'.format(type(self)))
		if other in self._updated_dicts:
			logger.debug("Attempted to update {}'s __defaults__ with the dictionary '{}' more than once.".format(
				self._parent, other))
	
		self._updated_dicts.append(other)
		ret = super().update(other)

	def __getattr__(self, attr):
		return self[attr]


def __update_defaults__(this_defaults, defaults = None, stack_level = -1):
	if defaults is None:
		defaults = from_stack('__defaults__', stack_level)

	defaults.update(this_defaults)


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
	attribute defined, all such '__defaults__'s are combined together

	Children will also take on all the defaults of their parents.

		class Bar(Foo):
			# __defaults__ is implicitly created from parent classes' __default___'s.
			# in this case, __defaults__ == {'spam': 'eggs', 'ham': True}
			__this_defaults__ = {'toast': 'jam'}
			def __init__(self, spam = __defaults__.spam, toast = __defaults__.toast):
				...

	The mere declaration of '__this_defaults__' does not ensure that it is added to '__defaults__',
	however there are a few ways to ensure it does.
		1. Explitictly, via the '__update_defaults__' method.
	
			class Car(metaclass=DefaultMeta)
				__this_defaults__ = {'colour': 'red'}
				__update_defaults__(__this_defaults__)
		
		2. Implicitly by either getting an attribute or an item from __defaults__ that isn't defined
			Note: This will cause '__this_defaults__' to be imported regardless of whether or not
				  the item in question exists in '__this_defaults__' or '__defaults__'.

		3. At the end of the class creation, if '__defaults__' isn't used.

	Note: This also works with annotations!
	'''
	
	@classmethod
	def __prepare__(metacls, name, bases, **kwargs):
		ret = super().__prepare__(metacls, name, bases, **kwargs)

		__defaults__ = _DefaultDict()

		for base in bases:
			if hasattr(base, '__defaults__'):
				__defaults__.update(base.__defaults__)

		ret['__defaults__'] = __defaults__
		ret['__update_defaults__'] = __update_defaults__
		return ret
	def __new__(cls, name, bases, attrs, **kwargs):
		# print(cls, name, bases, attrs, kwargs)
		# quit(attrs)
		ret = super().__new__(cls, name, bases, attrs, **kwargs)
		return ret
	def __init__(cls, name, bases, attrs, **kwargs):
		type.__init__(cls, name, bases, attrs, **kwargs)
		if '__repr__' not in attrs:
			cls.__repr__ = DefaultMeta._static__repr__

		assert hasattr(cls, '__defaults__') # Should have been made in __prepare__

		if hasattr(cls, '__this_defaults__') and cls.__this_defaults__ not in cls.__defaults__._updated_dicts:
			cls.__defaults__.update(cls.__this_defaults__)
		
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





