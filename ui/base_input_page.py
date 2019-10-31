from tkinter import Frame, Label, Button, Entry, OptionMenu, Listbox, Scrollbar, StringVar, filedialog
from PIL import Image
from PIL.ImageTk import PhotoImage
from abc import ABC, abstractmethod
from functools import partial
from os import environ

from ui.base_page import BasePage
from ui.input_option_enum import InputOptionEnum

class BaseInputPage(BasePage, ABC):
	
	def __init__(self, data_type, *args, **kwargs):
		BasePage.__init__(self, *args, **kwargs)
		
		self.data_type = data_type
		
		options_frame = Frame(self)
		options_frame.pack(side="left", fill="x", expand=True)
		
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
		
		self.input_widgets_frame = Frame(self)
		self.input_widgets_frame.pack(side="left", fill="x", expand=True)
		
		elements_frame = Frame(self)
		elements_frame.pack(side="left", fill="x", expand=True)
		elements_scrollbar = Scrollbar(elements_frame, orient="vertical")
		self.elements_list = Listbox(elements_frame, yscrollcommand=elements_scrollbar.set)
		elements_scrollbar.config(command=self.elements_list.yview)
		elements_scrollbar.pack(side="right", fill="y")
		self.elements_list.pack(side="right", fill="x", expand=True)
		
		finalize_input_frame = Frame(self)
		finalize_input_frame.pack(side="left", fill="x", expand=True)
		
		finalize_input_btns_frame = Frame(finalize_input_frame)
		finalize_input_btns_frame.pack(side="left", fill="x", expand=True)
		
		for s, e in [
			("add", self.add_element),
			("trash_can", self.remove_element),
			("floppy_disk", self.write_elements),
			("exit", self.close_active_file)
		]:
			img = PhotoImage(Image.open("./resources/%s.png" % s).resize((35, 35), Image.ANTIALIAS))
			btn = Button(
				finalize_input_btns_frame,
				image=img,
				command=e)
			btn.image = img
			btn.pack(side="top", fill="y", expand=True)
		
		error_frame = Frame(finalize_input_frame)
		error_frame.pack_propagate(0)
		error_frame.config(height=100, width=100)
		error_frame.pack(side="left", fill="x")
		
		self.error_message = None
		self.error_message_var = StringVar(error_frame)
		self.clear_error_message()
		Label(
			error_frame,
			textvariable=self.error_message_var,
			fg="red",
			wraplength=100
		).pack(side="top", fill="both", expand=True)
		
		self.input_elements = []
	
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
	
	def clear_input_elements(self):
		for input_field_tuple in self.input_elements:
			if (type(input_field_tuple[0]) == Entry) and (not input_field_tuple[1]):
				input_field_tuple[0].delete(0, "end")
				input_field_tuple[0].insert(0, input_field_tuple[2])
			else:
				input_field_tuple[1].set(input_field_tuple[2])
	
	def handle_option_request(self, input_option):
		if input_option == InputOptionEnum.CREATE_NEW:
			self.set_current_filename(self.prompt_save_dialog())
			self.clear_error_message()
		elif input_option == InputOptionEnum.EDIT_EXISTING:
			self.set_current_filename(self.prompt_open_dialog())
			self.clear_error_message()
		elif input_option == InputOptionEnum.COPY_EXISTING:
			copy_from_filename = self.prompt_open_dialog()
			if copy_from_filename:
				self.set_current_filename(self.prompt_save_dialog())
				if self.current_filename:
					if self.parse_elements_from(copy_from_filename):
						self.clear_error_message()
					else:
						err_s = copy_from_filename[copy_from_filename.rfind("/")+1:]
						self.set_error_message("ERROR: Loading data from %s was unsuccessful!" % err_s)
				else:
					self.set_error_message("ERROR: Must input a valid file to save to!")
			else:
				self.set_error_message("ERROR: Must select a valid file to copy from!")
		else:
			raise NotImplementedError()
	
	def prompt_open_dialog(self):
		return filedialog.askopenfilename(
			initialdir=environ["HOME"],
			title="Select File",
			filetypes=(("JSON files","*.json"), ("all files","*.*")))
	
	def prompt_save_dialog(self):
		return filedialog.asksaveasfilename(
			initialdir=environ["HOME"],
			title="Select Directory and Filename",
			filetypes=(("JSON files","*.json"), ("all files","*.*")))
	
	def add_element(self):
		raise NotImplementedError()
	
	def remove_element(self):
		raise NotImplementedError()
	
	def close_active_file(self):
		self.write_elements()
		self.clear_input_elements()
		self.set_current_filename(None)
	
	@abstractmethod
	def stringify_element(self):
		raise NotImplementedError()
	
	@abstractmethod
	def write_elements(self):
		raise NotImplementedError()
	
	@abstractmethod
	def parse_elements_from(self, filename):
		raise NotImplementedError()
	
	@staticmethod
	def get_labeled_input_field(master, name, input_field_type, *args, **kwargs):
		f = Frame(master)
		f.pack(side=kwargs.pop("f_side", "top"), fill=kwargs.pop("f_fill", "y"), expand=kwargs.pop("f_expand", True))
		
		l = None
		if name:
			l = Label(f, text=name)
			l.pack(side=kwargs.pop("l_side", "left"), fill=kwargs.pop("l_fill", "x"), expand=kwargs.pop("l_expand", False))
		
		i = None
		i_side = kwargs.pop("i_side", "right")
		i_fill = kwargs.pop("i_fill", "x")
		i_expand = kwargs.pop("i_expand", False)
		
		if input_field_type == "Entry":
			i = Entry(f, *args, **kwargs)
		elif input_field_type == "OptionMenu":
			if len(args) < 1:
				raise ValueError("There must be at least one dropdown option.")
			args[0].set(args[1])
			i = OptionMenu(f, *args, **kwargs)
		elif input_field_type == "Button":
			i = Button(f, *args, **kwargs)
			i.image = kwargs.get("image")
		else:
			raise ValueError("Unrecognized type of widget: %s" % input_field_type)
		
		i.pack(side=i_side, fill=i_fill, expand=i_expand)
		
		return f, l, i