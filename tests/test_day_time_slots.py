from json import loads as json_loads
from datetime import time

from src.day_time_slots import DayTimeSlots
from src.day_of_week import DayOfWeek
from src.time_range import TimeRange
from src.days_time_range_pair import DaysTimeRangePair
from src.professor import Professor
from src.course import Course
from src.classroom import Classroom
from src.booking import Booking

def test_book_and_total_minutes_booked():
	dts = DayTimeSlots()
	
	assert dts.total_minutes_booked() == 0
	
	dtrp0 = DaysTimeRangePair.factory_from_days_string("MWF",
		TimeRange(start=time(hour=8, minute=50), end=time(hour=10, minute=5)))
	dts.book(dtrp0)
	assert dts.total_minutes_booked() == 225
	
	dtrp1 = DaysTimeRangePair.factory_from_days_string("TR",
		TimeRange(start=time(hour=11, minute=30), end=time(hour=12, minute=20)))
	dts.book(dtrp1)
	assert dts.total_minutes_booked() == 325
	
	dtrp2 = DaysTimeRangePair.factory_from_days_string("F",
		TimeRange.normalize(15, 0, 2, 30))
	dts.book(dtrp2)
	assert dts.total_minutes_booked() == 475

def test_clashes_with():
	dts = DayTimeSlots()
	
	dtrp0 = DaysTimeRangePair.factory_from_days_string("MWF",
		TimeRange(start=time(hour=8, minute=50), end=time(hour=10, minute=5)))
	dtrp1 = DaysTimeRangePair.factory_from_days_string("TR",
		TimeRange(start=time(hour=11, minute=30), end=time(hour=12, minute=20)))
	dtrp2 = DaysTimeRangePair.factory_from_days_string("F",
		TimeRange.normalize(15, 0, 2, 30))
	
	dtrp_clashes0 = DaysTimeRangePair.factory_from_days_string("MWF",
		TimeRange(start=time(hour=8, minute=50), end=time(hour=10, minute=5)))
	dtrp_clashes1 = DaysTimeRangePair.factory_from_days_string("TWR",
		TimeRange(start=time(hour=12), end=time(hour=12, minute=50)))
	dtrp_clashes2 = DaysTimeRangePair.factory_from_days_string("F",
		TimeRange(start=time(hour=15, minute=10), end=time(hour=16)))
	
	dtrp_no_clash0 = DaysTimeRangePair.factory_from_days_string("TR",
		TimeRange(start=time(hour=13), end=time(hour=14, minute=15)))
	dtrp_no_clash1 = DaysTimeRangePair.factory_from_days_string("MTWRF",
		TimeRange(start=time(hour=7), end=time(hour=7, minute=50)))
	dtrp_no_clash2 = DaysTimeRangePair.factory_from_days_string("MF",
		TimeRange(start=time(hour=11, minute=30), end=time(hour=13, minute=30)))
	
	dts.book(dtrp0)
	dts.book(dtrp1)
	dts.book(dtrp2)
	
	assert dts.clashes_with(dtrp_clashes0.days, dtrp_clashes0.time_range)
	assert dts.clashes_with(dtrp_clashes1.days, dtrp_clashes1.time_range)
	assert dts.clashes_with(dtrp_clashes2.days, dtrp_clashes2.time_range)
	
	assert not dts.clashes_with(dtrp_no_clash0.days, dtrp_no_clash0.time_range)
	assert not dts.clashes_with(dtrp_no_clash1.days, dtrp_no_clash1.time_range)
	assert not dts.clashes_with(dtrp_no_clash2.days, dtrp_no_clash2.time_range)

