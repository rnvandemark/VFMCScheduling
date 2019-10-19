from src.scheduling import Scheduler

def main():
	import logging
	logging.basicConfig(
		filename='log/scheduling.log',
		format='%(asctime)s:%(levelname)s:%(message)s',
		level=logging.INFO
	)
	logging.info("Program started.")
	
	scheduler = Scheduler("FA19_courses", "FA19_professors", "FA19_classrooms", "FA19_restrictions")
	schedule = scheduler.plan()
	
	from src.day_of_week import DayOfWeek
	
	def do_sort(e):
		return (e[3], e[0].as_programmatic_string(), e[1], e[2])
	
	day_map = DayOfWeek.get_empty_dict(dict)
	for b in schedule:
		for s in b.blocks:
			for d in s[0].days:
				if b.professor not in day_map[d]:
					day_map[d][b.professor] = []
				
				day_map[d][b.professor].append((
					b.course,
					b.section_number,
					s[1],
					s[0].time_range
				))
	
	for day, prof_maps in day_map.items():
		print("*****{0}******".format(str(day)))
		for prof, slots in prof_maps.items():
			slots.sort(key=do_sort)
			print("\t{0}".format(str(prof)))
			for slot in slots:
				print("\t\t{0}, section #{1}".format(slot[0].as_programmatic_string(), slot[1]))
				print("\t\t{0}, {1}".format(slot[2].code, str(slot[3])))
				print()
		print()
	
	logging.info("Program terminated.")

if __name__ == "__main__":
	main()