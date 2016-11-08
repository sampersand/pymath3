class listoper():
	@property
	def powerlist(self):
		L = len(self)
		return ((self[i//L**j%L] for j in range(n)) for n in range(L+1) for i in range(L**n))
		# return self.sublists(len(self)+1)

	def sublists(self, n):
		for n in range(n):
			yield from self.nlist(n)

	def nlist(self, n):
		L = len(self)
		return ((self[i//L**j%L] for j in range(n)) for i in range(L**n))
		# for i in range(L**n):
		# 	yield 
	# @property
	# def powerset(self):
	# 	L = len(self)
	# 	for n in range(L + 1):
	# 		for i in range(L**n):
	# 			for j in range(n):
	# 				ret.add(self[i//L**j%L])
	# 			yield ret
class set2(listoper, list):
	pass
from time import time
from asyncio import get_event_loop, ensure_future

# def powerset(l):
# 	return subsets(l, len(l))

# async def nset(l, n):
# 	L = len(l)
# 	for i in range(L**n):
# 		yield (l[i//L**j%L] for j in range(n))
		
# async def subsets(l, n):
# 	L = len(l)
# 	for n in range(n):
# 		async for a in nset(l, n):
# 			yield a

async def foo():
	t = time()
	quit([list(x) for x in set2('ab').powerlist])
	for x in set2('abc').powerset:
		list(x)
	return time() - t

AMOUNT = 10000
loop = get_event_loop()
print(sum(loop.run_until_complete(foo()) for x in range(AMOUNT)) / AMOUNT)
