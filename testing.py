class foo():
	def func1(a, b, c):
		print(a, b, c)

	@classmethod
	def func2(a, b, c):
		print(a, b, c)

	@staticmethod
	def func3(a, b, c):
		print(a, b, c)

from types import MethodType, CodeType
help(CodeType)
f1 = foo.func1
f2 = foo.func2
f3 = foo.func3
f1c = f1.__code__
f2c = f2.__code__
f3c = f3.__code__
# f3v2 = FunctionType(f3c, f3.__globals__, f3.__name__, f3.__defaults__, f3.__closure__)
print(hash(f3v2), hash(f3))
quit()
 # |  function(code, globals[, name[, argdefs[, closure]]])


# assert dir(f1c) == dir(f2c) == dir(f2c)
# for attr in sorted(dir(f1c)):
# 	f1ca = getattr(f1c, attr)
# 	f2ca = getattr(f2c, attr)
# 	f3ca = getattr(f3c, attr)
# 	if f1ca == f2ca == f3ca or '__' in attr:
# 		continue
# 	print('{:20} ({}) {:15} | {:15} | {:15}'.format(*(str(x) for x in
# 		(attr, f1ca == f2ca == f3ca, f1ca, f2ca, f3ca))))
# quit()
# print(dir(f2))
# print(f2.__code__.co_varnames, dir(f2.__code__))
# quit()
# a = MethodType(f2, foo)
# print(a(1, 2, 3))