import logging
logger = logging.getLogger(__name__)

from pymath3.utils import scrub, import_module, tq

from pymath3.builtins.core.user_obj import UserObj
from pymath3.builtins.core.named_obj import NamedObj
from pymath3.builtins.core.valued_obj import ValuedObj
from pymath3.builtins.core.math_obj import MathObj
from pymath3.builtins.core.constant import Constant

from .unseeded_function import UserUnseededFunction; func = UserUnseededFunction

__all__ = ('func', )