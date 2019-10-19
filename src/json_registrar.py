import logging
from json import load as json_load

def input_json_name(name):
	return "./input_data/{0}.json".format(name)

class CourseRegistrar():
	
	def __init__(self, json_file_name):
		with open(input_json_name(json_file_name)) as json_file:
			self.course_list = json_load(json_file)
	
	def __str__(self):
		return str(self.course_list)

class ProfessorRegistrar():
	
	def __init__(self, json_file_name):
		with open(input_json_name(json_file_name)) as json_file:
			self.prof_list = json_load(json_file)
	
	def __str__(self):
		return "Professors:\n\t" + "\n\t".join([ProfessorRegistrar.get_stylized_name(prof) for prof in self.prof_list])
	
	@staticmethod
	def get_stylized_name(json_obj):
		name = json_obj["first_name"] + " "
		
		if "middle_name" in json_obj and len(json_obj["middle_name"]) != 0:
			name = name + json_obj["middle_name"] + " "
		
		return name + json_obj["last_name"]

class ClassroomRegistrar():
	
	def __init__(self, json_file_name):
		with open(input_json_name(json_file_name)) as json_file:
			self.room_list = json_load(json_file)
	
	def __str__(self):
		return str(self.room_list)

class RestrictionRegistrar():
	
	def __init__(self, json_file_name):
		with open(input_json_name(json_file_name)) as json_file:
			self.restriction_list = json_load(json_file)
	
	def __str__(self):
		return str(self.restriction_list)