from . import logger
class MathObj():
	'''
	Base class for all PyMath Objects.

	If attempting to directly instantiate a ValuedObj, a warning will be logged.
	'''
	def __init__(self, *args, **kwargs):
		''' Instantiates self.

		If attempting to directly instantiate a MathObj, a warning will be logged.

		Arguments:
			**kwargs -- Extra kwargs, will be ignored for this class.
		Returns:
			None
		'''

		if __debug__ and type(self) == MathObj:
			logger.warning("Should not instantiate {} directly!".format(type(self).__qualname__))
		super().__init__(*args, **kwargs)

	def __repr__(self):
		logger.info('math_obj.__repr__ is temporary')
		return str(sorted(set(dir(self)) - set(dir(object()))))

