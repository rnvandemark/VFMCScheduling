from datetime import time

from src.day_of_week import DayOfWeek
from src.time_range import TimeRange
from src.days_time_range_pair import DaysTimeRangePair

dtrp0 = DaysTimeRangePair.factory_from_days_string(
	"MWF",
	TimeRange(start=time(hour=7, minute=10), end=time(hour=8))
)
dtrp1 = DaysTimeRangePair.factory_from_days_string(
	"TR",
	TimeRange(start=time(hour=11, minute=15), end=time(hour=12, minute=30))
)
dtrp2 = DaysTimeRangePair.factory_from_days_string(
	"S",
	TimeRange.normalize(9, 0, 2, 30)
)

d0 = [DayOfWeek.WEDNESDAY, DayOfWeek.FRIDAY]
d1 = [DayOfWeek.WEDNESDAY, DayOfWeek.THURSDAY, DayOfWeek.FRIDAY]
d2 = [DayOfWeek.MONDAY, DayOfWeek.TUESDAY, DayOfWeek.WEDNESDAY]
d3 = [DayOfWeek.SATURDAY, DayOfWeek.SUNDAY]
d4 = d3

tr0 = TimeRange.normalize(7, 30, 0, 70)
tr1 = TimeRange.normalize(12, 0, 0, 75)
tr2 = TimeRange(start=time(hour=7, minute=30), end=time(hour=12))
tr3 = TimeRange(start=time(hour=9), end=time(hour=9, minute=50))
tr4 = TimeRange(start=time(hour=12), end=time(hour=13, minute=15))

def test_factory_from_days_string():
	assert dtrp0.days == [DayOfWeek.MONDAY, DayOfWeek.WEDNESDAY, DayOfWeek.FRIDAY]
	assert dtrp0.time_range == TimeRange(start=time(hour=7, minute=10), end=time(hour=8))
	
	assert dtrp1.days == [DayOfWeek.TUESDAY, DayOfWeek.THURSDAY]
	assert dtrp1.time_range == TimeRange(start=time(hour=11, minute=15), end=time(hour=12, minute=30))
	
	assert dtrp2.days == [DayOfWeek.SATURDAY]
	assert dtrp2.time_range == TimeRange(start=time(hour=9), end=time(hour=11, minute=30))

def test_overlaps_with():
	assert dtrp0.overlaps_with(d0, tr0)
	assert not dtrp1.overlaps_with(d0, tr0)
	assert not dtrp2.overlaps_with(d0, tr0)
	
	assert not dtrp0.overlaps_with(d1, tr1)
	assert dtrp1.overlaps_with(d1, tr1)
	assert not dtrp2.overlaps_with(d1, tr1)
	
	assert dtrp0.overlaps_with(d2, tr2)
	assert dtrp1.overlaps_with(d2, tr2)
	assert not dtrp2.overlaps_with(d2, tr2)
	
	assert not dtrp0.overlaps_with(d3, tr3)
	assert not dtrp1.overlaps_with(d3, tr3)
	assert dtrp2.overlaps_with(d3, tr3)
	
	assert not dtrp0.overlaps_with(d4, tr4)
	assert not dtrp1.overlaps_with(d4, tr4)
	assert not dtrp2.overlaps_with(d4, tr4)

def test_overlaps_with_other():
	dtrp3 = DaysTimeRangePair(days=d0, time_range=tr0)
	assert dtrp0.overlaps_with_other(dtrp3)
	assert not dtrp1.overlaps_with_other(dtrp3)
	assert not dtrp2.overlaps_with_other(dtrp3)
	
	dtrp4 = DaysTimeRangePair(days=d1, time_range=tr1)
	assert not dtrp0.overlaps_with_other(dtrp4)
	assert dtrp1.overlaps_with_other(dtrp4)
	assert not dtrp2.overlaps_with_other(dtrp4)
	
	dtrp5 = DaysTimeRangePair(days=d2, time_range=tr2)
	assert dtrp0.overlaps_with_other(dtrp5)
	assert dtrp1.overlaps_with_other(dtrp5)
	assert not dtrp2.overlaps_with_other(dtrp5)
	
	dtrp6 = DaysTimeRangePair(days=d3, time_range=tr3)
	assert not dtrp0.overlaps_with_other(dtrp6)
	assert not dtrp1.overlaps_with_other(dtrp6)
	assert dtrp2.overlaps_with_other(dtrp6)
	
	dtrp7 = DaysTimeRangePair(days=d4, time_range=tr4)
	assert not dtrp0.overlaps_with_other(dtrp7)
	assert not dtrp1.overlaps_with_other(dtrp7)
	assert not dtrp2.overlaps_with_other(dtrp7)