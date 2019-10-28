from src.day_of_week import DayOfWeek
from src.days_time_range_pair import DaysTimeRangePair
from src.restriction import Restriction

# This class describes each necessary DaysTimeRangePair for an element, as well as the element and
# the booked section number and the professor. The blocks list will likely be a list of size 1,
# but can be larger if there's an irregular meeting time, such as for labs.
class Booking():
	
	# Each booking needs the element being booked and the professor for this section of the element,
	# which are passed as an element instance and a professor instance, respectively.
	# Then, each element in contents is a tuple of size three containing:
	#	A list of DayOfWeek enums describing the applicable day(s)
	#	A TimeRange object describing the start and end time
	#	A Classroom instance describing the room that the class will be ran in
	# For example:
	#	<element1>,
	#	<Professor5>,
	#	("TR", TimeRange(11:00AM-12:15PM), <Classroom3>),
	#	("F", TimeRange(8:00AM-10:45AM), <Classroom11>)
	def __init__(self, element, prof, *contents):
		if len(contents) <= 0:
			raise ValueError("A booking needs to have at least one pair of days and corresponding time range.")
		
		self.element = element
		self.section_number = -1
		self.professor = prof
		
		self.blocks = [(
			DaysTimeRangePair(days=element[0], time_range=element[1]), element[2]
		) for element in contents]
	
	def finalize(self):
		section_number = self.element.schedule_section()
		if section_number < 0:
			raise ValueError("Provided element cannot schedule another section: %s" % self.element.name)
		
		self.section_number = section_number
		
		for b in self.blocks:
			b[1].slots.book(b[0])
		
		return self
	
	def time_ranges_overlapping_with(self, days, time_range):
		overlapping_blocks = []
		for b in self.blocks:
			if b[0].overlaps_with(days, time_range):
				overlapping_blocks.append(b[0].time_range)
		return overlapping_blocks
	
	def get_finalized_credits(self, days=[d for d in DayOfWeek]):
		total_credits = 0
		
		if self.section_number >= 0:
			for b in self.blocks:
				total_credits = total_credits + (sum(self.element.credit_count for d in b[0].days if d in days) / len(b[0].days))
			total_credits = total_credits / len(self.blocks)
		
		return int(total_credits)
	
	def get_finalized_weight(self, days=[d for d in DayOfWeek]):
		total_weight = 0
		
		if self.section_number >= 0:
			weight_per_section = self.element.get_weight_per_section()
			for b in self.blocks:
				total_weight = total_weight + (sum(weight_per_section for d in b[0].days if d in days) / len(b[0].days))
			total_weight = total_weight / len(self.blocks)
		
		return total_weight
	
	def restrictions_overlap(self, restriction_list, existing_bookings):
		overlapped = {}
		
		self_element_code = self.element.as_programmatic_string()
		for other_booking in existing_bookings:
			other_element = other_booking.element
			other_element_code = other_element.as_programmatic_string()
			for other_block in other_booking.blocks:
				for self_block in self.blocks:
					if self_block[0].overlaps_with_other(other_block[0]):
						if not Restriction.can_overlap(restriction_list, self_element_code, other_element_code):
							return True
		
		return False
	
	def __str__(self):
		return "{0}, section #{1}\n{2}\n{3}".format(
			str(self.element),
			self.section_number,
			str(self.professor),
			"\n".join("{0}: {1}".format(str(b[1]), str(b[0])) for b in self.blocks)
		)
	
	@staticmethod
	def get_total_finalized_credits_for(bookings, prof, days=[d for d in DayOfWeek]):
		return sum(b.get_finalized_credits(days=days) for b in bookings.get(prof, []))
	
	@staticmethod
	def get_total_finalized_weight_for(bookings, prof, days=[d for d in DayOfWeek]):
		return sum(b.get_finalized_weight(days=days) for b in bookings.get(prof, []))