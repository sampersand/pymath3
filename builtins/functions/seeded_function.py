from . import scrub, MathObj, ValuedObj
class SeededFunction(ValuedObj):

	def __init__(self, *, base, call_args, **kwgs):
		assert base
		self.base = base
		self.call_args = tuple(map(scrub, call_args))
		assert all(isinstance(arg, MathObj) for arg in self)
		super().__init__(**kwgs)

	def __iter__(self):
		return iter(self.call_args)
	def __len__(self):
		return len(self.call_args)
	def __getitem__(self, item):
		return self.call_args[item]

	base = property('the unseeded base object')
	@base.getter
	def base(self):
		return self._unseeded_base
	@base.setter
	def base(self, value):
		self._unseeded_base = value


	value = ValuedObj.value
	@value.getter
	def value(self):
		return self.base.base(*self)

	def hasvalue(self):
		if __debug__:
			for x in self:
				assert hasattr(x, 'hasvalue')
		return all(a.hasvalue() for a in self) and self.value is not None

	def __str__(self):
		if self.hasvalue():
			return str(self.value)
		if not self.base.hasname():
			name = '<Unnamed Function>'
		else:
			name = self.base.name
		return '{}({})'.format(name, ', '.join(str(x) for x in self))

	def _gen_repr(self, args, kwgs):
		assert 'base' not in kwgs, kwgs
		assert 'call_args' not in kwgs, kwgs
		kwgs['base'] = self.base
		kwgs['call_args'] = self.call_args
		return super()._gen_repr(args, kwgs)