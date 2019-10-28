from json import loads as json_loads
from datetime import time
from copy import copy

from src.schedulable_element import Course
from src.professor import Professor
from src.classroom import Classroom
from src.booking import Booking
from src.day_of_week import DayOfWeek
from src.time_range import TimeRange
from src.restriction import Restriction

course0 = Course(json_loads('''
	{
		"name": "Calculus 1",
		"course_code": "MA-104",
		"credit_count": 4,
		"standard_minutes_per_week": 200,
		"section_count": 2,
		"room_type": "cr",
		"lab": null
	}
'''))
course1 = Course(json_loads('''
	{
		"name": "College Algebra",
		"course_code": "MA-101",
		"credit_count": 3,
		"standard_minutes_per_week": 150,
		"section_count": 3,
		"room_type": "cr",
		"lab": null
	}
'''))
course2 = Course(json_loads('''
	{
		"name": "Research Methods",
		"course_code": "IN-200",
		"credit_count": 3,
		"standard_minutes_per_week": 150,
		"section_count": 1,
		"room_type": "cr",
		"lab": null
	}
'''))
course3 = Course(json_loads('''
	{
		"name": "Physics 1",
		"course_code": "PH-201",
		"credit_count": 4,
		"standard_minutes_per_week": 330,
		"section_count": 2,
		"room_type": "sl",
		"lab": null
	}
'''))

professor0 = Professor(json_loads('''
	{
		"first_name": "Joanne",
		"middle_name": "Q.",
		"last_name": "Smith",
		"departments": ["MA", "PH", "IN"]
	}
'''))
professor1 = Professor(json_loads('''
	{
		"first_name": "Robert",
		"middle_name": "",
		"last_name": "O'Connor",
		"departments": ["MA"]
	}
'''))

classroom0 = Classroom(json_loads('''
	{
		"room_code": "MB100",
		"room_type": "cr"
	}
'''))
classroom1 = Classroom(json_loads('''
	{
		"room_code": "MB110",
		"room_type": "cr"
	}
'''))
classroom2 = Classroom(json_loads('''
	{
		"room_code": "MB120",
		"room_type": "cr"
	}
'''))

booking0 = Booking(
	copy(course0),
	professor0,
	(DayOfWeek.list_from_string("TR"), TimeRange.normalize(7, 0, 0, 100), classroom0)
)
booking1 = Booking(
	copy(course0),
	professor0,
	(DayOfWeek.list_from_string("TR"), TimeRange.normalize(11, 0, 0, 100), classroom0)
)
booking2 = Booking(
	copy(course1),
	professor1,
	(DayOfWeek.list_from_string("MWF"), TimeRange.normalize(8, 10, 0, 50), classroom0)
)
booking3 = Booking(
	copy(course1),
	professor1,
	(DayOfWeek.list_from_string("T"), TimeRange.normalize(7, 0, 1, 15), classroom1),
	(DayOfWeek.list_from_string("R"), TimeRange.normalize(11, 0, 1, 15), classroom1)
)
booking4 = Booking(
	copy(course1),
	professor0,
	(DayOfWeek.list_from_string("TR"), TimeRange.normalize(13, 45, 0, 75), classroom2)
)
booking5 = Booking(
	copy(course2),
	professor1,
	(DayOfWeek.list_from_string("R"), TimeRange.normalize(8, 0, 2, 30), classroom2)
)
booking6 = Booking(
	copy(course3),
	professor1,
	(DayOfWeek.list_from_string("T"), TimeRange.normalize(12, 30, 2, 30), classroom2)
)

def test_finalize():
	c0 = copy(course0)
	c1 = copy(course1)
	
	cr = copy(classroom0)
	
	days_per_week = 2
	bookings = []
	lamb = lambda b: sum(len(s) for s in cr.slots.schedule.values()) == days_per_week * len(b)
	
	for c in [c0, c1]:
		for i in range(c.section_count):
			d, tr, _ = cr.slots.get_first_available(c.mins_per_week, bookings, [], preferred_days_per_week=days_per_week)
			b = Booking(c, professor0, (d, tr, cr))
			
			assert b.section_number == -1
			assert lamb(bookings)
			
			return_val = b.finalize()
			bookings.append(b)
			
			assert b.section_number == i
			assert return_val == b
			assert lamb(bookings)

