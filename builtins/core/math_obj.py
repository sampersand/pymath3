from . import logger, tq
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



	def _gen_repr(self, args, kwargs):
		return args, kwargs

	def __repr__(self):
		args, kwargs = self._gen_repr((), {})
		return '{}({}{}{})'.format(tq(self), 
		    ', '.join(repr(x) for x in args),
			', ' if args and kwargs else '',
			', '.join('{}={}'.format(key, repr(value)) for key, value in kwargs.items())
			)

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














