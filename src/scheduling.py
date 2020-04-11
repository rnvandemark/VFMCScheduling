import logging
from math import floor
from random import shuffle, getrandbits
from copy import deepcopy

from src.classroom import *
from src.json_registrar import *
from src.schedulable_element import *
from src.professor import *
from src.restriction import *
from src.booking import *
from src.constants import OBJECTIVE_WEIGHT_PER_PROFESSOR, FORCE_LAB_ON_ONE_DAY, ATTEMPT_EVEN_DISTRIBUTION

class Scheduler():
	
	def __init__(self, courses_url, profs_url, rooms_url, restrictions_url):
		self.course_registrar      = CourseRegistrar(courses_url)
		self.prof_registrar        = ProfessorRegistrar(profs_url)
		self.room_registrar        = ClassroomRegistrar(rooms_url)
		self.restriction_registrar = RestrictionRegistrar(restrictions_url)
		
		self.courses_in_registrar = [
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
		
		self.dept_relative_availability = None
		self.update_relative_availabilities(True)
		
		shuffle(self.courses_in_registrar)
		self.courses_in_registrar.sort(key=lambda c: self.get_element_sort_value(c))
		
		for dept_profs in self.profs_by_dept.values():
			shuffle(dept_profs)
	
	def account_for_restricted_course_codes(self, course_code_list):
		for course_code in course_code_list:
			dept_code, course_number = course_code.split("-")
			if course_number == "*":
				for course in self.courses_in_registrar:
					if course.dept_code == dept_code:
						course.restriction_count = course.restriction_count + 1
			else:
				try:
					course_number = int(course_number)
				except ValueError as e:
					logging.error("Invalid course number provided for restriction: %s" % course_number)
					continue
				
				for course in self.courses_in_registrar:
					if (course.dept_code == dept_code) and (course.course_number == course_number):
						course.restriction_count = course.restriction_count + 1
						break
				else:
					logging.warning("Restriction for nonexistent course: %s%d" % (dept_code, course_number))
	
	def update_relative_availabilities(self, reinitialize, dept_codes_list=None, existing_bookings={}):
		dict_obj = None
		
		if reinitialize:
			self.dept_relative_availability = {}
			dict_obj = self.profs_by_dept
		elif dept_codes_list:
			dict_obj = {dc:self.profs_by_dept[dc] for dc in dept_codes_list}
		else:
			dict_obj = {}
		
		for dept_code, profs_list in self.profs_by_dept.items():
			relative_availability = 0
			
			for prof in profs_list:
				prof_existing_weight = Booking.get_total_finalized_weight_for(existing_bookings, prof)
				relative_availability = relative_availability + OBJECTIVE_WEIGHT_PER_PROFESSOR - prof_existing_weight
			
			self.dept_relative_availability[dept_code] = 1 / relative_availability
	
	def get_element_sort_value(self, element):
		# This first prioritizes schedulable elements with the most restrictions, then prioritizes the elements
		# with the least cumulative amount of available time for all of the professors in this elements' department.
		return (element.restriction_count, self.dept_relative_availability[element.dept_code])
	
	def plan_schedulable_element(self, element, existing_bookings, desired_professor=None, sort_after=True):
		element_type = type(element)
		
		dept_code = None
		if element_type == Course:
			dept_code = element.dept_code
		elif element_type == Lab:
			dept_code = element.parent_course.dept_code
		else:
			raise ValueError("Impossible element type detected while planning: %s" % element_type.__name__)
		
		if dept_code not in self.profs_by_dept:
			raise ValueError("Department code not recognized: %s" % dept_code)
		elif len(self.profs_by_dept[dept_code]) < 1:
			raise ValueError("No professors available for a element's department code: %s" % dept_code)
		
		desired_professor = self.profs_by_dept[dept_code][0]
		prof_existing_weight = Booking.get_total_finalized_weight_for(existing_bookings, desired_professor)
		weight_per_element_section = element.get_weight_per_section()
		
		sections_bookable = min(
			2 if element_type == Lab else 3,
			floor(element.get_unbooked_weight() / weight_per_element_section),
			floor((OBJECTIVE_WEIGHT_PER_PROFESSOR - prof_existing_weight) / weight_per_element_section)
		)
		
		if sections_bookable <= 0:
			sections_bookable = 1
		
		desired_classroom_list = self.classrooms_by_type[element.classroom_type]
		
		# Just for now, because of the way it was requested this time
		preferred_days_per_week = 2
		#if FORCE_LAB_ON_ONE_DAY and (element_type == Lab):
		#	preferred_days_per_week = 1
		#elif ATTEMPT_EVEN_DISTRIBUTION:
		#	preferred_days_per_week = 2 + getrandbits(1)
		
		# Gather restrictions from existing bookings. No need to worry about classes with the selected professor
		# because those overlaps will be rejected in the DayTimeSlots' get_first_available routine, and we also
		# only need to check professors that have existing bookings.
		
		restricted_tuples = []
		for other_bookings in (b for p, b in existing_bookings.items() if p != desired_professor):
			for existing_booking in other_bookings:
				if not Restriction.can_overlap(
					self.active_restrictions,
					element.as_programmatic_string(),
					existing_booking.element.as_programmatic_string()
				):
					restricted_tuples.extend(
						(b[0], existing_booking.element) for b in existing_booking.blocks
					)
		
		classroom_index = None
		desired_classroom = None
		for i in range(sections_bookable):
			classroom_index = -1
			
			availability = None
			while availability is None:
				classroom_index = classroom_index + 1
				if classroom_index >= len(desired_classroom_list):
					raise ValueError("Ran out of possible classrooms for element: %s" % element.name)
				desired_classroom = desired_classroom_list[classroom_index]
				
				availability = desired_classroom.slots.get_first_available(
					element.mins_per_week,
					existing_bookings.get(desired_professor, []),
					restricted_tuples,
					preferred_days_per_week=preferred_days_per_week
				)
			
			new_booking = Booking(
				element,
				desired_professor,
				(availability[0], availability[1], desired_classroom)
			).finalize()
			
			if desired_professor not in existing_bookings:
				existing_bookings[desired_professor] = []
			existing_bookings[desired_professor].append(new_booking)
		
		if sort_after:
			self.profs_by_dept[dept_code].sort(
				key=lambda prof: Booking.get_total_finalized_weight_for(existing_bookings, prof),
				reverse=False
			)
			
			self.classrooms_by_type[element.classroom_type].sort(
				key=lambda room: room.business(),
				reverse=True
			)
		
		return desired_professor
	
	def plan(self):
		bookings = {}
		
		courses_to_schedule = deepcopy(self.courses_in_registrar)
		original_length = len(courses_to_schedule)
		while len(courses_to_schedule) > 0:
			stmt = str(round((1 - (len(courses_to_schedule) / original_length)) * 100, 4))
			stmt = stmt + ("0" * (4 - len(stmt[stmt.find(".")+1:]))) + "%"
			print(stmt, end="\r")
			
			scheduled_professor = None
			reattempt_scheduling = False
			
			course = courses_to_schedule.pop()
			if not course.are_all_sections_booked():
				scheduled_professor = self.plan_schedulable_element(course, bookings)
				if not course.are_all_sections_booked():
					reattempt_scheduling = True
			
			if course.lab:
				if not course.lab.are_all_sections_booked():
					scheduled_professor = self.plan_schedulable_element(course.lab, bookings, desired_professor=scheduled_professor)
					if not course.lab.are_all_sections_booked():
						reattempt_scheduling = True
			
			if reattempt_scheduling:
				courses_to_schedule.append(course)
				self.update_relative_availabilities(False, dept_codes_list=scheduled_professor.departments, existing_bookings=bookings)
				courses_to_schedule.sort(key=lambda c: self.get_element_sort_value(c))
		
		print("        ", end="\r")
		return bookings
	
	def try_until_success(self):
		retry = True
		schedule = None
		
		while retry:
			try:
				schedule = self.plan()
				retry = False
			except KeyboardInterrupt:
				raise
			except:
				pass
		
		return schedule