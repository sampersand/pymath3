def isa(a,b):
	return isinstance(a,b)
class a():
	def __init_subclass__(self, a = 3):
		pass
	pass
class bmeta(type):
	def __new__(cls, name, bases, attrs, **kwargs):
		print(bases)
		bases = (a, )
		return super().__new__(cls, name, bases, attrs, **kwargs)
b = bmeta('b', (), {}, a = 3)

assert issubclass(type(b), bmeta)