from typing import GenericMeta

class _default_dict(dict):
	def __getattr__(self, attr):
		return self[attr]

class DefaultMeta(type):
	def __init__(cls, name, bases, attributes):
		if 'defaults' in attributes:
			attributes['defaults'] = _default_dict(attributes['defaults'])
		type.__init__(cls, name, bases, attributes)
	# @staticmethod
	# def _getdefaults(bases):
	# 	defaults = _default_dict()
	# 	for base in bases:
	# 		if hasattr(base, 'defaults'):
	# 			defaults.update(base.defaults)
	# 	return defaults		
	# def __init__(cls, name, bases, attributes):
	# 	type.__init__(cls, name, bases, attributes)

	# 	cls.defaults = cls._getdefaults(bases)

	# 	for attr_name, attr_value in attributes.items():
	# 		if attr_name.lower().startswith('default_'):
	# 			cls.defaults[attr_name[len('default_'):].lower()] = attr_value
	# 			delattr(cls, attr_name)









