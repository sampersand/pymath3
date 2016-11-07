from . import ValuedObj, scrub, MathObj
class SeededFunction(ValuedObj):
	def __new__(cls, *, unseeded_base, call_args, **kwargs):
		if call_args:
			if isinstance(call_args[0], SeededFunction):
				if call_args[0].unseeded_base is unseeded_base:
					call_args = call_args[0].call_args + call_args[1:]
					return cls(unseeded_base = unseeded_base, call_args = call_args, **kwargs)
		return super().__new__(cls)

	def __init__(self, *, unseeded_base, call_args, **kwargs):
		assert unseeded_base
		self.unseeded_base = unseeded_base
		self.call_args = tuple(map(scrub, call_args))
		assert all(isinstance(arg, MathObj) for arg in self)
		super().__init__(**kwargs)

	def __iter__(self):
		return iter(self.call_args)

	value = ValuedObj.value
	@value.getter
	def value(self):
		return self.unseeded_base.base_func(*self)
	def hasvalue(self):
		if __debug__:
			for x in self:
				assert hasattr(x, 'hasvalue')
		return all(a.hasvalue() for a in self) and self.value is not None

	def __str__(self):
		if self.hasvalue():
			return str(self.value)
		return '{}({})'.format(self.unseeded_base.name, *self)

	def _gen_repr(self, args, kwargs):
		assert 'unseeded_base' not in kwargs, kwargs
		assert 'call_args' not in kwargs, kwargs
		kwargs['unseeded_base'] = self.unseeded_base
		kwargs['call_args'] = self.call_args
		return super()._gen_repr(args, kwargs)