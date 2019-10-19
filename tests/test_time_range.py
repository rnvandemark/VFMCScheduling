from datetime import time

from src.scheduling import MIN_MINS_BETWEEN_CLASSES
from src.time_range import TimeRange

def test_as_dummy_datetimes():
	tr0 = TimeRange(start=time(hour=8), end=time(hour=9, minute=15))
	tr1 = TimeRange(start=time(hour=11, minute=15), end=time(hour=13, minute=45))
	
	dummy0 = tr0.as_dummy_datetimes()
	dummy1 = tr1.as_dummy_datetimes()
	
	assert dummy0[0].date() == dummy0[1].date()
	assert dummy1[0].date() == dummy1[1].date()
	assert dummy0[0].date() == dummy1[0].date()
	assert dummy0[0].time() == tr0[0]
	assert dummy0[1].time() == tr0[1]
	assert dummy1[0].time() == tr1[0]
	assert dummy1[1].time() == tr1[1]

def test_overlaps_with():
	tr0 = TimeRange(start=time(hour=8), end=time(hour=9, minute=15))
	
	tr1_start_minute = tr0.end.minute + MIN_MINS_BETWEEN_CLASSES
	tr1 = TimeRange(start=time(hour=9, minute=tr1_start_minute), end=time(hour=10, minute=tr1_start_minute+15))
	
	tr2_start_minute = tr1_start_minute + 5
	tr2 = TimeRange(start=time(hour=9, minute=tr2_start_minute), end=time(hour=10, minute=tr2_start_minute+15))
	
	tr3 = TimeRange(start=time(hour=9, minute=15), end=time(hour=10, minute=30))
	
	tr4 = TimeRange(start=time(hour=9), end=time(hour=9, minute=50))
	
	tr5 = TimeRange(start=time(hour=8), end=time(hour=8, minute=50))
	
	tr6 = TimeRange(start=time(hour=8, minute=10), end=time(hour=9))
	
	tr7 = TimeRange(start=time(hour=7, minute=30), end=time(hour=9, minute=30))
	
	assert not tr0.overlaps_with(tr1)
	assert not tr0.overlaps_with(tr2)
	assert tr0.overlaps_with(tr3)
	assert not tr0.overlaps_with(tr3, include_buffer=False)
	assert tr0.overlaps_with(tr4)
	assert tr0.overlaps_with(tr5)
	assert tr0.overlaps_with(tr6)
	assert tr0.overlaps_with(tr7)

def test_normalize():
	tr0 = TimeRange(start=time(hour=8), end=time(hour=9, minute=15))
	tr1 = TimeRange.normalize(8, 0, 1, 15)
	tr2 = TimeRange.normalize(8, 0, 0, 75)
	
	tr3 = TimeRange(start=time(hour=11, minute=30), end=time(hour=14, minute=15))
	tr4 = TimeRange.normalize(11, 30, 2, 45)
	tr5 = TimeRange.normalize(11, 30, 1, 105)
	tr6 = TimeRange.normalize(11, 30, 0, 165)
	
	assert tr0 == tr1
	assert tr0 == tr2
	
	assert tr3 == tr4
	assert tr3 == tr5
	assert tr3 == tr6