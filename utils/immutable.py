class immutable():
	_default_lock = False
	def __init__(self, *args, locked = None, **kwargs):
		if locked == None:
			locked = self._default_lock
		self._locked = locked
		super().__init__(*args, **kwargs)

	@property
	def locked(self):
		return self._locked

	def acquire(self):
		assert not self.locked
		self._locked = True

	def assert_unlocked(self):
		if self.locked:
			raise TypeError("Cannot modify items/attributes in {}".format(type(self).__name__))

	@classmethod
	def __init_subclass__(cls, lock = None):
		if lock != None:
			cls._default_lock = lock





