from . import NamedValuedObj
class SeededFunction(NamedValuedObj):
	def __init__(self, unseeded_base, base_args, **kwargs):
		self.unseeded_base = unseeded_base
		self.base_args = base_args
		super().__init__(**kwargs)
