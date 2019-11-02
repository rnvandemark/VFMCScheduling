from tkinter import Frame, Button, Label, messagebox
from PIL import Image
from PIL.ImageTk import PhotoImage
from functools import partial

from ui.page_panel import PagePanel
from ui.course_input_page import CourseInputPage
from ui.professor_input_page import ProfessorInputPage
from ui.classroom_input_page import ClassroomInputPage
from ui.restriction_input_page import RestrictionInputPage
from ui.generation_page import GenerationPage

class GUI(Frame):
	
	def __init__(self, *args, **kwargs):
		Frame.__init__(self, *args, **kwargs)
		
		background_image = PhotoImage(
			Image.open("./resources/vfmc_logo.png").resize((400, 200), Image.ANTIALIAS))
		background_label = Label(image=background_image)
		background_label.image = background_image
		background_label.pack(fill="x")
		
		nav_frame = Frame(self)
		nav_frame.pack(side="top", fill="y")
		
		ip_list = [CourseInputPage(), ProfessorInputPage(), ClassroomInputPage(), RestrictionInputPage()]
		for ip in ip_list:
			ip.place_(in_=self)
		
		self.generation_p = GenerationPage()
		self.generation_p.place_(in_=self)
		
		self.parent_root = args[0]
		self.parent_root.protocol("WM_DELETE_WINDOW", self.on_kill)
		
		page_panel = PagePanel([*ip_list, self.generation_p], self)
		page_panel.pack(side="top", fill="both", expand=True)
		
		for ip in ip_list:
			Button(
				nav_frame,
				text="Input %s Data" % ip.data_type,
				command=partial(page_panel.show, ip)
			).pack(side="left")
		
		Button(nav_frame, text="Generate a Schedule", command=partial(page_panel.show, self.generation_p)).pack(side="left")
		
		page_panel.hide()
	
	def on_kill(self):
		self.bell()
		if messagebox.askokcancel("Quit", "Are you sure you want to quit?"):
			self.generation_p.kill_generation_request_thread()
			self.parent_root.destroy()