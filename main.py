import logging
from tkinter import Tk
from ui.gui import GUI
from ui.base_page import BasePage

def main():
	logging.basicConfig(
		filename="./log/scheduling.log",
		format="%(asctime)s:%(levelname)s:%(message)s",
		level=logging.INFO
	)
	
	root = Tk()
	BasePage.init_color_scheme(root, "#B88", "#DDD")
	
	gui = GUI(root)
	gui.pack(side="top", fill="both", expand=True)
	root.wm_geometry("1200x600")
	
	logging.info("Main Tkinter loop started.")
	root.mainloop()
	logging.info("Tkinter loop exited, program terminating.")

if __name__ == "__main__":
	main()