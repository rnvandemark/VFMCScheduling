from ui.base_input_page import BaseInputPage

class CourseInputPage(BaseInputPage):
	
	def __init__(self, *args, **kwargs):
		BaseInputPage.__init__(self, "Course", *args, **kwargs)
	
	def validate_input(self):
		raise NotImplementedError()
	
	def objectify_input(self):
		raise NotImplementedError()
	
	def deobjectify_element(self, obj):
		raise NotImplementedError()
	
	def stringify_element(self, obj):
		raise NotImplementedError()