def test_get_first_available():
	course0 = Course(json_loads('''
		{
			"name": "Math Lab",
			"course_code": "MA-100",
			"credit_count": 1,
			"standard_minutes_per_week": 50,
			"section_count": 1,
			"room_type": "cr"
		}
	'''))

	course1 = Course(json_loads('''
		{
			"name": "Research Methods",
			"course_code": "IN-200",
			"credit_count": 3,
			"standard_minutes_per_week": 150,
			"section_count": 2,
			"room_type": "cr"
		}
	'''))

	course2 = Course(json_loads('''
		{
			"name": "College Algebra",
			"course_code": "MA-101",
			"credit_count": 3,
			"standard_minutes_per_week": 150,
			"section_count": 3,
			"room_type": "cr"
		}
	'''))

	course3 = Course(json_loads('''
		{
			"name": "Calculus 1",
			"course_code": "MA-104",
			"credit_count": 4,
			"standard_minutes_per_week": 200,
			"section_count": 2,
			"room_type": "cr"
		}
	'''))
	
	professor = Professor(json_loads('''
		{
			"first_name": "Joanne",
			"middle_name": "Q.",
			"last_name": "Smith",
			"departments": ["MA", "IN"]
		}
	'''))
	
	classroom = Classroom(json_loads('''
		{
			"room_code": "MB100",
			"room_type": "cr"
		}
	'''))
	
	bookings = []
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(1, 50, bookings)
	assert found_days == DayOfWeek.list_from_string("M")
	assert found_time_range == TimeRange(start=time(hour=7), end=time(hour=7, minute=50))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(2, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("TR")
	assert found_time_range == TimeRange(start=time(hour=7), end=time(hour=8, minute=15))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(3, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("MWF")
	assert found_time_range == TimeRange(start=time(hour=7), end=time(hour=7, minute=50))
	
	booking = Booking(
		course0,
		professor,
		(DayOfWeek.list_from_string("M"), TimeRange.normalize(7, 0, 0, 50), classroom)
	)
	booking.finalize()
	bookings.append(booking)
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(1, 50, bookings)
	assert found_days == DayOfWeek.list_from_string("M")
	assert found_time_range == TimeRange(start=time(hour=8), end=time(hour=8, minute=50))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(2, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("TR")
	assert found_time_range == TimeRange(start=time(hour=7), end=time(hour=8, minute=15))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(3, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("MWF")
	assert found_time_range == TimeRange(start=time(hour=8), end=time(hour=8, minute=50))
	
	booking = Booking(
		course1,
		professor,
		(DayOfWeek.list_from_string("F"), TimeRange.normalize(8, 0, 2, 30), classroom)
	)
	booking.finalize()
	bookings.append(booking)
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(1, 50, bookings)
	assert found_days == DayOfWeek.list_from_string("M")
	assert found_time_range == TimeRange(start=time(hour=8), end=time(hour=8, minute=50))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(2, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("TR")
	assert found_time_range == TimeRange(start=time(hour=7), end=time(hour=8, minute=15))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(3, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("MWF")
	assert found_time_range == TimeRange(start=time(hour=10, minute=40), end=time(hour=11, minute=30))
	
	booking = Booking(
		course1,
		professor,
		(DayOfWeek.list_from_string("T"), TimeRange.normalize(7, 0, 2, 30), classroom)
	)
	booking.finalize()
	bookings.append(booking)
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(1, 50, bookings)
	assert found_days == DayOfWeek.list_from_string("M")
	assert found_time_range == TimeRange(start=time(hour=8), end=time(hour=8, minute=50))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(2, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("TR")
	assert found_time_range == TimeRange(start=time(hour=9, minute=40), end=time(hour=10, minute=55))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(3, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("MWF")
	assert found_time_range == TimeRange(start=time(hour=10, minute=40), end=time(hour=11, minute=30))
	
	booking = Booking(
		course3,
		professor,
		(DayOfWeek.list_from_string("M"), TimeRange.normalize(8, 0, 0, 150), classroom),
		(DayOfWeek.list_from_string("F"), TimeRange.normalize(10, 40, 0, 50), classroom)
	)
	booking.finalize()
	bookings.append(booking)
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(1, 50, bookings)
	assert found_days == DayOfWeek.list_from_string("M")
	assert found_time_range == TimeRange(start=time(hour=10, minute=40), end=time(hour=11, minute=30))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(2, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("TR")
	assert found_time_range == TimeRange(start=time(hour=9, minute=40), end=time(hour=10, minute=55))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(3, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("MWF")
	assert found_time_range == TimeRange(start=time(hour=11, minute=40), end=time(hour=12, minute=30))
	
	booking = Booking(
		course3,
		professor,
		(DayOfWeek.list_from_string("TR"), TimeRange.normalize(9, 40, 1, 40), classroom)
	)
	booking.finalize()
	bookings.append(booking)
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(1, 50, bookings)
	assert found_days == DayOfWeek.list_from_string("M")
	assert found_time_range == TimeRange(start=time(hour=10, minute=40), end=time(hour=11, minute=30))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(2, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("TR")
	assert found_time_range == TimeRange(start=time(hour=11, minute=30), end=time(hour=12, minute=45))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(3, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("MWF")
	assert found_time_range == TimeRange(start=time(hour=11, minute=40), end=time(hour=12, minute=30))
	
	booking = Booking(
		course2,
		professor,
		(DayOfWeek.list_from_string("MWF"), TimeRange.normalize(11, 40, 0, 50), classroom)
	)
	booking.finalize()
	bookings.append(booking)
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(1, 50, bookings)
	assert found_days == DayOfWeek.list_from_string("M")
	assert found_time_range == TimeRange(start=time(hour=10, minute=40), end=time(hour=11, minute=30))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(2, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("TR")
	assert found_time_range == TimeRange(start=time(hour=11, minute=30), end=time(hour=12, minute=45))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(3, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("MWF")
	assert found_time_range == TimeRange(start=time(hour=12, minute=40), end=time(hour=13, minute=30))
	
	booking = Booking(
		course2,
		professor,
		(DayOfWeek.list_from_string("M"), TimeRange.normalize(10, 40, 0, 50), classroom),
		(DayOfWeek.list_from_string("TR"), TimeRange.normalize(11, 30, 0, 50), classroom)
	)
	booking.finalize()
	bookings.append(booking)
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(1, 50, bookings)
	assert found_days == DayOfWeek.list_from_string("M")
	assert found_time_range == TimeRange(start=time(hour=12, minute=40), end=time(hour=13, minute=30))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(2, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("TR")
	assert found_time_range == TimeRange(start=time(hour=12, minute=30), end=time(hour=13, minute=45))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(3, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("MWF")
	assert found_time_range == TimeRange(start=time(hour=12, minute=40), end=time(hour=13, minute=30))
	
	booking = Booking(
		course2,
		professor,
		(DayOfWeek.list_from_string("MWF"), TimeRange.normalize(12, 40, 0, 50), classroom)
	)
	booking.finalize()
	bookings.append(booking)
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(1, 50, bookings)
	assert found_days == DayOfWeek.list_from_string("M")
	assert found_time_range == TimeRange(start=time(hour=13, minute=40), end=time(hour=14, minute=30))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(2, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("TR")
	assert found_time_range == TimeRange(start=time(hour=12, minute=30), end=time(hour=13, minute=45))
	
	found_days, found_time_range, _ = classroom.slots.get_first_available(3, 150, bookings)
	assert found_days == DayOfWeek.list_from_string("MWF")
	assert found_time_range == TimeRange(start=time(hour=13, minute=40), end=time(hour=14, minute=30))