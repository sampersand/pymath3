from copy import copy
def checkmap(iterable, func, expected, preproc = False, postproc = False):
	for ele in iterable:
		if preproc:
			ele = preproc(ele)
		yield func(ele) == expected(ele)
		postproc and postproc(ele)
# def checkmap(func,
# 		 iterable,
# 		 check = bool,
# 		 preproc = None,
# 		 comp = None,
# 		 cleanup = False):

# 	if comp == True:
# 		comp = comp_true
# 	elif not comp:
# 		comp = comp_none

# 	if preproc:
# 		iterable = map(preproc, iterable)

# 	if not cleanup:
# 		comp_ = lambda a: comp(check, func, a)
# 		yield from map(comp_, iterable)
# 	for ele in iterable:
# 		yield comp(func, check, ele)
# 		cleanup and cleanup(ele)
# def powerlist(l):
# 	L = len(l)
# 	return ((l[i//L**j%L] for j in range(n)) for n in range(L+1) for i in range(L**n))