from tkinter import Frame, Label, Button, Entry, OptionMenu, StringVar, END

from ui.base_page import BasePage

class BaseInputPage(BasePage):
	
	def __init__(self, data_type, *args, **kwargs):
		BasePage.__init__(self, *args, **kwargs)
		
		self.data_type = data_type
		
		options_frame = Frame(self)
		options_frame.pack(side="left", fill="x", expand=True)
		
		for s in ["Create New %s Set", "Edit Existing %s Set", "Copy Existing %s Set"]:
			Button(options_frame, text=s % self.data_type, command=None).pack(side="top")
		
		self.input_elements = []
	
	def clear_input_elements(self):
		for input_field_tuple in self.input_elements:
			if (type(input_field_tuple[0]) == Entry) and (not input_field_tuple[1]):
				input_field_tuple[0].delete(0, END)
				input_field_tuple[0].insert(0, input_field_tuple[2])
			else:
				input_field_tuple[1].set(input_field_tuple[2])
	
	@staticmethod
	def get_labeled_frame(master, name, input_field_type, *args, var=None, f_side="top", f_fill="y", f_expand=True):
		f = Frame(master)
		f.pack(side=f_side, fill=f_fill, expand=f_expand)
		
		l = Label(f, text=name)
		l.pack(side="left", fill="x")
		
		i = None
		v = var if var else StringVar(master)
		if input_field_type == "Entry":
			i = Entry(f, textvariable=v)
		elif input_field_type == "OptionMenu":
			i = OptionMenu(f, v, *args)
			v.set(args[0])
		
		i.pack(side="right", fill="x")
		
		return f, i, v