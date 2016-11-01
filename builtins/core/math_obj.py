from . import logger
class MathObj():
	'''
	Base class for all PyMath Objects.

	A warning will be logged if a ValuedObj is attempted to be instanced directly.
	'''
	def __init__(self, *args, **kwargs):
		''' Instantiates self.

		A warning will be logged if a MathObj is attempted to be instanced directly.

		Arguments:
			**kwargs -- Extra kwargs, will be ignored for this class.
		Returns:
			None
		'''

		if __debug__ and type(self) == MathObj:
			logger.warning("Should not instantiate {} directly!".format(type(self).__qualname__))
		super().__init__(*args, **kwargs)

	def __repr__(self):
		return '{}()'.format(type(self).__qualname__)