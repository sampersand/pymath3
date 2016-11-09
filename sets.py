from inspect import stack
class FooMeta(type):
	def __prepare__(self, *args, **kwargs):
		pass
	def __init__(self, *args, **kwargs):
		quit('no')
	def __new__(self, *args, **kwargs):
		quit('no')
	def __init_subclass__(self, *args, **kwargs):
		quit('no')
print(dir(type))
for attr in sorted(set(dir(type) ) - {'__dict__', '__doc__'}):
	try:
		print('{:20}: {}'.format(attr, getattr(type, attr)))
	except AttributeError:
		print('{:20}: {}'.format(attr, 'ERROR'))
class foo(meta=FooMeta):
	raise IndexError()
	# a, b, c = 