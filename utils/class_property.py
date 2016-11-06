class classproperty(object):
	'''
	from http://stackoverflow.com/questions/5189699/how-can-i-make-a-class-property-in-python#5191224
	'''
	def __init__(self, val):
		self.val = val
	def __get__(self, instance, parent):
		return self.val(parent)
