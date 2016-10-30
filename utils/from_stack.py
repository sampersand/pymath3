def from_stack(varname, stack_level):
	frame_info = stack()[stack_level]
	f_locals = frame_info.frame.f_locals

	if varname not in f_locals:
		assert len(frame_info.code_context) == 1, frame_info.code_context # why wouldnt it be?
		raise AttributeError('Cannot find {} at context\n\n{}\n(level = {})'.format(
			varname, frame_info.code_context[0], stack_level))

	return f_locals[varname]
