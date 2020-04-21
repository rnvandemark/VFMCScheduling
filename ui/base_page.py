from tkinter import Frame, Label, Button, Entry, OptionMenu, Checkbutton, Text, filedialog
from os import environ

class BasePage(Frame):
	
	COLOR_TEXT_ENABLED_BACKGROUND = None
	COLOR_ENABLED_BACKGROUND      = None
	COLOR_ENABLED_FOREGROUND      = None
	COLOR_DISABLED_BACKGROUND     = None
	COLOR_DISABLED_FOREGROUND     = None
	
	def __init__(self, *args, **kwargs):
		Frame.__init__(self, *args, **kwargs)
		self.last_dialog_dir = None
	
	def place_(self, in_=None, x=0, y=0, relwidth=1, relheight=1):
		self.place(in_=in_, x=x, y=y, relwidth=relwidth, relheight=relheight)
	
	def bring_up(self):
		self.lift()
	
	def show(self, in_=None):
		self.place_(in_=in_)
		self.bring_up()
	
	def hide(self):
		self.place_forget()
	
	def config_widget(self, w, enabled, **kwargs):
		kwargs["state"] = "normal" if enabled else "disabled"
		
		t = type(w)
		if (t == Text) or (t == OptionMenu):
			kwargs["fg"] = BasePage.COLOR_ENABLED_FOREGROUND if enabled else BasePage.COLOR_DISABLED_FOREGROUND
			if t == OptionMenu:
				kwargs["bg"] = BasePage.COLOR_ENABLED_BACKGROUND if enabled else BasePage.COLOR_DISABLED_BACKGROUND
			else:
				kwargs["bg"] = BasePage.COLOR_TEXT_ENABLED_BACKGROUND if enabled else BasePage.COLOR_DISABLED_BACKGROUND
		
		w.config(**kwargs)
	
	def get_prompt_initial_dir(self):
		return self.last_dialog_dir if self.last_dialog_dir else environ["HOME"]
	
	def issue_file_dialog(self, dialog_dir):
		if dialog_dir:
			last_index = dialog_dir.rfind("/")
			if last_index > 0:
				self.last_dialog_dir = dialog_dir[:last_index]
			else:
				self.last_dialog_dir = "/"
		
		return dialog_dir
	
	def prompt_open_dialog(
		self,
		initialdir=None,
		title="Select File to Open",
		filetypes=(("JSON files","*.json"), ("all files","*.*"))
	):
		if not initialdir:
			initialdir = self.get_prompt_initial_dir()
		return self.issue_file_dialog(filedialog.askopenfilename(
			initialdir=initialdir,
			title=title,
			filetypes=filetypes
		))
	
	def prompt_save_dialog(
		self,
		initialdir=None,
		title="Input Save Location and Filename",
		filetypes=(("JSON files","*.json"), ("all files","*.*"))
	):
		if not initialdir:
			initialdir = self.get_prompt_initial_dir()
		return self.issue_file_dialog(filedialog.asksaveasfilename(
			initialdir=initialdir,
			title=title,
			filetypes=filetypes
		))
	
	@staticmethod
	def init_color_scheme(root, disabled_bg, disabled_fg, text_enabled_bg="#FFF"):
		BasePage.COLOR_TEXT_ENABLED_BACKGROUND = text_enabled_bg
		BasePage.COLOR_ENABLED_BACKGROUND      = root["bg"]
		BasePage.COLOR_ENABLED_FOREGROUND      = "#000"
		BasePage.COLOR_DISABLED_BACKGROUND     = disabled_bg
		BasePage.COLOR_DISABLED_FOREGROUND     = disabled_fg
	
	@staticmethod
	def get_labeled_input_field(master, name, input_field_type, *args, **kwargs):
		f = Frame(master)
		f.pack(
			side=kwargs.pop("f_side", "top"),
			fill=kwargs.pop("f_fill", "y"),
			padx=kwargs.pop("f_padx", 0),
			pady=kwargs.pop("f_pady", 0),
			expand=kwargs.pop("f_expand", True))
		
		r = kwargs.pop("required", False)
		l = None
		if name:
			l = Label(f, text="%s%s: "%("*" if r else "",name))
			l.pack(
				side=kwargs.pop("l_side", "left"),
				fill=kwargs.pop("l_fill", "x"),
				padx=kwargs.pop("l_padx", 0),
				pady=kwargs.pop("l_pady", 0),
				expand=kwargs.pop("l_expand", False))
		
		i = None
		i_side = kwargs.pop("i_side", "right")
		i_fill = kwargs.pop("i_fill", "x")
		i_padx = kwargs.pop("i_padx", 0),
		i_pady = kwargs.pop("i_pady", 0),
		i_expand = kwargs.pop("i_expand", False)
		
		if input_field_type == "Entry":
			kwargs["bg"] = BasePage.COLOR_TEXT_ENABLED_BACKGROUND
			kwargs["fg"] = BasePage.COLOR_ENABLED_FOREGROUND
			kwargs["disabledbackground"] = BasePage.COLOR_DISABLED_BACKGROUND
			kwargs["disabledforeground"] = BasePage.COLOR_DISABLED_FOREGROUND
			i = Entry(f, *args, **kwargs)
			
		elif input_field_type == "OptionMenu":
			if len(args) < 2:
				raise ValueError("There must be at least one dropdown option, along with the linked variable.")
			args[0].set(args[1])
			i = OptionMenu(f, *args, **kwargs)
			
		elif input_field_type == "Button":
			i = Button(f, *args, **kwargs)
			i.image = kwargs.get("image")
			
		elif input_field_type == "Checkbutton":
			i = Checkbutton(f, *args, **kwargs)
			
		elif input_field_type == "Text":
			i = Text(f, *args, **kwargs)
			
		else:
			raise ValueError("Unsupported type of widget: %s" % input_field_type)
		
		i.pack(side=i_side, fill=i_fill, expand=i_expand, padx=i_padx, pady=i_pady)
		
		return f, l, i