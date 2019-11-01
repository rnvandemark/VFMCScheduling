def main():
	import sys
	import logging
	logging.basicConfig(
		filename='log/scheduling.log',
		format='%(asctime)s:%(levelname)s:%(message)s',
		level=logging.INFO
	)
	logging.info("Program started.")
	
	MAIN_MODE = int(sys.argv[1]) if len(sys.argv) > 1 else 1
	
	#
	# Start Testing/Debug Code
	#
	
	schedule = None
	if (MAIN_MODE == 1) or (MAIN_MODE == 2):
		from src.scheduling import Scheduler
		scheduler = Scheduler("FA19_courses", "FA19_professors", "FA19_classrooms", "FA19_restrictions")
		schedule = scheduler.plan()
	
	if MAIN_MODE == 1:
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
	
	elif MAIN_MODE == 2:
		from src.excel_writer import ExcelWriter
		xlw = ExcelWriter()
		xlw.write_schedule(schedule)
		print("Done.    ")
	
	elif MAIN_MODE == 3:
		from tkinter import Tk
		from ui.gui import GUI
		from ui.base_input_page import BaseInputPage
		
		root = Tk()
		
		BaseInputPage.init_color_scheme(root, "#B88", "#DDD")
		
		gui = GUI(root)
		gui.pack(side="top", fill="both", expand=True)
		
		root.wm_geometry("1200x600")
		root.mainloop()
	
	#
	# End Testing/Debug Code
	#
	
	logging.info("Program terminated.")

if __name__ == "__main__":
	main()