
class PropertyDomain():

	def __init__(self, db_object=None):

		if db_object != None:
			self.key = db_object.term_object._term_key
			self.name = db_object.term_object.term
			self.value = db_object.value
		else:
			self.name = None
			self.value = None
