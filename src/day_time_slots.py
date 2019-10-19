from math import floor
from datetime import time

from src.scheduling import MIN_MINS_BETWEEN_CLASSES
from src.day_of_week import DayOfWeek
from src.time_range import TimeRange

EARLIEST_START_TIME = time(hour=7)
LATEST_START_TIME = time(hour=16)

class DayTimeSlots():
	
	def __init__(self):
		self.schedule = DayOfWeek.get_empty_dict(list)
	
	def total_minutes_booked(self):
		return sum(tr.minutes() for time_ranges in self.schedule.values() for tr in time_ranges)
	
	def book(self, days_time_range_pair):
		for day in days_time_range_pair.days:
			self.schedule[day].append(days_time_range_pair.time_range)
	
	def clashes_with(self, days, time_range):
		clashes = []
		
		for day in days:
			for existing_time_range in self.schedule[day]:
				if time_range.overlaps_with(existing_time_range):
					clashes.append(existing_time_range)
		
		return clashes
	
	def get_first_available(self, days_per_week, mins_per_week, professor_bookings):
		desired_days_list = DayOfWeek.optimal_lists_for(days_per_week)
		mins_per_day = floor(mins_per_week / days_per_week)
		
		found_days = None
		found_time_range = None
		penalty = 0
		for desired_days in desired_days_list:
			desired_time_range = TimeRange.normalize(
				EARLIEST_START_TIME.hour, 
				EARLIEST_START_TIME.minute,
				0,
				mins_per_day
			)
			
			existing_clashes = self.clashes_with(desired_days, desired_time_range)
			for booking in professor_bookings:
				existing_clashes.extend(booking.time_ranges_overlapping_with(desired_days, desired_time_range))
			
			while len(existing_clashes) > 0:
				latest_end = max(time_range.end for time_range in existing_clashes)
				earliest_start = TimeRange.time_translated_by(latest_end, 0, MIN_MINS_BETWEEN_CLASSES)
				
				desired_time_range = TimeRange.normalize(earliest_start.hour, earliest_start.minute, 0, mins_per_day)
				if desired_time_range.start > LATEST_START_TIME:
					break
				
				existing_clashes = self.clashes_with(desired_days, desired_time_range)
				for booking in professor_bookings:
					existing_clashes.extend(booking.time_ranges_overlapping_with(desired_days, desired_time_range))
				
				penalty = sum(
					time_range.minutes_between(desired_time_range) for time_range in existing_clashes
				) / days_per_week
			
			if len(existing_clashes) == 0:
				found_days = desired_days
				found_time_range = desired_time_range
				break
		
		if (found_days is not None) and (found_time_range is not None):
			return (found_days, found_time_range, penalty)
		else:
			return None