def test_time_ranges_overlapping_with():
	b0 = copy(booking0)
	b0.finalize()
	
	b1 = copy(booking1)
	b1.finalize()
	
	b2 = copy(booking2)
	b2.finalize()
	
	b3 = copy(booking3)
	b3.finalize()
	
	b4 = copy(booking4)
	b4.finalize()
	
	days = DayOfWeek.list_from_string("MWF")
	time_range = TimeRange.normalize(7, 0, 0, 50)
	expected_blocks = []
	assert b0.time_ranges_overlapping_with(days, time_range) == expected_blocks
	
	days = DayOfWeek.list_from_string("TR")
	time_range = TimeRange.normalize(6, 0, 0, 50)
	assert b0.time_ranges_overlapping_with(days, time_range) == expected_blocks
	
	time_range = TimeRange.normalize(6, 0, 0, 150)
	expected_blocks = [TimeRange.normalize(7, 0, 0, 100)]
	assert b0.time_ranges_overlapping_with(days, time_range) == expected_blocks
	
	time_range = TimeRange.normalize(8, 40, 0, 75)
	assert b0.time_ranges_overlapping_with(days, time_range) == expected_blocks
	
	time_range = TimeRange.normalize(8, 50, 0, 75)
	expected_blocks = []
	assert b0.time_ranges_overlapping_with(days, time_range) == expected_blocks
	assert b1.time_ranges_overlapping_with(days, time_range) == expected_blocks
	assert b4.time_ranges_overlapping_with(days, time_range) == expected_blocks
	
	days = DayOfWeek.list_from_string("MWF")
	time_range = TimeRange.normalize(7, 0, 0, 50)
	assert b2.time_ranges_overlapping_with(days, time_range) == expected_blocks
	
	time_range = TimeRange.normalize(8, 0, 0, 50)
	expected_blocks = [TimeRange.normalize(8, 10, 0, 50)]
	assert b2.time_ranges_overlapping_with(days, time_range) == expected_blocks
	
	days = DayOfWeek.list_from_string("TR")
	time_range = TimeRange(start=time(hour=7), end=time(hour=16))
	expected_blocks = [TimeRange.normalize(7, 0, 0, 100)]
	assert b0.time_ranges_overlapping_with(days, time_range) == expected_blocks
	
	expected_blocks = [TimeRange.normalize(11, 0, 0, 100)]
	assert b1.time_ranges_overlapping_with(days, time_range) == expected_blocks
	
	expected_blocks = [TimeRange.normalize(13, 45, 0, 75)]
	assert b4.time_ranges_overlapping_with(days, time_range) == expected_blocks
	
	expected_blocks = [TimeRange.normalize(7, 0, 1, 15), TimeRange.normalize(11, 0, 1, 15)]
	assert b3.time_ranges_overlapping_with(days, time_range) == expected_blocks
	
	days = DayOfWeek.list_from_string("T")
	expected_blocks = [TimeRange.normalize(7, 0, 1, 15)]
	assert b3.time_ranges_overlapping_with(days, time_range) == expected_blocks
	
	days = DayOfWeek.list_from_string("R")
	expected_blocks = [TimeRange.normalize(11, 0, 1, 15)]
	assert b3.time_ranges_overlapping_with(days, time_range) == expected_blocks

