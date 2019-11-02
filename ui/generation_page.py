from tkinter import Frame, Label, Button, StringVar
from PIL import Image
from PIL.ImageTk import PhotoImage
from functools import partial
from threading import Thread, Lock
from time import sleep
import logging

from ui.base_page import BasePage
from src.scheduling import Scheduler
from src.excel_writer import ExcelWriter
from src.constants import GENERATION_CHECK_SLEEP_S

class GenerationPage(BasePage):
	
	def __init__(self, *args, **kwargs):
		BasePage.__init__(self, *args, **kwargs)
		
		main_frame = Frame(self, padx=5, pady=15)
		main_frame.pack(side="top", fill="both", expand=True)
		
		input_frame = Frame(main_frame, padx=15)
		input_frame.pack(side="left", fill="both", expand=True)
		
		self.course_var      = StringVar(main_frame)
		self.professor_var   = StringVar(main_frame)
		self.classroom_var   = StringVar(main_frame)
		self.restriction_var = StringVar(main_frame)
		
		for s, v in [
			("Courses", self.course_var),
			("Professors", self.professor_var),
			("Classrooms", self.classroom_var),
			("Restrictions", self.restriction_var)
		]:
			f, _, _ = BasePage.get_labeled_input_field(
				input_frame,
				"%s File" % s,
				"Entry",
				l_side="left",
				i_side="left",
				f_pady=8,
				i_padx=15,
				width=50,
				textvariable=v,
				required=True)
			
			i = PhotoImage(Image.open("./resources/folder.png").resize((30, 30), Image.ANTIALIAS))
			btn = Button(f, image=i, command=partial(self.select_file, v))
			btn.image = i
			btn.pack(side="left")
		
		generation_frame = Frame(main_frame)
		generation_frame.pack_propagate(0)
		generation_frame.config(height=100, width=200)
		generation_frame.pack(side="left", fill="both", expand=True)
		
		Button(generation_frame, text="Generate a random schedule!", command=self.do_generation).pack(side="top", expand=True)
		
		self.status_message_var = StringVar(generation_frame)
		self.status_message_label = Label(
			generation_frame,
			textvariable=self.status_message_var,
			wraplength=200
		)
		self.status_message_label.pack(side="top", fill="both", expand=True)
		self.clear_status_message()
		
		self.gen_urls = None
		self.gen_mutex = Lock()
		self.keep_gen_thread_alive = True
		self.gen_thread = Thread(target=self._do_generation_requests)
		self.gen_thread.start()
	
	def _do_generation_requests(self):
		while self.keep_gen_thread_alive:
			self.gen_mutex.acquire()
			try:
				if self.gen_urls:
					scheduler = None
					try:
						scheduler = Scheduler(*self.gen_urls[:4])
					except:
						logging.error("Failed to create scheduler object.")
						self.set_status_message("One of the four provided files caused an error!", "#F00")
						return
					
					self.set_status_message("Starting schedule generation...", "#090")
					logging.info("Generation attempt started...")
					
					schedule = scheduler.try_until_success()
					
					self.set_status_message("Generation succeeded! Saving...", "#090")
					logging.info("Generation succeeded, attempting to save file...")
					
					save_url = self.gen_urls[4]
					ExcelWriter.write_schedule(schedule, save_url)
					
					self.set_status_message("Finished exporting Excel spreadsheet!", "#090")
					logging.info("Excel sheet generation completed, saved to: %s" % save_url)
					
					self.gen_urls = None
			finally:
				self.gen_mutex.release()
			
			sleep(GENERATION_CHECK_SLEEP_S)
	
	def kill_generation_request_thread(self):
		self.keep_gen_thread_alive = False
	
	def set_status_message(self, msg, color):
		self.status_message_var.set(msg)
		self.status_message_label.config(fg=color)
	
	def clear_status_message(self):
		self.set_status_message("", "#000")
	
	def select_file(self, string_var):
		file_url = self.prompt_open_dialog()
		if file_url:
			string_var.set(file_url)
			self.clear_status_message()
		else:
			self.set_status_message("Bad file URL received!", "#F00")
	
	def do_generation(self):
		course_url      = self.course_var.get()
		professor_url   = self.professor_var.get()
		classroom_url   = self.classroom_var.get()
		restriction_url = self.restriction_var.get()
		
		if course_url and professor_url and classroom_url and restriction_url:
			save_url = self.prompt_save_dialog(
				title="Input Save Location and Name for Excel Sheet",
				filetypes=(("MS Excel files","*.xlsx"), ("all files","*.*")))
			if save_url:
				if self.gen_mutex.acquire(blocking=False):
					try:
						self.gen_urls = (course_url, professor_url, classroom_url, restriction_url, save_url)
					finally:
						self.gen_mutex.release()
			else:
				self.set_status_message("A file location and name is required to save the exported file!", "#F00")
		else:
			self.set_status_message("Make sure each of the four required files URLs are entered!", "#F00")