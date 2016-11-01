from .math_obj import MathObj
class Operable(MathObj):
	def __init__(self, *args, **kwargs):
		''' Instantiates self.

		A warning will be logged if an Operable is attempted to be instanced directly.

		Arguments:
			*args    -- Ignored
			**kwargs -- Ignored
		Returns:
			None
		'''
		if __debug__ and type(self) == Operable:
			logger.warning("Should not instantiate {} directly!".format(type(self).__qualname__))

		super().__init__(*args, **kwargs)


	def _do(self, func, *args):
		from pymath3.builtins.functions import operators
		return operators[func](self, *args)
	def __add__(self, other):
		return self._do('__add__', other)