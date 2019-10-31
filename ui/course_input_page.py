from ui.base_input_page import BaseInputPage

class CourseInputPage(BaseInputPage):
	
	def __init__(self, *args, **kwargs):
		BaseInputPage.__init__(self, "Course", *args, **kwargs)
	
	def stringify_element(self):
		raise NotImplementedError()
	
	def write_elements(self):
		raise NotImplementedError()
	
	def parse_elements_from(self, filename):
		raise NotImplementedError()