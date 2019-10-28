from collections import namedtuple

from src.day_of_week import DayOfWeek

# This represents a pair of one of more days and the range of time that a course runs for each of those
# days. For example, "TR" at 11:00AM-12:15PM (Tuesday and Thursday from 11:00AM-12:15PM).
class DaysTimeRangePair(namedtuple("DaysTimeRangePairTuple", ["days", "time_range"])):
	
	def overlaps_with(self, day_enums, time_range):
		if time_range.overlaps_with(self.time_range):
			return len(set(self.days) & set(day_enums)) > 0
	
	def overlaps_with_other(self, days_time_range_pair):
		return self.overlaps_with(days_time_range_pair[0], days_time_range_pair[1])
	
	def __str__(self):
		return "{0} : {1}".format(
			",".join(str(d) for d in self.days),
			str(self.time_range)
		)
	
	def __lt__(self, other):
		return self.days < other.days if self.time_range == other.time_range else self.time_range < other.time_range
	
	@staticmethod
	def factory_from_days_string(days, time_range):
		return DaysTimeRangePair(days=DayOfWeek.list_from_string(days), time_range=time_range)