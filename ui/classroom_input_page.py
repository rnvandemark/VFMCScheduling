from tkinter import Frame, Entry, StringVar

from ui.base_input_page import BaseInputPage

class ClassroomInputPage(BaseInputPage):
	
	def __init__(self, *args, **kwargs):
		BaseInputPage.__init__(self, "Classroom", *args, **kwargs)
		
		code_var = StringVar(self.input_widgets_frame)
		_, _, code_entry = BaseInputPage.get_labeled_input_field(
			self.input_widgets_frame,
			"Classroom Code",
			"Entry",
			textvariable=code_var
		)
		self.input_elements.append((code_entry, code_var, ""))
		
		type_options = ["Standard", "Computer Lab", "Science Lab"]
		type_var = StringVar(self.input_widgets_frame)
		_, _, type_entry = BaseInputPage.get_labeled_input_field(
			self.input_widgets_frame,
			"Classroom Type",
			"OptionMenu",
			type_var,
			*type_options
		)
		self.input_elements.append((type_entry, type_var, type_options[0]))
	
	def stringify_element(self):
		raise NotImplementedError()
	
	def write_elements(self):
		raise NotImplementedError()
	
	def parse_elements_from(self, filename):
		raise NotImplementedError()