def test_get_finalized_weight():
	c0_weight_per_section = course0.get_weight_per_section()
	c1_weight_per_section = course1.get_weight_per_section()
	
	b0 = copy(booking0)
	assert b0.get_finalized_weight() == 0
	b0.finalize()
	assert b0.get_finalized_weight() == c0_weight_per_section
	assert b0.get_finalized_weight(days=DayOfWeek.list_from_string("TR")) == c0_weight_per_section
	assert b0.get_finalized_weight(days=DayOfWeek.list_from_string("T")) == c0_weight_per_section / 2
	assert b0.get_finalized_weight(days=DayOfWeek.list_from_string("R")) == c0_weight_per_section / 2
	assert b0.get_finalized_weight(days=DayOfWeek.list_from_string("MWF")) == 0
	assert b0.get_finalized_weight(days=DayOfWeek.list_from_string("URS")) == c0_weight_per_section / 2
	assert b0.get_finalized_weight(days=DayOfWeek.list_from_string("MTW")) == c0_weight_per_section / 2
	assert b0.get_finalized_weight(days=[]) == 0
	
	b1 = copy(booking1)
	assert b1.get_finalized_weight() == 0
	b1.finalize()
	assert b1.get_finalized_weight() == c0_weight_per_section
	assert b1.get_finalized_weight(days=DayOfWeek.list_from_string("TR")) == c0_weight_per_section
	assert b1.get_finalized_weight(days=DayOfWeek.list_from_string("T")) == c0_weight_per_section / 2
	assert b1.get_finalized_weight(days=DayOfWeek.list_from_string("R")) == c0_weight_per_section / 2
	assert b1.get_finalized_weight(days=DayOfWeek.list_from_string("MWF")) == 0
	assert b1.get_finalized_weight(days=DayOfWeek.list_from_string("MTWRF")) == c0_weight_per_section
	assert b1.get_finalized_weight(days=DayOfWeek.list_from_string("URS")) == c0_weight_per_section / 2
	assert b1.get_finalized_weight(days=DayOfWeek.list_from_string("MTW")) == c0_weight_per_section / 2
	assert b1.get_finalized_weight(days=[]) == 0
	
	b2 = copy(booking2)
	assert b2.get_finalized_weight() == 0
	b2.finalize()
	assert b2.get_finalized_weight() == c1_weight_per_section
	assert b2.get_finalized_weight(days=DayOfWeek.list_from_string("MWF")) == c1_weight_per_section
	assert b2.get_finalized_weight(days=DayOfWeek.list_from_string("MW")) == c1_weight_per_section * 2 / 3
	assert b2.get_finalized_weight(days=DayOfWeek.list_from_string("F")) == c1_weight_per_section / 3
	assert b2.get_finalized_weight(days=DayOfWeek.list_from_string("TR")) == 0
	assert b2.get_finalized_weight(days=DayOfWeek.list_from_string("T")) == 0
	assert b2.get_finalized_weight(days=DayOfWeek.list_from_string("MTWRF")) == c1_weight_per_section
	assert b2.get_finalized_weight(days=DayOfWeek.list_from_string("UMT")) == c1_weight_per_section / 3
	assert b2.get_finalized_weight(days=DayOfWeek.list_from_string("MTW")) == c1_weight_per_section * 2 / 3
	assert b2.get_finalized_weight(days=[]) == 0
	
	b3 = copy(booking3)
	assert b3.get_finalized_weight() == 0
	b3.finalize()
	assert b3.get_finalized_weight() == c1_weight_per_section
	assert b3.get_finalized_weight(days=DayOfWeek.list_from_string("TR")) == c1_weight_per_section
	assert b3.get_finalized_weight(days=DayOfWeek.list_from_string("T")) == c1_weight_per_section / 2
	assert b3.get_finalized_weight(days=DayOfWeek.list_from_string("R")) == c1_weight_per_section / 2
	assert b3.get_finalized_weight(days=DayOfWeek.list_from_string("MWF")) == 0
	assert b3.get_finalized_weight(days=DayOfWeek.list_from_string("MTWRF")) == c1_weight_per_section
	assert b3.get_finalized_weight(days=DayOfWeek.list_from_string("URS")) == c1_weight_per_section / 2
	assert b3.get_finalized_weight(days=DayOfWeek.list_from_string("MTW")) == c1_weight_per_section / 2
	assert b3.get_finalized_weight(days=[]) == 0
	
	b4 = copy(booking4)
	assert b4.get_finalized_weight() == 0
	b4.finalize()
	assert b4.get_finalized_weight() == c1_weight_per_section
	assert b4.get_finalized_weight(days=DayOfWeek.list_from_string("TR")) == c1_weight_per_section
	assert b4.get_finalized_weight(days=DayOfWeek.list_from_string("T")) == c1_weight_per_section / 2
	assert b4.get_finalized_weight(days=DayOfWeek.list_from_string("R")) == c1_weight_per_section / 2
	assert b4.get_finalized_weight(days=DayOfWeek.list_from_string("MWF")) == 0
	assert b4.get_finalized_weight(days=DayOfWeek.list_from_string("MTWRF")) == c1_weight_per_section
	assert b4.get_finalized_weight(days=DayOfWeek.list_from_string("URS")) == c1_weight_per_section / 2
	assert b4.get_finalized_weight(days=DayOfWeek.list_from_string("MTW")) == c1_weight_per_section / 2
	assert b4.get_finalized_weight(days=[]) == 0

def test_restrictions_overlap():
	r0 = Restriction(json_loads('''
		{
			"type": 1,
			"contents":
			[
				"MA-101", "MA-104", "FA-102", "FA-105", "LT-103", "LT-203"
			]
		}
	'''))
	r1 = Restriction(json_loads('''
		{
			"type": 2,
			"contents":
			[
				[
					"MS-*"
				],
				[
					"CH-103", "CH-104", "MA-103", "MA-104", "PH-201", "PH-202", "ER-*"
				],
				[
					"IN-200"
				]
			]
		}
	'''))

	b0 = copy(booking0)
	b1 = copy(booking1)
	b2 = copy(booking2)
	b3 = copy(booking3)
	b4 = copy(booking4)
	b5 = copy(booking5)
	b6 = copy(booking6)
	
	restriction_list = [r0, r1]
	
	bookings = []
	for b in [b0, b1, b2, b3, b4 ,b5, b6]:
		assert not b.restrictions_overlap(restriction_list, bookings)
	
	bookings = [b3]
	assert b0.restrictions_overlap(restriction_list, bookings)
	assert b1.restrictions_overlap(restriction_list, bookings)
	
	bookings = [b0]
	assert b3.restrictions_overlap(restriction_list, bookings)
	
	bookings = [b1]
	assert b3.restrictions_overlap(restriction_list, bookings)
	
	bookings = [b6]
	assert not b1.restrictions_overlap(restriction_list, bookings)
	
	bookings = [b1]
	assert not b6.restrictions_overlap(restriction_list, bookings)
	
	bookings = [b6]
	assert not b0.restrictions_overlap(restriction_list, bookings)
	assert not b1.restrictions_overlap(restriction_list, bookings)
	
	bookings = [b0, b1]
	assert not b6.restrictions_overlap(restriction_list, bookings)