# from . import logger
class MathObj():
	'''
	Base class for all PyMath Objects.

	A warning will be logged if a MathObj is attempted to be instanced directly.
	'''

	__doc_defaults__ = {
		'__init__': '''
			Instantiates self.

			A warning will be logged if 'type(self) == {ctype}' evaluates to true.

			Arguments:
				*args    -- Ignored{kwonly_args}
				**kwargs -- Ignored
			Returns:
				None
			''',
		'__repr__': '''No doc lol noob
		''',
	}





	def __init__(self, *args, **kwargs):
		if __debug__ and type(self) == MathObj:
			logger.warning("Should not instantiate {} directly!".format(type(self).__qualname__))
		super().__init__(*args, **kwargs)

	def __repr__(self):
		return '{}()'.format(type(self).__qualname__)


