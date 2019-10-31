from ui.base_input_page import BaseInputPage

class ProfessorInputPage(BaseInputPage):
	
	def __init__(self, *args, **kwargs):
		BaseInputPage.__init__(self, "Professor", *args, **kwargs)
	
	def stringify_element(self):
		raise NotImplementedError()
	
	def write_elements(self):
		raise NotImplementedError()
	
	def parse_elements_from(self, filename):
		raise NotImplementedError()