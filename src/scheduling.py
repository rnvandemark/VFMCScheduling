import logging
from random import shuffle
from math import floor

MIN_MINS_BETWEEN_CLASSES = 10
OBJECTIVE_CREDITS_PER_PROFESSOR = 15

from src.json_registrar import *
from src.course import *
from src.classroom import *
from src.professor import *
from src.restriction import *
from src.booking import *

class Scheduler():
	
	def __init__(self, courses_url, profs_url, rooms_url, restrictions_url):
		self.course_registrar      = CourseRegistrar(courses_url)
		self.prof_registrar        = ProfessorRegistrar(profs_url)
		self.room_registrar        = ClassroomRegistrar(rooms_url)
		self.restriction_registrar = RestrictionRegistrar(restrictions_url)
		
		self.courses_to_schedule = [
			Course(course_json) for course_json in self.course_registrar.course_list
		]
		
		self.profs_by_dept = {}
		for prof_json in self.prof_registrar.prof_list:
			prof = Professor(prof_json)
			for d in prof.departments:
				if d not in self.profs_by_dept:
					self.profs_by_dept[d] = []
				self.profs_by_dept[d].append(prof)
		
		self.classrooms_by_type = {
			ClassroomType.STANDARD: [],
			ClassroomType.SCIENCE_LAB: [],
			ClassroomType.COMPUTER_LAB: []
		}
		for room_json in self.room_registrar.room_list:
			room = Classroom(room_json)
			self.classrooms_by_type[room.type].append(room)
		
		self.active_restrictions = []
		for restriction_json in self.restriction_registrar.restriction_list:
			restriction = Restriction(restriction_json)
			self.active_restrictions.append(restriction)
			
			if restriction.type == RestrictionType.SINGLE_GROUP:
				self.account_for_restricted_course_codes(restriction.contents)
			elif restriction.type == RestrictionType.MULTIPLE_GROUPS:
				for course_codes in restriction.contents:
					self.account_for_restricted_course_codes(course_codes)
			else:
				raise ValueError("Can't process for invalid restriction type: {0}".format(restriction.type))
		
		shuffle(self.courses_to_schedule)
		self.courses_to_schedule.sort(key=lambda course: course.restriction_count)
		
		for dept_profs in self.profs_by_dept.values():
			shuffle(dept_profs)
	
	def account_for_restricted_course_codes(self, course_code_list):
		for course_code in course_code_list:
			dept_code, course_number = course_code.split("-")
			if course_number == "*":
				for course in self.courses_to_schedule:
					if course.dept_code == dept_code:
						course.restriction_count = course.restriction_count + 1
			else:
				try:
					course_number = int(course_number)
				except ValueError as e:
					logging.error("Invalid course number provided for restriction: %s" % course_number)
					continue
				
				for course in self.courses_to_schedule:
					if (course.dept_code == dept_code) and (course.course_number == course_number):
						course.restriction_count = course.restriction_count + 1
						break
				else:
					logging.warning("Restriction for nonexistent department: %d" % course_number)
	
	#def get_credit_count_for(self, *dept_codes):
	#	total_credits = 0
	#	for dept_code in dept_codes:
	#		if dept_code in self.courses_to_schedule:
	#			for course in self.courses_to_schedule[dept_code].values():
	#				total_credits = total_credits + (course.credits * course.sections)
	#		else:
	#			logging.warning("Attempted to search for a department with no courses in it: %s" % dept_code)
	#	return total_credits
	
	#def has_work_left(self):
	#	for course in self.courses_to_schedule:
	#		if not course.all_sections_booked():
	#			return True
	#	
	#	return False
	
	def plan(self):
		bookings = []
		
		while len(self.courses_to_schedule) > 0:
			course = self.courses_to_schedule.pop()
			if course.all_sections_booked():
				continue
			
			credits_to_try = course.get_unbooked_section_credits()
			while credits_to_try > 0:
				desired_professor = self.profs_by_dept[course.dept_code][0]
				
				booked_credits = Booking.get_total_booked_credits_for(bookings, desired_professor)
				sections_bookable = 0
				if booked_credits + course.credit_count >= OBJECTIVE_CREDITS_PER_PROFESSOR:
					sections_bookable = 1
				else:
					available_credits = OBJECTIVE_CREDITS_PER_PROFESSOR - booked_credits
					sections_bookable = floor(min(credits_to_try, available_credits) / course.credit_count)
				
				desired_classroom_list = self.classrooms_by_type[course.classroom_type]
				
				days_per_week = 0
				if course.credit_count == 1:
					days_per_week = 1
				elif course.mins_per_week % 3 != 0:
					days_per_week = 2
				elif course.mins_per_week < 150:
					days_per_week = 1
				else:
					days_per_week = 3
				
				sections_booked = 0
				classroom_index = -1
				desired_classroom = None
				for i in range(sections_bookable):
					availability = None
					while availability is None:
						classroom_index = classroom_index + 1
						if classroom_index >= len(desired_classroom_list):
							raise ValueError("Impossible schedule!")
						desired_classroom = desired_classroom_list[classroom_index]
						
						availability = desired_classroom.slots.get_first_available(
							days_per_week,
							course.mins_per_week,
							[b for b in bookings if b.professor == desired_professor]
						)
					
					potential_booking = Booking(
						course,
						desired_professor,
						(availability[0], availability[1], desired_classroom)
					)
					
					#if potential_booking.restrictions_overlap(self.active_restrictions, bookings):
					#	self.courses_to_schedule.append(course)
					#	self.courses_to_schedule.sort(key=lambda course: course.restriction_count)
					#else:
					#	potential_booking.finalize()
					#	bookings.append(potential_booking)
					#	sections_booked = sections_booked + 1
					
					potential_booking.finalize()
					bookings.append(potential_booking)
					sections_booked = sections_booked + 1
				
				self.profs_by_dept[course.dept_code].sort(
					key=lambda prof: Booking.get_total_booked_credits_for(bookings, prof)
				)
				
				self.classrooms_by_type[course.classroom_type].sort(
					key=lambda room: room.business(),
					reverse=True
				)
				
				credits_to_try = credits_to_try - (sections_bookable * course.credit_count)
		
		return bookings