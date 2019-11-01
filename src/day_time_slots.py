from math import floor
from datetime import time

from src.scheduling import MIN_MINS_BETWEEN_CLASSES
from src.day_of_week import DayOfWeek
from src.time_range import TimeRange

EARLIEST_START_TIME = time(hour=7)
LATEST_START_TIME = time(hour=15)
LUNCH_PERIOD = TimeRange(start=time(hour=11, minute=5), end=time(hour=12))

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
	
	def get_all_clashes_for(self, days, time_range, bookings, restricted_tuples):
		clashes = self.clashes_with(days, time_range)
		
		for booking in bookings:
			clashes.extend(booking.time_ranges_overlapping_with(days, time_range))
		
		clashes.extend(t[0].time_range for t in restricted_tuples if t[0].overlaps_with(days, time_range))
		
		return clashes
	
	def get_first_available(self, mins_per_week, professor_bookings, restricted_tuples, preferred_days_per_week=None):
		if not preferred_days_per_week:
			preferred_days_per_week = 3
		
		days_per_week = None
		
		if mins_per_week < preferred_days_per_week * 50:
			days_per_week = 1
		elif mins_per_week % preferred_days_per_week == 0:
			days_per_week = preferred_days_per_week
		elif mins_per_week % 2 == 0:
			days_per_week = 2
		else:
			days_per_week = 3
			
		desired_days_list = DayOfWeek.optimal_lists_for(days_per_week)
		
		found_days = None
		found_time_range = None
		penalty = 0
		
		for desired_days in desired_days_list:
			days_per_week = len(desired_days)
			mins_per_day = floor(mins_per_week / days_per_week)
			desired_time_range = TimeRange.from_time_and_duration(EARLIEST_START_TIME, mins_per_day)
			
			existing_clashes = self.get_all_clashes_for(desired_days, desired_time_range, professor_bookings, restricted_tuples)
			while len(existing_clashes) > 0:
				latest_end = max(time_range.end for time_range in existing_clashes)
				earliest_start = TimeRange.time_translated_by(latest_end, 0, MIN_MINS_BETWEEN_CLASSES)
				
				desired_time_range = TimeRange.from_time_and_duration(earliest_start, mins_per_day)
				if desired_time_range.overlaps_with(LUNCH_PERIOD, include_buffer=False):
					desired_time_range = TimeRange.from_time_and_duration(LUNCH_PERIOD.end, mins_per_day)
				if desired_time_range.start > LATEST_START_TIME:
					break
				
				existing_clashes = self.get_all_clashes_for(desired_days, desired_time_range, professor_bookings, restricted_tuples)
				
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