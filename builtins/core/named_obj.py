from . import logger
from .math_obj import MathObj

class NamedObj(MathObj):
	''' Represents an object that can have a name.

	This class is meant to be subclassed, and shouldn't be instanced directly.

	See Constant and Variable for builtin subclasses for this.
	
	If attempting to directly instantiate a NamedObj, a warning will be logged.
	'''

	_default_name = None
	def __init__(self, name = _default_name, **kwargs):
		''' Initializes self with 'name'
		
		If attempting to directly instantiate a NamedObj, a warning will be logged.

		Arguments:
			name    -- The name of this class. (default: None)
			**kwargs -- Extra kwargs, will be ignored for this class.
		'''

		if __debug__ and type(self) == NamedObj:
			logger.warning("Should not instantiate {} directly!".format(type(self).__qualname__))

		super().__init__(**kwargs)
		self.name = name


	name = property(doc = "The name of this class")

	@name.getter
	def name(self):
		return self._name

	@name.setter
	def name(self, val):
		self._name = val

	@name.deleter
	def name(self):
		self._name = self._default_name

	def hasname(self):
		''' Return true if this this class has a name. '''
		return self.name != self._default_name

	def __str__(self):
		''' Returns a string representation of this class.

		Returns:
			str(self.name)    -- If 'self.hasname()' evaluates to True
			super().__str__() -- If 'self.hasname()' doesn't evaluate to True
		'''
		if self.hasname():
			return str(self.name)

		assert __debug__ or not self.hasname()

		return super().__str__()

	def __repr__(self):
		''' Returns the string defined by gen_repr with the kwarg 'name'. '''
		return self.gen_repr(name = (self.name, self._default_name))



__all__ = ('NamedObj', )