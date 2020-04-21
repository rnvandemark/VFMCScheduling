from tkinter import StringVar

from ui.base_page import BasePage
from ui.base_input_page import BaseInputPage
from src.classroom import ClassroomType

class ClassroomInputPage(BaseInputPage):
	
	def __init__(self, *args, **kwargs):
		BaseInputPage.__init__(self, "Classroom", *args, **kwargs)
		
		self.code_var = StringVar(self.input_widgets_frame)
		_, _, code_entry = BasePage.get_labeled_input_field(
			self.input_widgets_frame,
			"Classroom Code",
			"Entry",
			textvariable=self.code_var,
			f_pady=5,
			required=True)
		self.input_widget_descriptors.append((code_entry, self.code_var, ""))
		
		self.type_options = {t.pretty_print():t.value for t in ClassroomType}
		type_options_list = list(self.type_options.keys())
		self.type_var = StringVar(self.input_widgets_frame)
		_, _, type_menu = BasePage.get_labeled_input_field(
			self.input_widgets_frame,
			"Classroom Type",
			"OptionMenu",
			self.type_var,
			*type_options_list,
			f_pady=5,
			required=True)
		self.input_widget_descriptors.append((type_menu, self.type_var, type_options_list[0]))
		
		self.occupancy_var = StringVar(self.input_widgets_frame)
		_, _, occupancy_entry = BasePage.get_labeled_input_field(
			self.input_widgets_frame,
			"Classroom Occupancy",
			"Entry",
			textvariable=self.occupancy_var,
			f_pady=5,
			required=True)
		self.input_widget_descriptors.append((occupancy_entry, self.occupancy_var, ""))
	
	def validate_input(self):
		valid = len(self.code_var.get()) > 0
		
		occ = 0
		if valid:
			try:
				occ = int(self.occupancy_var.get())
			except ValueError:
				pass
			
			valid = occ > 0
		
		return valid
	
	def objectify_input(self):
		return {
			"room_code": self.code_var.get(),
			"room_type": self.type_options[self.type_var.get()],
			"room_occupancy": self.occupancy_var.get()
		}
	
	def deobjectify_element(self, obj):
		self.code_var.set(obj["room_code"])
		self.type_var.set(ClassroomType(obj["room_type"]).pretty_print())
		self.occupancy_var.set(obj["room_occupancy"])
	
	def stringify_element(self, obj):
		return "{0} ({1}, {2})".format(
			obj["room_code"],
			ClassroomType(obj["room_type"]).pretty_print(),
			obj["room_occupancy"]
		)
	
	def refresh_inputs(self):
		pass