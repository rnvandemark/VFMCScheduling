from tkinter import Frame, Entry, StringVar

from ui.base_input_page import BaseInputPage
from src.classroom import ClassroomType

class ClassroomInputPage(BaseInputPage):
	
	def __init__(self, *args, **kwargs):
		BaseInputPage.__init__(self, "Classroom", *args, **kwargs)
		
		self.code_var = StringVar(self.input_widgets_frame)
		_, _, code_entry = BaseInputPage.get_labeled_input_field(
			self.input_widgets_frame,
			"Classroom Code",
			"Entry",
			textvariable=self.code_var,
			required=True)
		self.input_widget_descriptors.append((code_entry, self.code_var, ""))
		
		self.type_options = {t.pretty_print():t.value for t in ClassroomType}
		type_options_list = list(self.type_options.keys())
		self.type_var = StringVar(self.input_widgets_frame)
		_, _, type_entry = BaseInputPage.get_labeled_input_field(
			self.input_widgets_frame,
			"Classroom Type",
			"OptionMenu",
			self.type_var,
			*type_options_list,
			required=True)
		self.input_widget_descriptors.append((type_entry, self.type_var, type_options_list[0]))
	
	def validate_input(self):
		return len(self.code_var.get()) > 0
	
	def objectify_input(self):
		return {
			"room_code": self.code_var.get(),
			"room_type": self.type_options[self.type_var.get()]
		}
	
	def deobjectify_element(self, obj):
		self.code_var.set(obj["room_code"])
		self.type_var.set(ClassroomType(obj["room_type"]).pretty_print())
	
	def stringify_element(self, obj):
		return "%s (%s)" % (obj["room_code"], ClassroomType(obj["room_type"]).pretty_print())
	
	def refresh_inputs(self):
		pass