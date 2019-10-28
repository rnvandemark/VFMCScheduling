from math import floor
from collections import namedtuple
from datetime import time, datetime, timedelta, MINYEAR

from src.scheduling import MIN_MINS_BETWEEN_CLASSES

class TimeRange(namedtuple("TimeRangeTuple", ["start", "end"])):
	
	def as_dummy_datetimes(self):
		return (
			TimeRange.time_as_dummy_datetime(self.start),
			TimeRange.time_as_dummy_datetime(self.end)
		)
	
	def overlaps_with(self, other, include_buffer=True):
		if self.start == other.start:
			return True
		
		dummy_self  = self.as_dummy_datetimes()
		dummy_other = other.as_dummy_datetimes()
		
		earlier = None
		later   = None
		
		if self.start <= other.start:
			earlier = dummy_self
			later   = dummy_other
		else:
			earlier = dummy_other
			later   = dummy_self
		
		if include_buffer:
			return (earlier[1] + timedelta(minutes=MIN_MINS_BETWEEN_CLASSES)) > later[0]
		else:
			return earlier[1] > later[0]
	
	def minutes(self):
		dummy = self.as_dummy_datetimes()
		return floor((dummy[1] - dummy[0]).seconds / 60)
	
	def minutes_between(self, other):
		if self.overlaps_with(other, include_buffer=False):
			return 0
		
		dummy_self  = self.as_dummy_datetimes()
		dummy_other = other.as_dummy_datetimes()
		
		earlier = None
		later   = None
		
		if self.end <= other.start:
			earlier = dummy_self
			later   = dummy_other
		else:
			earlier = dummy_other
			later   = dummy_self
		
		return floor((later[0] - earlier[1]).seconds / 60)
	
	def pretty_print(self):
		start_hour = str(self.start.hour + 1)
		if self.start.hour + 1 < 10:
			start_hour = "0" + start_hour
		
		start_minute = str(self.start.minute)
		if self.start.minute < 10:
			start_minute = "0" + start_minute
		
		end_hour = str(self.end.hour + 1)
		if self.end.hour + 1 < 10:
			end_hour = "0" + end_hour
		
		end_minute = str(self.end.minute)
		if self.end.minute < 10:
			end_minute = "0" + end_minute
		
		return "{0}:{1} to {2}:{3}".format(
			start_hour,
			start_minute,
			end_hour,
			end_minute
		)
	
	def __str__(self):
		return "[{0} to {1}]".format(
			self.start,
			self.end
		)
	
	def __lt__(self, other):
		return self.end < other.end if self.start == other.start else self.start < other.start
	
	@staticmethod
	def normalize(start_hour, start_minute, duration_hours, duration_minutes):
		if (duration_hours < 0) or (duration_minutes < 0):
			raise ValueError("Each duration (hour and minute) must be a non-negative number.")
		
		add_hours, end_minute = divmod(start_minute + duration_minutes, 60)
		end_hour = start_hour + duration_hours + add_hours
		
		if end_hour > 23:
			raise ValueError("The TimeRange class does not support a time spanning multiple days.")
		
		return TimeRange(
			start=time(hour=start_hour, minute=start_minute),
			end=time(hour=end_hour, minute=end_minute)
		)
	
	@staticmethod
	def time_as_dummy_datetime(time):
		return datetime.combine(datetime(year=MINYEAR, month=1, day=1), time)
	
	@staticmethod
	def time_translated_by(t, h, m):
		return (TimeRange.time_as_dummy_datetime(t) + timedelta(hours=h, minutes=m)).time()