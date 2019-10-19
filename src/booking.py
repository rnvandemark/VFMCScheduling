from src.day_of_week import DayOfWeek
from src.days_time_range_pair import DaysTimeRangePair
from src.restriction import Restriction

# This class describes each necessary DaysTimeRangePair for a course, as well as the course and
# the booked section number and the professor. The blocks list will likely be a list of size 1,
# but can be larger if there's an irregular meeting time, such as for labs.
class Booking():
	
	# Each booking needs the course being booked and the professor for this section of the course,
	# which are passed as a course instance and a professor instance, respectively.
	# Then, each element in contents is a tuple of size three containing:
	#	A list of DayOfWeek enums describing the applicable day(s)
	#	A TimeRange object describing the start and end time
	#	A Classroom instance describing the room that the class will be ran in
	# For example:
	#	<Course1>,
	#	<Professor5>,
	#	("TR", TimeRange(11:00AM-12:15PM), <Classroom3>),
	#	("F", TimeRange(8:00AM-10:45AM), <Classroom11>)
	def __init__(self, course, prof, *contents):
		if len(contents) <= 0:
			raise ValueError("A booking needs to have at least one pair of days and corresponding time range.")
		
		self.course = course
		self.section_number = -1
		self.professor = prof
		
		self.blocks = [(
			DaysTimeRangePair(days=element[0], time_range=element[1]), element[2]
		) for element in contents]
	
	def finalize(self):
		section_number = self.course.schedule_section()
		if section_number < 0:
			raise ValueError("Provided course cannot schedule another section: %s" % self.course.name)
		
		self.section_number = section_number
		
		for b in self.blocks:
			b[1].slots.book(b[0])
	
	def time_ranges_overlapping_with(self, days, time_range):
		overlapping_blocks = []
		for b in self.blocks:
			if b[0].overlaps_with(days, time_range):
				overlapping_blocks.append(b[0].time_range)
		return overlapping_blocks
	
	def get_booked_credits_for(self, prof):
		return self.course.credit_count if (self.section_number >= 0) and (prof == self.professor) else 0
	
	def restrictions_overlap(self, restriction_list, existing_bookings):
		self_course_code = self.course.as_programmatic_string()
		for other_booking in existing_bookings:
			other_course_code = other_booking.course.as_programmatic_string()
			for other_block in other_booking.blocks:
				for self_block in self.blocks:
					if self_block[0].overlaps_with_other(other_block[0]):
						if not Restriction.can_overlap(restriction_list, self_course_code, other_course_code):
							return True
		return False
	
	def __str__(self):
		return "{0}, section #{1}\n{2}\n{3}".format(
			str(self.course),
			self.section_number,
			str(self.professor),
			"\n".join("{0}: {1}".format(str(b[1]), str(b[0])) for b in self.blocks)
		)
	
	@staticmethod
	def get_total_booked_credits_for(bookings, prof):
		return sum(b.get_booked_credits_for(prof) for b in bookings)