# CS 140 MP1: The Next Iron Chef
# This Project uses Python 2.7
# Team Cypher-VizVille

# Christopher Vizcarra 2013-58235
# Cyan Villarin

from Tkinter import * # For python version 2.7 only.
from tkFileDialog import * # For built-in Tkinter file dialogs.
import ScrolledText # For scrolledText widget used in messaging, statuses and deletion.

class Iron_Chef():
	def __init__(self):
		self.tasklist = "tasklist.txt"
		self.dishAtStove = "__empty__"		
		self.dishWaiting = []

class GUI:
	def __init__(self):
		self.root = Tk()
		self.root.geometry("600x400")
		self.root.config(bg="LIGHTCYAN2")
		self.root.resizable(width=FALSE, height=FALSE)
		self.root.title("Iron Chef v1.03")
		
	def show(self):
		Up = Label(self.root, text="I R O N  C H E F", font=("Tahoma", 30, "bold"), bd=10, bg="DODGER BLUE", fg="LIGHTCYAN1")
		Up.pack(side=TOP, fill=X, pady=(0,5))	

		Down = Frame(self.root, width=600, height=50, bg="DODGER BLUE")
		Down.pack(side=BOTTOM)
		
		mainFrame = Frame(self.root, bg="DODGER BLUE")
		mainFrame.pack(fill=X, pady=(0,5))
		
		timeFRAME = Frame(mainFrame, bg="DODGER BLUE")
		timeFRAME.pack(side=LEFT, padx=3, pady=5)
		timeL = Label(timeFRAME, text="Time", font=("Tahoma", 10, "bold"))
		timeL.pack(side=TOP, pady=1, fill=X)
		
		stoveFRAME = Frame(mainFrame, bg="DODGER BLUE")
		stoveFRAME.pack(side=LEFT, padx=20, pady=5)
		stoveL = Label(stoveFRAME, text="Stove", font=("Tahoma", 10, "bold"))
		stoveL.pack(side=TOP, pady=1, fill=X)
		
		readyFRAME = Frame(mainFrame, bg="DODGER BLUE")
		readyFRAME.pack(side=LEFT, padx=20, pady=5)
		readyL = Label(readyFRAME, text="Ready", font=("Tahoma", 10, "bold"))
		readyL.pack(side=TOP, pady=1, fill=X)

		assistantsFRAME = Frame(mainFrame, bg="DODGER BLUE")
		assistantsFRAME.pack(side=LEFT, padx=40, pady=5)
		assistantsL = Label(assistantsFRAME, text="Assistants", font=("Tahoma", 10, "bold"))
		assistantsL.pack(side=TOP, pady=1, fill=X)

		remarksFRAME = Frame(mainFrame, bg="DODGER BLUE")
		remarksFRAME.pack(side=LEFT, padx=40, pady=5)
		remarksL = Label(remarksFRAME, text="Remarks", font=("Tahoma", 10, "bold"))
		remarksL.pack(side=TOP, pady=1, fill=X)

		contentText = ScrolledText.ScrolledText(self.root, width=49, height=17, font=("Tahoma", 12), bd=5, bg="WHITE", relief=FLAT)
		contentText.pack(side=TOP, fill=X, pady=10, padx=5)
		contentText.insert(INSERT, "1   adobo etc etc WEW LAST NA LNG TO HIRAP PALA GAWIN LOL")
		contentText.config(state=DISABLED)

		self.root.mainloop()





window = GUI()
window.show()
