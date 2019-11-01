from tkinter import StringVar
from Pmw import Balloon

from ui.base_input_page import BaseInputPage

class ProfessorInputPage(BaseInputPage):
	
	def __init__(self, *args, **kwargs):
		BaseInputPage.__init__(self, "Professor", *args, **kwargs)
		
		self.first_name_var = StringVar(self.input_widgets_frame)
		_, _, first_name_entry = BaseInputPage.get_labeled_input_field(
			self.input_widgets_frame,
			"First Name",
			"Entry",
			textvariable=self.first_name_var,
			required=True)
		self.input_widget_descriptors.append((first_name_entry, self.first_name_var, ""))
		
		self.middle_name_var = StringVar(self.input_widgets_frame)
		_, _, middle_name_entry = BaseInputPage.get_labeled_input_field(
			self.input_widgets_frame,
			"Middle Name",
			"Entry",
			textvariable=self.middle_name_var,
			required=False)
		self.input_widget_descriptors.append((middle_name_entry, self.middle_name_var, ""))
		
		self.last_name_var = StringVar(self.input_widgets_frame)
		_, _, last_name_entry = BaseInputPage.get_labeled_input_field(
			self.input_widgets_frame,
			"Last Name",
			"Entry",
			textvariable=self.last_name_var,
			required=True)
		self.input_widget_descriptors.append((last_name_entry, self.last_name_var, ""))
		
		self.depts_var = StringVar(self.input_widgets_frame)
		depts_frame, _, depts_entry = BaseInputPage.get_labeled_input_field(
			self.input_widgets_frame,
			"Departments",
			"Entry",
			textvariable=self.depts_var,
			required=True)
		self.input_widget_descriptors.append((depts_entry, self.depts_var, ""))
		
		Balloon(self).bind(
			depts_frame,
			"""
				Enter a list of comma-seperated department codes that this\n
				 professor can teach in. For example, physics, engineering,\n
				 and math could look like \"PH,ENG,MA\" (Spaces are optional).
			""".replace("\n\t", "").replace("\t", "")
		)
	
	def validate_input(self):
		return all(len(v.get()) > 0 for v in [self.first_name_var, self.last_name_var, self.depts_var])
	
	def objectify_input(self):
		return {
			"first_name": self.first_name_var.get(),
			"middle_name": self.middle_name_var.get(),
			"last_name": self.last_name_var.get(),
			"departments": [d.strip() for d in self.depts_var.get().split(",")]
		}
	
	def deobjectify_element(self, obj):
		self.first_name_var.set(obj["first_name"])
		self.middle_name_var.set(obj["middle_name"])
		self.last_name_var.set(obj["last_name"])
		self.depts_var.set(",".join(obj["departments"]))
	
	def stringify_element(self, obj):
		middle_name = obj["middle_name"]
		return "{0}, {1} {2}({3})".format(
			obj["last_name"],
			obj["first_name"],
			"%s " % middle_name if middle_name else "",
			",".join(obj["departments"])
		)
	
	def refresh_inputs(self):
		pass