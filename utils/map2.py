from copy import copy
def map2(func, iterable, check = bool, preproc = None, comp = None, cleanup = False):
	if comp == True:
		comp = lambda a, b: a == b
	if preproc:
		iterable = map(preproc, iterable)
	for ele in iterable:
		if comp:
			yield comp(func(ele), check(ele))
		else:
			yield check(func(ele))
		if cleanup:
			cleanup(ele)
