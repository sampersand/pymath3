class a():
	__slots__ = 'a',
class b(a):
	__slots__ = 'b',
B = b()
B.a = 1
print(B)