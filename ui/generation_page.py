from tkinter import Label

from ui.base_page import BasePage

class GenerationPage(BasePage):
	
	def __init__(self, *args, **kwargs):
		BasePage.__init__(self, *args, **kwargs)
		
		l = Label(self, text="Example Generation Page!")
		l.pack()