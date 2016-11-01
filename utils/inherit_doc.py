def inheritdoc(parent):
	def capture(func):
		assert hasattr(func, '__name__')

		name = func.__name__

		assert hasattr(parent, name)

		func.__doc__ = getattr(parent, name).__doc__
		return func

	return capture