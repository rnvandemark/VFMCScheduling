class Professor():
	
	def __init__(self, json_obj):
		self.first_name  = json_obj["first_name"]
		self.middle_name = json_obj.get("middle_name")
		self.last_name   = json_obj["last_name"]
		self.departments = json_obj["departments"]
	
	def get_full_name(self):
		name = self.first_name + " "
		if self.middle_name:
			name = name + self.middle_name + " "
		return name + self.last_name
	
	def get_stylized_name(self):
		name = self.last_name + ", " + self.first_name
		if self.middle_name:
			name = name + " " + self.middle_name
		return name
	
	def __str__(self):
		return "\"{0}\"".format(self.get_stylized_name())