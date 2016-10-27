from .math_obj import MathObj
from .user_obj import UserObj
class Constant(MathObj):
	pass
class UserConstant(UserObj, Constant):
	pass