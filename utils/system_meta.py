from . import scrub, import_module, logger, tq
from inspect import stack
Variable = None
MathObj = None
def getVariable():
	global Variable
	Variable = Variable or import_module('pymath3.builtins.core.variable').Variable
	return Variable
def getMathObj():
	global MathObj
	MathObj = MathObj or import_module('pymath3.builtins.core.math_obj').MathObj
	return MathObj

class _system_locals(dict):
	__slots__ = ('__globals__', )
	BUILTIN_OBJNAMES = {'__module__', '__qualname__', '__name__'}

	@classmethod
	def __new__(cls, *a, **kw):
		return super().__new__(cls)

	def __init__(self, d, __globals__):
		super().__init__(d)
		self.__globals__ = __globals__
		super().__setitem__('derive', SystemMeta.derive)
		super().__setitem__('d', super().__getitem__('derive'))
	def __setitem__(self, name, value):
		if name in self:
			if isinstance(self[name], getVariable()):
				self[name].value = value
				return
		if name in self.BUILTIN_OBJNAMES:
			super().__setitem__(name, value)
			return
		if name not in self:
			if 0 and issubclass(type(value), _SystemObjMeta):
				p = value.__parent__
				args, kwgs = value.__init_args__
				if 'name' in kwgs:
					logger.debug("'name' in __init_args__: {}".format(value.__init_args__))
				else:
					kwgs['name'] = name
				value = value.__parent__(*args, **kwgs)
			else:
				if value is None:
					value = getVariable()()
				value = scrub(value)
				if hasattr(value, 'hasname') and not value.hasname():
					value.name = name
		super().__setitem__(name, value)

	def __getitem__(cls, item):
		# print(item)
		if item in cls.__globals__:
			return cls.__globals__[item]
		if item in dir(cls.__globals__['__builtins__']):
			return getattr(cls.__globals__['__builtins__'], item)
		if item not in cls:
			cls[item] = cls['var'](name = item)
			# super().__setitem__(item, lambda *args: print(*args))#cls['var'](name = item))
		return super().__getitem__(item)
		# get = super().__getitem__(item)
		# if issubclass(type(get), _SystemObjMeta):
			# return get.__new_instance__()
		# return get
# class _SystemObjMeta(type):
# 	def __new__(cls, *args, **kwargs):
# 		ret = super().__new__(cls, *args, **kwargs)
# 		ret.__init_args__ = [(), {}]
# 		return ret

# 	def __mul__(cls, val):
# 		if not isinstance(val, int):
# 			return NotImplemented
# 		return (cls.__new_instance__() for a in range(val))

# 	def __rmul__(cls, val):
# 		return cls * val

# 	def __iter__(cls):
# 		raise TypeError("'{}' object is not iterable".format(tq(cls)))

# 	def __getitem__(cls, item):
# 		if not isinstance(item, slice):
# 			raise TypeError('Can only set init args by: "[args]:[kwargs]". not {} ({})'.format(item, type(item)))
# 		if item.start is not None:
# 			cls.__init_args__[0] = item.start
# 		if item.stop is not None:
# 			cls.__init_args__[1] = item.stop
# 		return cls
# 	def __new_instance__(cls):
# 		return cls.__parent__(*cls.__init_args__[0], **cls.__init_args__[1])
class SystemMeta(type):
	'''
	this class is not meant to be taken seriously (for now), and just for me to toy with
	'''
	@staticmethod
	def _get_globals(__globals__, stack_level):
		if __globals__ is not None:
			return __globals__
		frame_info = stack()[stack_level]
		f_globals = frame_info.frame.f_globals
		return f_globals

	@classmethod
	def __prepare__(metacls, name, bases, *, __globals__ = None, globals_stacklevel = -1, **kwgs):
		ret = super().__prepare__(name, bases, **kwgs)
		__globals__ = metacls._get_globals(__globals__, globals_stacklevel)
		# metacls._insert_mathobjs(ret, __globals__)
		ret = _system_locals(ret, __globals__)
		return ret

	@staticmethod
	def derive(fx, dx):
		return fx.__derive__(dx)
	# @classmethod
	# def _insert_mathobjs(metacls, ret, __globals__):
	# 	mathobj = getMathObj()
		# for name, parent in __globals__.items():
		# 	if not isinstance(parent, type):
		# 		continue
		# 	if issubclass(parent, mathobj):
		# 		ret[name] = _SystemObjMeta(name, (), {'__parent__': parent, '__slots__': ()})

# class System(metaclass=SystemMeta):

# 	@staticmethod
# 	def __init_subclass__(*, __globals__, **kwargs):
# 		pass

