from . import logger
from typing import GenericMeta

class PropertyMeta(GenericMeta, ):
	SUFFIXES = {'_getter': 'fget', '_setter':'fset', '_deleter':'fdel', '_doc':'doc'}
	# def __new__(self, *Args):
	# 	quit('a')
	def __init__(cls, name, bases, attributes):
		type.__init__(cls, name, bases, attributes)
		controllers = {}
		for attr_name, attr_value in attributes.items():
			for suffix_find, suffix_replace in PropertyMeta.SUFFIXES.items():
				if attr_name.endswith(suffix_find):
					property_name = attr_name[:-len(suffix_find)]

					if property_name not in controllers:
						controllers[property_name] = {}

					if not callable(attr_value):
						logger.warning("{}'s {} should be callabel, but isnt".format(cls, property_name))
					assert callable(attr_value), attr_value
					delattr(cls, attr_name)

					controllers[property_name][suffix_replace] = attr_value

		for c_name, c_values in controllers.items():
			setattr(cls, c_name, property(**c_values))













