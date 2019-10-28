from xlsxwriter import Workbook

from src.booking import Booking

class ExcelWriter():
	
	@staticmethod
	def write_schedule(schedule, destination_file_name="/home/nick/Documents/test.xlsx"):
		wb = Workbook(destination_file_name)
		
		ws_professor = wb.add_worksheet("By Professor")
		ws_classroom = wb.add_worksheet("By Classroom")
		ws_course = wb.add_worksheet("By Course")
		
		section_title_format = wb.add_format({"bold": True})
		subsection_title_format = wb.add_format({"italic": True})
		
		#
		# Create the professor page
		#
		
		current_row = 0
		
		prof_list = list(schedule.keys())
		prof_list.sort(key=lambda p : (p.last_name, p.first_name))
		for prof in prof_list:
			prof_all_blocks = []
			
			ws_professor.merge_range(current_row, 0, current_row, 2, prof.get_stylized_name(), section_title_format)
			ws_professor.write(current_row, 3, Booking.get_total_finalized_credits_for(schedule, prof))
			ws_professor.write(current_row, 4, Booking.get_total_finalized_weight_for(schedule, prof))
			current_row = current_row + 1
			
			for booking in schedule[prof]:
				ws_professor.merge_range(current_row, 0, current_row, 2, booking.element.name, subsection_title_format)
				ws_professor.write(current_row, 3, booking.element.as_programmatic_string(), subsection_title_format)
				ws_professor.write(current_row, 4, "Sctn #%d" % booking.section_number)
				current_row = current_row + 1
				for block in booking.blocks:
					ws_professor.write(current_row, 1, block[1].code)
					ws_professor.merge_range(
						current_row,
						2,
						current_row,
						4,
						"%s, %s" % ("".join(d.value for d in block[0].days), block[0].time_range.pretty_print())
					)
					current_row = current_row + 1
			
			current_row = current_row + 1
		
		#
		# Create the classroom page
		#
		
		current_row = 0
		
		bookings_by_classroom = {}
		for prof_bookings in schedule.values():
			for booking in prof_bookings:
				for block in booking.blocks:
					if block[1] not in bookings_by_classroom:
						bookings_by_classroom[block[1]] = []
					bookings_by_classroom[block[1]].append((booking.element, booking.section_number, booking.professor, block[0]))
		
		for classroom, booking_elements in bookings_by_classroom.items():
			booking_elements.sort(key=lambda e: (e[3], e[0].name, e[1], e[2]))
			ws_classroom.merge_range(current_row, 0, current_row, 1, classroom.code, section_title_format)
			current_row = current_row + 1
			
			for e in booking_elements:
				ws_classroom.merge_range(current_row, 0, current_row, 2, e[0].name, subsection_title_format)
				ws_classroom.write(current_row, 3, e[0].as_programmatic_string(), subsection_title_format)
				ws_classroom.write(current_row, 4, "Sctn #%d" % e[1])
				ws_classroom.merge_range(current_row, 5, current_row, 7, e[2].get_stylized_name())
				ws_classroom.merge_range(
					current_row,
					8,
					current_row,
					10,
					"%s, %s" % ("".join(d.value for d in e[3].days), e[3].time_range.pretty_print())
				)
				current_row = current_row + 1
			
			current_row = current_row + 1
		
		#
		# Create the classroom page
		#
		
		current_row = 0
		
		bookings_by_course = {}
		for prof_bookings in schedule.values():
			for booking in prof_bookings:
				if booking.element not in bookings_by_course:
					bookings_by_course[booking.element] = []
				bookings_by_course[booking.element].append((booking.section_number, booking.professor, booking.blocks))
		
		element_list = list(bookings_by_course.keys())
		element_list.sort(key=lambda e : (e.dept_code, e.course_number))
		for element in element_list:
			ws_course.merge_range(current_row, 0, current_row, 2, element.name, section_title_format)
			ws_course.write(current_row, 3, element.as_programmatic_string(), section_title_format)
			current_row = current_row + 1
			
			booking_elements = bookings_by_course[element]
			booking_elements.sort(key=lambda e: e[0])
			for e in booking_elements:
				ws_course.write(current_row, 1, "Sctn #%d" % e[0])
				ws_course.merge_range(current_row, 2, current_row, 4, e[1].get_stylized_name())
				for b in e[2]:
					ws_course.merge_range(
						current_row,
						5,
						current_row,
						7,
						"%s, %s" % ("".join(d.value for d in b[0].days), b[0].time_range.pretty_print())
					)
					current_row = current_row + 1
			
			current_row = current_row + 1
		
		wb.close()