from tkinter import Frame, Checkbutton, StringVar, IntVar

from ui.base_input_page import BaseInputPage
from src.classroom import ClassroomType

class CourseInputPage(BaseInputPage):
	
	def __init__(self, *args, **kwargs):
		BaseInputPage.__init__(self, "Course", *args, **kwargs)
		
		left_frame = Frame(self.input_widgets_frame)
		left_frame.pack(side="left", fill="x", expand=True)
		
		self.name_var = StringVar(left_frame)
		_, _, name_entry = BaseInputPage.get_labeled_input_field(
			left_frame,
			"Course Name",
			"Entry",
			textvariable=self.name_var,
			required=True)
		self.input_widget_descriptors.append((name_entry, self.name_var, ""))
		
		self.dept_code_var = StringVar(left_frame)
		_, _, dept_code_entry = BaseInputPage.get_labeled_input_field(
			left_frame,
			"Department Code",
			"Entry",
			textvariable=self.dept_code_var,
			required=True)
		self.input_widget_descriptors.append((dept_code_entry, self.dept_code_var, ""))
		
		self.course_number_var = StringVar(left_frame)
		_, _, course_number_entry = BaseInputPage.get_labeled_input_field(
			left_frame,
			"Course Number",
			"Entry",
			textvariable=self.course_number_var,
			validate="key",
			validatecommand=(left_frame.register(self.ensure_int), "%S"),
			required=True)
		self.input_widget_descriptors.append((course_number_entry, self.course_number_var, ""))
		
		self.num_credits_var = StringVar(left_frame)
		_, _, num_credits_entry = BaseInputPage.get_labeled_input_field(
			left_frame,
			"Credit Count",
			"Entry",
			textvariable=self.num_credits_var,
			validate="key",
			validatecommand=(left_frame.register(self.ensure_int), "%S"),
			required=True)
		self.input_widget_descriptors.append((num_credits_entry, self.num_credits_var, ""))
		
		self.mins_per_week_var = StringVar(left_frame)
		_, _, mins_per_week_entry = BaseInputPage.get_labeled_input_field(
			left_frame,
			"Minutes/Week",
			"Entry",
			textvariable=self.mins_per_week_var,
			validate="key",
			validatecommand=(left_frame.register(self.ensure_int), "%S"),
			required=True)
		self.input_widget_descriptors.append((mins_per_week_entry, self.mins_per_week_var, ""))
		
		self.num_sections_var = StringVar(left_frame)
		_, _, num_sections_entry = BaseInputPage.get_labeled_input_field(
			left_frame,
			"Section Count",
			"Entry",
			textvariable=self.num_sections_var,
			validate="key",
			validatecommand=(left_frame.register(self.ensure_int), "%S"),
			required=True)
		self.input_widget_descriptors.append((num_sections_entry, self.num_sections_var, ""))
		
		self.room_type_options = {t.pretty_print():t.value for t in ClassroomType}
		self.room_type_options_list = list(self.room_type_options.keys())
		self.room_type_var = StringVar(left_frame)
		_, _, room_type_entry = BaseInputPage.get_labeled_input_field(
			left_frame,
			"Classroom Type",
			"OptionMenu",
			self.room_type_var,
			*self.room_type_options_list,
			required=True)
		self.input_widget_descriptors.append((
			room_type_entry, self.room_type_var, self.room_type_options_list[0]))
		
		right_frame = Frame(self.input_widgets_frame)
		right_frame.pack(side="right", fill="x", expand=True)
		
		self.has_lab_var = IntVar(right_frame)
		_, _, has_lab_checkbtn = BaseInputPage.get_labeled_input_field(
			right_frame,
			"Has a Lab",
			"Checkbutton",
			variable=self.has_lab_var,
			command=self.update_lab_widget_states,
			required=True)
		self.input_widget_descriptors.append((has_lab_checkbtn, self.has_lab_var, 0))
		
		self.lab_num_credits_var = StringVar(right_frame)
		_, _, self.lab_num_credits_entry = BaseInputPage.get_labeled_input_field(
			right_frame,
			"Credit Count",
			"Entry",
			textvariable=self.lab_num_credits_var,
			validate="key",
			validatecommand=(right_frame.register(self.ensure_int), "%S"),
			required=True)
		self.input_widget_descriptors.append((self.lab_num_credits_entry, self.lab_num_credits_var, ""))
		
		self.lab_mins_per_week_var = StringVar(right_frame)
		_, _, self.lab_mins_per_week_entry = BaseInputPage.get_labeled_input_field(
			right_frame,
			"Minutes/Week",
			"Entry",
			textvariable=self.lab_mins_per_week_var,
			validate="key",
			validatecommand=(right_frame.register(self.ensure_int), "%S"),
			required=True)
		self.input_widget_descriptors.append((self.lab_mins_per_week_entry, self.lab_mins_per_week_var, ""))
		
		self.lab_num_sections_var = StringVar(right_frame)
		_, _, self.lab_num_sections_entry = BaseInputPage.get_labeled_input_field(
			right_frame,
			"Section Count",
			"Entry",
			textvariable=self.lab_num_sections_var,
			validate="key",
			validatecommand=(left_frame.register(self.ensure_int), "%S"),
			required=True)
		self.input_widget_descriptors.append((self.lab_num_sections_entry, self.lab_num_sections_var, ""))
		
		self.lab_room_type_var = StringVar(right_frame)
		_, _, self.lab_room_type_entry = BaseInputPage.get_labeled_input_field(
			right_frame,
			"Classroom Type",
			"OptionMenu",
			self.lab_room_type_var,
			*self.room_type_options_list,
			required=True)
		self.input_widget_descriptors.append((
			self.lab_room_type_entry, self.lab_room_type_var, self.room_type_options_list[0]))
		
		self.update_lab_widget_states()
	
	def ensure_int(self, S):
		try:
			int(S)
		except:
			self.bell()
			return False
		return True
	
	def update_lab_widget_states(self):
		s = "disabled" if self.has_lab_var.get() == 0 else "normal"
		for e in [
			self.lab_num_credits_entry,
			self.lab_mins_per_week_entry,
			self.lab_num_sections_entry,
			self.lab_room_type_entry
		]:
			e.config(state=s)
	
	def validate_input(self):
		check_lab = (self.has_lab_var.get() == 0) or (
			(self.has_lab_var.get() == 1)
				and (len(self.lab_num_credits_var.get()) > 0)
				and (len(self.lab_mins_per_week_var.get()) > 0)
				and (len(self.lab_num_sections_var.get()) > 0)
		)
		
		check_course = (
			(len(self.name_var.get()) > 0)
				and (len(self.dept_code_var.get()) > 0)
				and (len(self.course_number_var.get()) > 0)
				and (len(self.num_credits_var.get()) > 0)
				and (len(self.mins_per_week_var.get()) > 0)
				and (len(self.num_sections_var.get()) > 0)
		)
		
		return check_lab and check_course
	
	def objectify_input(self):
		lab_dict = {
			"credit_count": self.lab_num_credits_var.get(),
			"standard_minutes_per_week": self.lab_mins_per_week_var.get(),
			"section_count": self.lab_num_sections_var.get(),
			"room_type": self.room_type_options[self.lab_room_type_var.get()]
		} if self.has_lab_var.get() == 1 else None
		
		course_number = self.course_number_var.get()
		while len(course_number) < 3:
			course_number = "0" + course_number
		
		return {
			"name": self.name_var.get(),
			"course_code": "%s-%s" % (self.dept_code_var.get(), course_number),
			"credit_count": self.num_credits_var.get(),
			"standard_minutes_per_week": self.mins_per_week_var.get(),
			"section_count": self.num_sections_var.get(),
			"room_type": self.room_type_options[self.room_type_var.get()],
			"lab": lab_dict
		}
	
	def deobjectify_element(self, obj):
		dept_code, course_number = obj["course_code"].split("-")
		
		self.name_var.set(obj["name"])
		self.dept_code_var.set(dept_code)
		self.course_number_var.set(course_number)
		self.num_credits_var.set(obj["credit_count"])
		self.mins_per_week_var.set(obj["standard_minutes_per_week"])
		self.num_sections_var.set(obj["section_count"])
		self.room_type_var.set(ClassroomType(obj["room_type"]).pretty_print())
		
		lab_obj = obj["lab"]
		if lab_obj:
			self.has_lab_var.set(1)
			self.lab_num_credits_var.set(lab_obj["credit_count"])
			self.lab_mins_per_week_var.set(lab_obj["standard_minutes_per_week"])
			self.lab_num_sections_var.set(lab_obj["section_count"])
			self.lab_room_type_var.set(ClassroomType(lab_obj["room_type"]).pretty_print())
		else:
			self.has_lab_var.set(0)
			self.lab_num_credits_var.set("")
			self.lab_mins_per_week_var.set("")
			self.lab_num_sections_var.set("")
			self.lab_room_type_var.set(self.room_type_options_list[0])
	
	def stringify_element(self, obj):
		return "%s (%s)" % (obj["course_code"].replace("-", ""), obj["name"])
	
	def refresh_inputs(self):
		self.update_lab_widget_states()