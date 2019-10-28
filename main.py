def main():
	import logging
	logging.basicConfig(
		filename='log/scheduling.log',
		format='%(asctime)s:%(levelname)s:%(message)s',
		level=logging.INFO
	)
	logging.info("Program started.")
	
	#
	# Start Testing/Debug Code
	#
	
	from src.scheduling import Scheduler
	scheduler = Scheduler("FA19_courses", "FA19_professors", "FA19_classrooms", "FA19_restrictions")
	schedule = scheduler.plan()
	
	from src.booking import Booking
	
	def do_sort(b):
		return (b[0], b[1].name, b[2], b[3].code)
		
	prof_list = list(schedule.keys())
	prof_list.sort(key=lambda p : (p.last_name, p.first_name))
	for prof in prof_list:
		all_blocks = []
		
		for booking in schedule[prof]:
			for block in booking.blocks:
				all_blocks.append((block[0], booking.element, booking.section_number, block[1]))
		
		all_blocks.sort(key=do_sort)
		
		print("{0} ({1}, {2})".format(
			prof.get_stylized_name(),
			Booking.get_total_finalized_credits_for(schedule, prof),
			Booking.get_total_finalized_weight_for(schedule, prof)
		))
		for t in all_blocks:
			print("\t{0} ({1}), section #{2}".format(t[1].name, t[1].as_programmatic_string(), t[2]))
			print("\t\t{0}: {1}".format(str(t[3]), str(t[0])))
		print()
	
	objective = sum(len(b) for b in schedule.values())
	actual = sum(c.section_count + (c.lab.section_count if c.lab else 0) for c in scheduler.courses_in_registrar)
	print("Objective sections to book: {0}\nActual sections booked: {1}\n{2}".format(
		objective,
		actual,
		"SUCCESS!" if objective == actual else "FAILURE!!!"
	))
	
	#
	# End Testing/Debug Code
	#
	
	logging.info("Program terminated.")

if __name__ == "__main__":
	main()