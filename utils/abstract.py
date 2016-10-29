# from . import logger
# from typing import Type, Any

# def abstract(cls: Type[Any]) -> Type[Any]:
# 	''' Marks the passed class as abstract.
# 	This does nothing, except set 'cls._isabstract' to True

# 	If 'isinstance(cls, type)' evalutes to False, a warning is logged.

# 	Arguments:
# 		cls -- The class to mark abstract
# 	Returns:
# 		cls
# 	'''
# 	if __debug__ and not isinstance(cls, type):
# 			logger.warning('Attempting to declare a {} abstract'.frmat(cls))
# 	cls._isabstract = True
# 	return cls