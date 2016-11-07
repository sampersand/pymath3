class b():
	pass
class a():
	def __new__(self):
		return a(1)
print(type(a()))