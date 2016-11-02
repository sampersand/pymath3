LOGGING_LEVEL = 'DEBUG'
LOGGING_FORMAT = '[{asctime}][{levelname:<5}] {funcName} :: {message}'
LOGGING_STYLE = '{'
import logging
logging.basicConfig(level = LOGGING_LEVEL, format = LOGGING_FORMAT, style = LOGGING_STYLE)

logger = logging.getLogger(__name__)

from utils.default_meta import *
class spam(metaclass=NestedDefaultMeta):
	__class_defaults__ = {
		'attr1': 1,
		'attr2': 2,
	}
	def foo():
		pass

print(spam.__defaults__)
spam.__defaults__.__class_defaults__ = 1


spam.__class_defaults__ = 3

