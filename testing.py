from itertools import permutations, chain
from importlib import import_module
def _setattr(attr, val):
	def capture(e):
		setattr(e, attr, val)
		return e
	return capture	
def _delattr(attr):
	def capture(e):
		delattr(e, attr)
		return e
	return capture
def _setdelattr(attr):
	def capture(e):
		setattr(e, '_old_' + attr, getattr(e, attr))
		delattr(e, attr)
		return e
	return capture
def _delsetattr(attr):
	def capture(e):
		setattr(e, attr, getattr(e, '_old_' + attr))
		delattr(e, '_old_' + attr)
		return e
	return capture

def _test_normal_strs(vars, consts, checkmap):
	assert all(checkmap(vars, str, lambda e: e.name))
	assert all(checkmap(consts, str, lambda e: str(e.value)))

def _test_change_value_strs(vars, consts, checkmap):
	assert all((all(checkmap(vars, str,
	                lambda e: str(e.value), 
	                preproc = _setattr('value', ele),
	                postproc = _delattr('value')))
				for ele in range(1000)
				))
	assert all(checkmap(vars, str, lambda e: e.name))
	assert all(checkmap(consts, str,
	                lambda e: '0', 
	                preproc = _setdelattr('value'),
	                postproc = _delsetattr('value'),
				))
	assert all(checkmap(consts, str, lambda e: str(e.value)))
def _get_multi_operators(pymath3):
	MultiOperator = import_module('pymath3.builtins.functions.operator').MultiOperator
	for oper in import_module('pymath3.builtins.functions.operator').operators.values():
		if isinstance(oper, MultiOperator):
			yield oper
def _test_opers(vars, consts, multi_opers, checkmap, amount):
	opers = chain.from_iterable(permutations(multi_opers, n) for n in range(amount))
	
def test(pymath3):
	var = pymath3.var
	const = pymath3.const
	checkmap = pymath3.utils.checkmap
	## declare constants
	vars = [var(l) for l in 'abcdefghjijklmnopqrstuvwxyz']
	consts = [const(l) for l in (a*0.01 for a in range(1000))]

	_test_normal_strs(vars, consts, checkmap)
	_test_change_value_strs(vars, consts, checkmap)
	multi_operators = tuple(_get_multi_operators(pymath3))
	_test_opers(vars, consts, multi_operators, checkmap, amount = 10)
	print('done')














