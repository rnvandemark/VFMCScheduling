from tkinter import Frame, Label, Button, Entry, Listbox, Scrollbar, Text, StringVar
from PIL import Image
from PIL.ImageTk import PhotoImage
from functools import partial
from abc import ABC, abstractmethod
from json import load as json_load, dump as json_dump

from ui.base_page import BasePage
from ui.input_option_enum import InputOptionEnum

class BaseInputPage(BasePage, ABC):
	
	def __init__(self, data_type, *args, **kwargs):
		BasePage.__init__(self, *args, **kwargs)
		
		self.data_type = data_type
		
		options_frame = Frame(self)
		options_frame.pack(side="left", fill="x")
		
		self.current_filename = None
		self.current_filename_var = StringVar(options_frame)
		self.set_current_filename(None)
		Label(options_frame, textvariable=self.current_filename_var).pack(side="top")
		
		for i, s in enumerate(
			["Create New %s Set", "Edit Existing %s Set", "Copy Existing %s Set"],
			start=1
		):
			Button(
				options_frame,
				text=s%self.data_type,
				command=partial(self.handle_option_request, InputOptionEnum(i))
			).pack(side="top")
		
		error_frame = Frame(options_frame)
		error_frame.pack_propagate(0)
		error_frame.config(height=100, width=200)
		error_frame.pack(side="left", fill="x")
		
		self.error_message_var = StringVar(error_frame)
		self.clear_error_message()
		Label(
			error_frame,
			textvariable=self.error_message_var,
			fg="red",
			wraplength=200
		).pack(side="top", fill="both", expand=True)
		
		self.input_widgets_frame = Frame(self)
		self.input_widgets_frame.pack(side="left", fill="x", expand=True)
		
		elements_frame = Frame(self)
		elements_frame.pack(side="left", fill="x", expand=True)
		elements_yscrollbar = Scrollbar(elements_frame, orient="vertical")
		elements_xscrollbar = Scrollbar(elements_frame, orient="horizontal")
		self.elements_listbox = Listbox(
			elements_frame,
			selectmode="extended",
			xscrollcommand=elements_xscrollbar.set,
			yscrollcommand=elements_yscrollbar.set)
		elements_yscrollbar.config(command=self.elements_listbox.yview)
		elements_yscrollbar.pack(side="right", fill="y")
		elements_xscrollbar.config(command=self.elements_listbox.xview)
		elements_xscrollbar.pack(side="bottom", fill="x")
		self.elements_listbox.pack(side="right", fill="x", expand=True)
		
		action_btns_frame = Frame(self)
		action_btns_frame.pack(side="left", fill="x")
		
		element_btns_frame = Frame(action_btns_frame)
		element_btns_frame.pack(side="left", fill="x")
		
		page_btns_frame = Frame(action_btns_frame)
		page_btns_frame.pack(side="left", fill="x")
		
		for s, e, f in [
			("add", self.add_element, element_btns_frame),
			("pencil", self.edit_element, element_btns_frame),
			("trash_can", self.remove_element, element_btns_frame),
			("floppy_disk", self.write_elements, page_btns_frame),
			("exit", self.close_active_file, page_btns_frame)
		]:
			i = PhotoImage(Image.open("./resources/%s.png" % s).resize((35, 35), Image.ANTIALIAS))
			btn = Button(f, image=i, command=e)
			btn.image = i
			btn.pack(side="top", fill="y")
		
		self.input_widget_descriptors = []
		self.backing_elements_list = []
	
	def set_current_filename(self, filename):
		self.current_filename = filename
		if self.current_filename:
			self.current_filename_var.set(
				"Current Selection: %s" % self.current_filename[self.current_filename.rfind("/")+1:])
		else:
			self.current_filename = None
			self.current_filename_var.set("No filename is selected yet.")
	
	def set_error_message(self, msg):
		if not msg:
			msg = ""
		self.error_message_var.set(msg)
	
	def clear_error_message(self):
		self.set_error_message(None)
	
	def clear_input_widgets(self):
		for input_field_tuple in self.input_widget_descriptors:
			t = type(input_field_tuple[0])
			if t == Text:
				input_field_tuple[0].delete(1.0, "end")
				input_field_tuple[0].insert(1.0, input_field_tuple[2])
			elif ((t == Entry) and (input_field_tuple[1] is None)):
				input_field_tuple[0].delete(0, "end")
				input_field_tuple[0].insert(0, input_field_tuple[2])
			else:
				input_field_tuple[1].set(input_field_tuple[2])
	
	def handle_option_request(self, input_option):
		if input_option == InputOptionEnum.CREATE_NEW:
			self.set_current_filename(self.prompt_save_dialog())
			self.clear_error_message()
			
		elif input_option == InputOptionEnum.EDIT_EXISTING:
			desired_filename = self.prompt_open_dialog()
			if desired_filename:
				if self.load_elements_from(desired_filename):
					self.set_current_filename(desired_filename)
					self.clear_error_message()
				else:
					err_s = desired_filename[desired_filename.rfind("/")+1:]
					self.set_error_message("Loading data from %s was unsuccessful!" % err_s)
			else:
				self.set_error_message("Must select a valid file to open from!")
				
		elif input_option == InputOptionEnum.COPY_EXISTING:
			copy_from_filename = self.prompt_open_dialog(title="Select File to Copy From")
			if copy_from_filename:
				self.set_current_filename(self.prompt_save_dialog())
				if self.current_filename:
					if self.load_elements_from(copy_from_filename):
						self.write_elements()
						self.clear_error_message()
					else:
						err_s = copy_from_filename[copy_from_filename.rfind("/")+1:]
						self.set_error_message("Loading data from %s was unsuccessful!" % err_s)
				else:
					self.set_error_message("Must input a valid file to save to!")
			else:
				self.set_error_message("Must select a valid file to copy from!")
		else:
			raise ValueError("Unrecognized input option: %s" % str(input_option))
	
	def add_element(self, clear=False):
		if self.validate_input():
			o = self.objectify_input()
			self.backing_elements_list.append(o)
			self.elements_listbox.insert("end", self.stringify_element(o))
			self.clear_error_message()
			
			if clear:
				self.clear_input_widgets()
		else:
			self.set_error_message("Input is invalid! Ensure all required fields are completed properly.")
	
	def edit_element(self):
		current_selection = self.elements_listbox.curselection()
		if len(current_selection) > 0:
			i = int(current_selection[0])
			self.deobjectify_element(self.backing_elements_list[i])
			self.remove_element(at=i)
			self.refresh_inputs()
	
	def remove_element(self, at=None):
		indices = [at] if at else sorted((int(a) for a in self.elements_listbox.curselection()), reverse=True)
		for i in indices:
			self.elements_listbox.delete(i)
			del self.backing_elements_list[i]
	
	def close_active_file(self):
		self.write_elements()
		self.set_current_filename(None)
		self.backing_elements_list = []
		self.elements_listbox.delete(0, "end")
		self.clear_input_widgets()
		self.refresh_inputs()
	
	def load_elements_from(self, filename):
		try:
			with open(filename, "r") as f:
				self.backing_elements_list = json_load(f)
			
			self.elements_listbox.delete(0, "end")
			for o in self.backing_elements_list:
				self.elements_listbox.insert("end", self.stringify_element(o))
		except:
			return False
		
		return True
	
	def write_elements(self):
		if not self.current_filename:
			self.set_current_filename(self.prompt_save_dialog())
			if not self.current_filename:
				self.set_error_message("You must set a file location and name so you can save!")
				return
		
		with open(self.current_filename, "w+") as f:
			json_dump(self.backing_elements_list, f, indent=4)
	
	def show(self, in_=None):
		super().show(in_=in_)
		self.refresh_inputs()
	
	@abstractmethod
	def validate_input(self):
		raise NotImplementedError()
	
	@abstractmethod
	def objectify_input(self):
		raise NotImplementedError()
	
	@abstractmethod
	def deobjectify_element(self, obj):
		raise NotImplementedError()
	
	@abstractmethod
	def stringify_element(self, obj):
		raise NotImplementedError()
	
	@abstractmethod
	def refresh_inputs(self):
		raise NotImplementedError()