LOGGING_LEVEL = 'DEBUG'
LOGGING_FORMAT = '[{asctime}][{levelname:<5}] {funcName} :: {message}'
LOGGING_STYLE = '{'
import logging
logging.basicConfig(level = LOGGING_LEVEL, format = LOGGING_FORMAT, style = LOGGING_STYLE)

logger = logging.getLogger(__name__)

import .utils
tq = .utils.tq
SystemMeta = .utils.SystemMeta
from .builtins import *
__all__ = [x for x in list(locals()) if x[0] != '_']