LOGGING_LEVEL = 'DEBUG'
LOGGING_LEVEL = 'INFO'
LOGGING_FORMAT = '[{asctime}][{levelname:<5}] {funcName} :: {message}'
LOGGING_STYLE = '{'
import logging
logging.basicConfig(level = LOGGING_LEVEL, format = LOGGING_FORMAT, style = LOGGING_STYLE)
logger = logging.getLogger(__name__)




import pymath3.utils as utils
tq = utils.tq
from .builtins import *

SystemMeta = utils.SystemMeta


__all__ = [x for x in list(locals()) if x[0] != '_']