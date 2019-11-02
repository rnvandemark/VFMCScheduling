from tkinter import Scrollbar, StringVar
from Pmw import Balloon

from ui.base_page import BasePage
from ui.base_input_page import BaseInputPage
from src.restriction import RestrictionType

class RestrictionInputPage(BaseInputPage):
	
	def __init__(self, *args, **kwargs):
		BaseInputPage.__init__(self, "Restriction", *args, **kwargs)
		
		self.type_options = {t.pretty_print():t.value for t in RestrictionType}
		type_options_list = list(self.type_options.keys())
		self.type_var = StringVar(self.input_widgets_frame)
		_, _, type_menu = BasePage.get_labeled_input_field(
			self.input_widgets_frame,
			"Restriction Type",
			"OptionMenu",
			self.type_var,
			*type_options_list,
			required=True)
		self.input_widget_descriptors.append((type_menu, self.type_var, type_options_list[0]))
		
		self.single_group_var = StringVar(self.input_widgets_frame)
		single_group_frame, _, self.single_group_entry = BasePage.get_labeled_input_field(
			self.input_widgets_frame,
			"Single Group Course Codes",
			"Entry",
			f_pady=15,
			textvariable=self.single_group_var,
			required=True)
		self.input_widget_descriptors.append((self.single_group_entry, self.single_group_var, ""))
		
		multiple_groups_frame, _, self.multiple_groups_text = BasePage.get_labeled_input_field(
			self.input_widgets_frame,
			"Multiple Groups Course Codes",
			"Text",
			f_expand=True,
			l_side="top",
			l_fill="x",
			i_side="top",
			i_fill="x",
			i_expand=True,
			width=40,
			height=8,
			wrap="none",
			required=True)
		self.input_widget_descriptors.append((self.multiple_groups_text, None, ""))
		
		#text_yscrollbar = Scrollbar(multiple_groups_frame, orient="vertical")
		#self.multiple_groups_text["yscrollcommand"] = text_yscrollbar.set
		#text_yscrollbar.config(command=self.multiple_groups_text.yview)
		#text_yscrollbar.pack(side="right", fill="y")
		
		text_xscrollbar = Scrollbar(multiple_groups_frame, orient="horizontal")
		self.multiple_groups_text["xscrollcommand"] = text_xscrollbar.set
		text_xscrollbar.config(command=self.multiple_groups_text.xview)
		text_xscrollbar.pack(side="bottom", fill="x")
		
		Balloon(self).bind(
			single_group_frame,
			"""
				Enter a list of comma-seperated course codes for courses that should\n
				not be taught at the same time and day, and please include a hyphen\n
				between the department code and the course number. For example, if\n
				MA101, MA104, PH101, and PH201 should not be ran in parallel, then input\n
				could look like \"MA-101,MA-104,PH-101,PH-201\" (spaces before or after\n
				each comma are optional).
			""".replace("\n\t", "").replace("\t", "")
		)
		
		Balloon(self).bind(
			multiple_groups_frame,
			"""
				Enter a list of comma-seperated and new-line-seperated course codes for groups of courses\n
				that should not be taught at the same time and day, but the courses within a group can be\n
				taught in parallel, and please include a hyphen between the department code and the course\n
				number, and start each group on a new line. For example, if:PNL
				1.) MA101, MA201, and MA301 are allowed to run in parallelPNL
				2.) But none of those should run at the same time and day as MS301, MS302, MS303, or MS304,\n
				      even though each of those MS courses are allowed to run in parallelPNL
				3.) And neither of those two groups should run in parallel with ANY engineering coursePNL
				PNL
				Then input could look like:PNL
				MA-101,MA-201,MA-301PNL
				MS-301,MS-302,MS-303,MS-304PNL
				ER-*PNL
				PNL
				(Spaces before or after each comma are optional.)
			""".replace("\n\t", "").replace("\t", "").replace("PNL", "\n")
		)
		
		self.type_var.trace("w", self.update_widget_states)
	
	def update_widget_states(self, *args):
		type_str = self.type_var.get()
		single_state_enabled = False
		multiple_state_enabled = False
		
		if type_str == RestrictionType.SINGLE_GROUP.pretty_print():
			single_state_enabled = True
		elif type_str == RestrictionType.MULTIPLE_GROUPS.pretty_print():
			multiple_state_enabled = True
		
		self.config_widget(self.single_group_entry, single_state_enabled)
		self.config_widget(self.multiple_groups_text, multiple_state_enabled)
	
	def validate_input(self):
		type_str = self.type_var.get()
		if type_str not in self.type_options:
			return False
		
		rows = None
		rt = RestrictionType(self.type_options[type_str])
		if rt == RestrictionType.SINGLE_GROUP:
			rows = [self.single_group_var.get()]
			if len(rows[0].strip()) == 0:
				return False
		elif rt == RestrictionType.MULTIPLE_GROUPS:
			rows = [r for r in self.multiple_groups_text.get(1.0, "end").split("\n") if len(r) > 0]
			if len(rows) == 1:
				return False
		
		elements = (e.strip() for r in rows for e in r.split(",") if len(e.strip()) > 0)
		for e in elements:
			if e.find("-") < 0:
				return False
			
			if e.find("-") != e.rfind("-"):
				return False
			
			dept_code, course_number = e.split("-")
			if (not dept_code) or (not course_number):
				return False
			
			if course_number != "*":
				try:
					int(course_number)
				except:
					return False
		
		return True
	
	def objectify_input(self):
		rows = None
		rtv = self.type_options[self.type_var.get()]
		if rtv == RestrictionType.SINGLE_GROUP.value:
			rows = [e.strip() for e in self.single_group_var.get().split(",") if e.strip()]
		elif rtv == RestrictionType.MULTIPLE_GROUPS.value:
			rows = self.multiple_groups_text.get(0.0, "end").split("\n")
			rows = [[e.strip() for e in r.split(",") if e.strip()] for r in rows if len(r) > 0]
		
		return {
			"type": rtv,
			"contents": rows
		}
	
	def deobjectify_element(self, obj):
		type_obj = obj["type"]
		contents_obj = obj["contents"]
		
		self.type_var.set(RestrictionType(type_obj).pretty_print())
		
		self.multiple_groups_text.delete(1.0, "end")
		if type_obj == RestrictionType.SINGLE_GROUP.value:
			self.single_group_var.set(",".join(contents_obj))
		elif type_obj == RestrictionType.MULTIPLE_GROUPS.value:
			self.single_group_var.set("")
			self.multiple_groups_text.insert(
				"end",
				"\n".join(",".join(c) for c in contents_obj)
		 	)
	
	def stringify_element(self, obj):
		type_obj = obj["type"]
		contents_obj = obj["contents"]
		
		type_str = None
		contents_str = None
		if type_obj == RestrictionType.SINGLE_GROUP.value:
			type_str = "One Group"
			if len(contents_obj) > 5:
				contents_str = "%s..." % ",".join(c.replace("-", "") for c in contents_obj[:5])
			else:
				contents_str = ",".join(c.replace("-", "") for c in contents_obj)
		elif type_obj == RestrictionType.MULTIPLE_GROUPS.value:
			type_str = "%d Groups" % len(contents_obj)
			contents_str = ",".join(c[0].replace("-", "") + ("..." if len(c) > 1 else "") for c in contents_obj)
		else:
			raise ValueError("Unrecognized RestrictionType value: %d" % type_obj)
		
		return "%s: %s" % (type_str, contents_str)
	
	def refresh_inputs(self):
		self.update_widget_states()