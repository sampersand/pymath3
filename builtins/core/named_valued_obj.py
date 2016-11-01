from pymath3.utils.inherit_doc import inheritdoc
from . import logger
from .math_obj import MathObj
from .named_obj import NamedObj
from .valued_obj import ValuedObj

class NamedValuedObj(NamedObj, ValuedObj):
	''' Represents an object that can have both a name and a value.

	This class is meant to be subclassed, and shouldn't be instanced directly.

	A warning will be logged if a NamedValuedObj is attempted to be instanced directly.
	'''
	@inheritdoc(MathObj)
	def __init__(self, *args, **kwargs):
		if __debug__ and type(self) == NamedValuedObj:
			logger.warning("Should not instantiate {} directly!".format(type(self).__qualname__))
		super().__init__(*args, **kwargs)


	def __str__(self):
		''' Returns a string representation of this class.

		Returns:
			ValuedObj.__str__(self) -- If 'self.known()' evaluates to True
			NamedObj.__str__(self)  -- If 'self.known()' evaluates to False
		'''
		if self.hasvalue():
			return ValuedObj.__str__(self)

		assert not self.hasvalue()
		assert True #assert super() type is NamedObj

		return super().__str__()


	@inheritdoc(NamedObj)
	def __repr__(self):
		if self.hasname() and self.hasvalue():
			return '{}(name={!r}, value={!r})'.format(type(self).__qualname__, self.name, self.value)
		assert not self.hasname() or not self.hasvalue()
		return super().__repr__()









