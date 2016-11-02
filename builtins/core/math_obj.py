from . import logger
class MathObj():
	'''
	Base class for all PyMath Objects.

	This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
	warning will be logged.
	'''

	def __init__(self, *args, **kwargs):
		'''Initialize self.

		This class is meant to be subclassed, and shouldn't be instanced directly. If attempted, a
		warning will be logged.

		Arguments:
			*args    -- Ignored
			**kwargs -- Ignored
		Returns:
			None
		'''

		__class__.checktype(self)
		super().__init__(*args, **kwargs)

	def __repr__(self):
		return '{}()'.format(type(self).__qualname__)

	@classmethod
	def checktype(cls, self):
		''' Check to see if self.__class__ is equal to cls, and log a warning if they are.

		Normal usage is:

			class spam():
				def foo(self, ...):
					__class__.checktype(self)
		Arguments:
			cls  -- The class to check type(self) against
			self -- the instance who's class will be checked against cls
		Returns:
			False if a warning was logged, true otherwise.
		'''
		if type(self) == cls:
			logger.warning("Should not instantiate {} directly!".format(cls))
			return False
		return True
