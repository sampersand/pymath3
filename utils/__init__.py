import logging
logger = logging.getLogger(__name__)
def tq(obj):
	return type(obj).__qualname__

from importlib import import_module
from .checkmap import checkmap
from .from_stack import from_stack
from .setdoc import setdoc
from .scrub import scrub
from .system_meta import SystemMeta
