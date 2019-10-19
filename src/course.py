import logging

from src.classroom import ClassroomType

class Course():
	
	def __init__(self, json_obj):
		dept_code, course_number = json_obj["course_code"].split("-")
		
		self.name = json_obj["name"]
		self.dept_code = dept_code
		self.course_number = int(course_number)
		self.credit_count = json_obj["credit_count"]
		self.mins_per_week = json_obj["standard_minutes_per_week"]
		self.section_count = json_obj["section_count"]
		self.classroom_type = ClassroomType(json_obj["room_type"])
		self.scheduled_sections = 0
		self.restriction_count = 0
	
	def unschedule_section(self):
		if self.scheduled_sections == 0:
			logging.error(
				"Attempted to unschedule a section when none were scheduled: {0}{1}".format(
					self.dept_code,
					self.course_number
				)
			)
			return False
		
		self.scheduled_sections = self.scheduled_sections - 1
		return True
	
	def schedule_section(self):
		if self.all_sections_booked():
			logging.error(
				"Attempted to schedule a section when no more were available: {0}{1}, {2}".format(
					self.dept_code,
					self.course_number,
					self.scheduled_sections
				)
			)
			return -1
		
		return_value = self.scheduled_sections
		self.scheduled_sections = self.scheduled_sections + 1
		return return_value
	
	def all_sections_booked(self):
		return self.section_count == self.scheduled_sections
	
	def get_section_credits(self):
		return self.credit_count * self.section_count
	
	def get_unbooked_section_credits(self):
		return self.credit_count * (self.section_count - self.scheduled_sections)
	
	def as_programmatic_string(self):
		return "{0}-{1}".format(self.dept_code, self.course_number)
	
	def __str__(self):
		return self.name + ": " + self.as_programmatic_string()