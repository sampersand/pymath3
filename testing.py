# import sys
# sys.path[0] = sys.path[0][:-len('/pymath3')]
# import pymath3
class a():
	def __init__(self, *a, **k):
		k['a'] = 0
		super().__init__(*a)
class b(a):
	def __init__(self, *a, **k):
		k['b'] = 1
		super().__init__(*a, **k)
class c(a):
	def __init__(self, *a, **k):
		k['c'] = 2
		super().__init__(*a, **k)
class d(b, c):
	# def __init__(self, *a, **k):
	1
		# k['d'] = 3
		# super().__init__(*a, **k)

d(1)