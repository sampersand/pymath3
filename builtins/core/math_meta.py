from pymath3.utils import DefaultMeta
from . import logger

class _gen_slots_class():
	__slots__ = ('_slots', )
	def __init__(self, bases):
		self._slots = self._get_slots_from_bases(bases)

	@staticmethod
	def _get_slots_from_bases(bases):
		ret = set()
		for base in bases:
			if not hasattr(base, '__slots__'):
				logger.warning("Base {} doesn't have a '__slots__' attribute! Ignoring it!".format(
					base.__qualname__))
				continue
			assert isinstance(base.__slots__, (set, frozenset)), '{} | {}'.format(base, type(base.__slots__))
			ret |= base.__slots__
		return frozenset(ret)

	def __call__(self, *extra_slots, bases = None):
		slots = self._slots
		if bases != None:
			slots = self._get_slots_from_bases(bases)

		assert isinstance(slots, frozenset) # should always be...

		ret = set(slots)
		ret |= set(extra_slots)
		return frozenset(ret)

class MathMeta(DefaultMeta):
	__slots__ = ()
	@classmethod
	def __prepare__(metacls, name, bases, **kwargs):
		ret = super().__prepare__(name, bases, **kwargs)
		ret['__gen_slots__'] = _gen_slots_class(bases)
		return ret
		








