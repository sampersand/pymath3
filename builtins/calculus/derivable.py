from . import MathObj
class Derivable(MathObj):
	def isconst(self, other):
		raise NotImplementedError
	def __derive__(self, du):
		raise NotImplementedError
