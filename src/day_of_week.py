from enum import Enum

class DayOfWeek(Enum):
	SUNDAY = "U"
	MONDAY = "M"
	TUESDAY = "T"
	WEDNESDAY = "W"
	THURSDAY = "R"
	FRIDAY = "F"
	SATURDAY = "S"
	
	def __str__(self):
		return self.name
	
	@staticmethod
	def get_empty_dict(obj_type):
		return {day:obj_type() for day in DayOfWeek}
	
	@staticmethod
	def list_from_string(days):
		return [DayOfWeek(day) for day in days]
	
	@staticmethod
	def optimal_lists_for(num_days):
		if num_days == 1:
			return [
				DayOfWeek.list_from_string("M"),
				DayOfWeek.list_from_string("T"),
				DayOfWeek.list_from_string("W"),
				DayOfWeek.list_from_string("R"),
				DayOfWeek.list_from_string("F")
			]
		elif num_days == 2:
			return [
				DayOfWeek.list_from_string("TR"),
				DayOfWeek.list_from_string("MW"),
				DayOfWeek.list_from_string("MF")
			]
		elif num_days == 3:
			return [
				DayOfWeek.list_from_string("MWF"),
				DayOfWeek.list_from_string("TWR"),
				DayOfWeek.list_from_string("WRF"),
				DayOfWeek.list_from_string("MTW")
			]
		elif num_days == 4:
			return [
				DayOfWeek.list_from_string("MTWR"),
				DayOfWeek.list_from_string("TWRF")
			]
		elif num_days == 5:
			return [
				DayOfWeek.list_from_string("MTWRF")
			]
		else:
			return None