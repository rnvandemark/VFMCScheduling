from tkinter import Frame

class BasePage(Frame):
	
	def __init__(self, *args, **kwargs):
		Frame.__init__(self, *args, **kwargs)
	
	def place_(self, in_=None, x=0, y=0, relwidth=1, relheight=1):
		self.place(in_=in_, x=x, y=y, relwidth=relwidth, relheight=relheight)
	
	def bring_up(self):
		self.lift()
	
	def show(self, in_=None):
		self.place_(in_=in_)
		self.bring_up()
	
	def hide(self):
		self.place_forget()