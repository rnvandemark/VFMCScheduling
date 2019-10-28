from enum import Enum

class RestrictionType(Enum):
	SINGLE_GROUP = 1
	MULTIPLE_GROUPS = 2

class Restriction():
	
	def __init__(self, json_obj):
		self.type = RestrictionType(json_obj["type"])
		self.contents = json_obj["contents"]
	
	def can_overlap_with(self, course_code0, course_code1):
		if course_code0 == course_code1:
			return True
		
		if self.type == RestrictionType.SINGLE_GROUP:
			return not (
				Restriction.course_is_in(course_code0, self.contents)
					and Restriction.course_is_in(course_code1, self.contents)
			)
		
		elif self.type == RestrictionType.MULTIPLE_GROUPS:
			num_groups = len(self.contents)
			for i in range(num_groups):
				if Restriction.course_is_in(course_code0, self.contents[i]):
					for j in range(num_groups):
						if i == j:
							continue
						
						if Restriction.course_is_in(course_code1, self.contents[j]):
							return False
			
			return True
		else:
			raise ValueError("Can't process for invalid restriction type: {0}".format(self.type))
	
	def restricts(self, course_code):
		if self.type == RestrictionType.SINGLE_GROUP:
			return course_code in self.contents
		elif self.type == RestrictionType.MULTIPLE_GROUPS:
			return any(course_code in g for g in self.contents)
		else:
			raise ValueError("Can't process for invalid restriction type: {0}".format(self.type))
	
	@staticmethod
	def course_is_in(course, restricted_courses):
		for c in restricted_courses:
			if c.endswith("-*"):
				if course.startswith(c[:c.index("-*")+1]):
					return True
			elif c == course:
				return True
		return False
	
	@staticmethod
	def can_overlap(restriction_list, course_code0, course_code1):
		return all(r.can_overlap_with(course_code0, course_code1) for r in restriction_list)
	
	@staticmethod
	def is_restricted(restriction_list, course_code):
		return any(r.restricts(course_code) for r in restriction_list)