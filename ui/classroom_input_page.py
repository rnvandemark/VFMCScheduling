from tkinter import Frame, Entry

from ui.base_input_page import BaseInputPage

class ClassroomInputPage(BaseInputPage):
	
	def __init__(self, *args, **kwargs):
		BaseInputPage.__init__(self, "Classroom", *args, **kwargs)
		
		column_frame = Frame(self)
		column_frame.pack(side="right", fill="x", expand=True)
		
		_, entry_code, var_code = BaseInputPage.get_labeled_frame(
			column_frame,
			"Classroom Code",
			"Entry"
		)
		self.input_elements.append((entry_code, var_code, ""))
		
		options_type = ["Standard", "Computer Lab", "Science Lab"]
		_, entry_type, var_type = BaseInputPage.get_labeled_frame(
			column_frame,
			"Classroom Type",
			"OptionMenu",
			*options_type
		)
		self.input_elements.append((entry_type, var_type, options_type[0]))