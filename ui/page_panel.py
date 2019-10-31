from tkinter import Frame

class PagePanel(Frame):
	
	def __init__(self, base_pages, *args, **kwargs):
		Frame.__init__(self, *args, **kwargs)
		
		self.base_pages = base_pages
		for bp in self.base_pages:
			bp.place_(in_=self)
	
	def bring_up(self, base_page):
		base_page.bring_up()
	
	def show(self, base_page):
		for bp in self.base_pages:
			if bp == base_page:
				bp.show(in_=self)
			else:
				bp.hide()
	
	def hide(self):
		self.show(None)