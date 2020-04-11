import logging

from src.classroom import ClassroomType

class SchedulableElement():
	
	WEIGHT_PER_CREDIT_FACTOR = 1
	WEIGHT_PER_MINUTE_FACTOR = 0.05
	
	def __init__(self, json_obj, dept_code, course_number, name):
		self.name = name
		self.dept_code = dept_code
		self.course_number = course_number
		self.credit_count = int(json_obj["credit_count"])
		self.mins_per_week = int(json_obj["standard_minutes_per_week"])
		self.section_count = int(json_obj["section_count"])
		self.classroom_type = ClassroomType(json_obj["room_type"])
		self.scheduled_sections = 0
		self.restriction_count = 0
		
		self.scheduling_weight = SchedulableElement.calculated_weight(self.credit_count, self.mins_per_week)
	
	def unschedule_section(self):
		if self.scheduled_sections == 0:
			logging.error("Attempted to unschedule a section when none were scheduled.")
			return False
		
		self.scheduled_sections = self.scheduled_sections - 1
		return True
	
	def schedule_section(self):
		if self.are_all_sections_booked():
			logging.error("Attempted to schedule a section when no more were available.")
			return -1
		
		return_value = self.scheduled_sections
		self.scheduled_sections = self.scheduled_sections + 1
		return return_value
	
	def are_all_sections_booked(self):
		return self.section_count == self.scheduled_sections
	
	def get_section_credits(self):
		return self.credit_count * self.section_count
	
	def get_booked_section_credits(self):
		return self.credit_count * self.scheduled_sections
	
	def get_unbooked_section_credits(self):
		return self.credit_count * (self.section_count - self.scheduled_sections)
	
	def get_total_possible_weight(self):
		return SchedulableElement.calculated_weight(
			self.get_section_credits(),
			self.section_count * self.mins_per_week
		)
	
	def get_booked_weight(self):
		return SchedulableElement.calculated_weight(
			self.get_booked_section_credits(),
			self.section_count * self.mins_per_week
		)
	
	def get_unbooked_weight(self):
		return SchedulableElement.calculated_weight(
			self.get_unbooked_section_credits(),
			self.mins_per_week * (self.section_count - self.scheduled_sections)
		)
	
	def get_weight_per_section(self):
		return SchedulableElement.calculated_weight(
			self.credit_count,
			self.mins_per_week
		)
	
	def as_programmatic_string(self):
		return "{0}-{1}".format(self.dept_code, self.course_number if self.course_number >= 100 else "0" + str(self.course_number))
	
	def __str__(self):
		return self.name + ": " + self.as_programmatic_string()
	
	@staticmethod
	def calculated_weight(credit_count, mins_per_week):
		return ((SchedulableElement.WEIGHT_PER_CREDIT_FACTOR * credit_count)
					+ (SchedulableElement.WEIGHT_PER_MINUTE_FACTOR * mins_per_week))

class Lab(SchedulableElement):
	
	def __init__(self, json_obj, parent_course):
		self_dept_code = parent_course.dept_code + "L"
		self_course_number = parent_course.course_number
		self_name = parent_course.name + " Lab"
		
		super(Lab, self).__init__(json_obj, self_dept_code, self_course_number, self_name)

		self.parent_course = parent_course

class Course(SchedulableElement):
	
	def __init__(self, json_obj):
		dept_code, course_number_str = json_obj["course_code"].split("-")
		super(Course, self).__init__(json_obj, dept_code, int(course_number_str), json_obj["name"])
		
		lab_json_obj = json_obj["lab"]
		self.lab = None if lab_json_obj is None else Lab(lab_json_obj, self)