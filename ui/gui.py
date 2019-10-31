from tkinter import Frame, Button, Label
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
			Image.open("./resources/vfmc_logo.jpeg").resize((400, 200), Image.ANTIALIAS))
		background_label = Label(image=background_image)
		background_label.image = background_image
		background_label.pack(fill="x")
		
		nav_frame = Frame(self)
		nav_frame.pack(side="top", fill="y")
		
		ip_list = [CourseInputPage(), ProfessorInputPage(), ClassroomInputPage(), RestrictionInputPage()]
		for ip in ip_list:
			ip.place_(in_=self)
		
		generation_p = GenerationPage()
		generation_p.place_(in_=self)
		
		page_panel = PagePanel([*ip_list, generation_p], self)
		page_panel.pack(side="top", fill="both", expand=True)
		
		for ip in ip_list:
			Button(
				nav_frame,
				text="Input %s Data" % ip.data_type,
				command=partial(page_panel.show, ip)
			).pack(side="left")
		
		Button(nav_frame, text="Generate a Schedule", command=partial(page_panel.show, generation_p)).pack(side="left")
		
		page_panel.hide()