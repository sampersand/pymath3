import logging
logger = logging.getLogger(__name__)
def tq(obj):
	return type(obj).__qualname__
from .from_stack import from_stack
from .doc_meta import DocMeta, setdoc