from enum import Enum

from src.day_time_slots import DayTimeSlots

class ClassroomType(Enum):
	STANDARD = "cr"
	SCIENCE_LAB = "sl"
	COMPUTER_LAB = "cl"

class Classroom():
	
	def __init__(self, json_obj):
		self.code = json_obj["room_code"]
		self.type = ClassroomType(json_obj["room_type"])
		self.slots = DayTimeSlots()
	
	def business(self):
		return self.slots.total_minutes_booked()
	
	def is_booked_at(self, days, time_range):
		return len(self.slots.clashes_with(days, time_range)) != 0
	
	def __str__(self):
		return self.code