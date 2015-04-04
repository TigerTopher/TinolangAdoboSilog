# CS 140 MP1: The Next Iron Chef
# This Project uses Python 2.7
# Team Cypher-VizVille

# Christopher Vizcarra 2013-58235
# Cyan Villarin 2013-10940

from Tkinter import * 		# For python version 2.7 only.
from tkFileDialog import * 	# For built-in Tkinter file dialogs.
import ScrolledText 		# For scrolledText widget used in messaging, statuses and deletion.

class Stove():
	def __init__(self):
		self.current = []
		self.isHotVar = False
		self.isCleanVar = True
		self.isOccupiedVar = False

	def cook(self, newDish):
		if (self.isHotVar == True) and (self.isCleanVar == True) and (isOccupiedVar == False):
			
			self.current.append(newDish)
			self.isOccupiedVar = True
			self.isCleanVar = False

			return True
		else:
			return False

	def remove(self):
		if(isOccupiedVar == False):		# Nothing was removed
			return False

		# If indeed there is...
		self.isOccupiedVar = False
		self.isHotVar = False
		self.isCleanVar = False

		return self.current.pop()

	def isOccupied(self):
		return self.isOccupiedVar

	def isHot(self):
		return self.isHotVar

	def isClean(self):
		return self.isCleanVar

	def preheat(self):
		self.isHotVar = True

	def clean(self):
		self.isCleanvar = True

class Scheduler():
	def __init__(self, dishWaiting):
		self.dishWaiting = dishWaiting
		self.time = 0

		#self.current = Dish()		# This is the current dish that is
		self.ourStove = Stove()
		self.ready = []				# This are the ones waiting for the stove
		self.preparing = []			# This are the ones in preparing state
		self.switching = False
		self.temporary = []

		# self.numAssistants = -1 	# -1 Indicates unlimited assistants. Unlimited assistants mean that there is no limit in number of dishes in preparing state

		self.remarks = ""

	def printStatus(self):
		print str(self.time) + " ," + self.current.name + " ," + str(self.current.time) + " ," + str(self.ready) + " ," + str(self.preparing) + " ," + self.remarks
		

	"""First come, first serve steps:
		
		Iterate time.

		1. Check all the dishes in dishWaiting. Check if there is an upcoming dish by matching the time of arrival with the current time.
			a. If it matches, assign the incoming dish: whether it goes to the preparation or to the ready state.
			

		2. PREPARATION
			a. Check if preparation is empty
			b. If not, iterate through the list, and subtract 1 in preparation timer. 
				-> If the current time is zero, pop its current instruction. Now check whether there is still an instruction.
					If there is, (transfer it to the ready state -if cooking yung next state)

		3. COOKING

			Check if the stove is occupied
				a. -- Empty:
					> Check if clean. 
						- Check if there is a dish in the temporary list or check if the stove is not clean. 
							If there is, we don't proceed to cooking
							> Set Stove to be clean
							> Remove the one in temporary list and assign in either prep or ready

						- Check if there is a ready dish.
							- If yes, check if the stove is warm.
								- If yes, transfer the dish to the cooking.
								- Change the state to occupied.


							- If not, preheat the stove... go to printing

						-> If not, proceed to printing....



				b. -- Occupied:
					Proceed. Subtract 1 time in the cook time of the current dish.
					See if the current dish's cook time is zero. 
						-> If it is zero, remove the respective instruction set.
							And see if there is still a remaining instruction.
							If there is still a remaining instruction put it in temporary list first.
							Remove it from cooking. Change the value to unoccupied.

							

						-> If not just proceed with printing

		-> Print Status
		-> Check if stove is empty and 
				 if ready is empty and
				 if preparation is empty and
				 if not switching [Context time switch] and
				 if dishWaiting is empty

				 -If all of these are satisfied, we now terminate.
				 [ Print status outside na lang to tell na tapos na]
	"""

	def FCFS(self):								# First come, First serve
		while self.dishWaiting != []:			# Here we have all this dish that haven't arrive yet.
			self.time = self.time + 1 			# This is our time variable that iterates
			for dish in self.dishWaiting:		# Iterates through all the dish in dishWaiting
				if dish.time == self.time:		# Checks if a dish's arrival time is equal to scheduler's time
					for inst in dish.instructions:		# Iterates through the instructions of a dish
						if inst[0] == "cook":
							self.ready.append(dish)		# If it is, append that dish to the ready queue
						elif inst[0] == "prep":
							self.preparing.append(dish)
				if self.preparing != []:				# Checks if the prep queue is empty
					for dish in self.preparing:			# Iterates through all the dishes in prep queue
						dish.instructions[0][1] = str(int(dish.instructions[0][1]) - 1)	# This should decrement prep time by 1, but it doesnt work
						if dish.instructions[0][1] == 0:	# Now, if prep time is 0
							dish.instructions.pop(0)		# Pop the current instruction
			if self.ourStove.isOccupied == False:
				if self.ourStove.isClean == True:
					pass
					# Huhuhu sorry Toph, naguguluhan talaga ako :(				

						

	def SJF(self):
		pass

	def Priority(self):
		pass

	def RoundRobin(self):
		pass

	def MultiQueue(self):
		pass
		
	def run():
		pass
		
class Dish():
	def __init__(self):
		self.name = ""
		self.time = 0
		self.priority = 0
		self.instructions = []

	def setName(self, newName):
		self.name = newName

	def setTime(self, newTime):
		self.time = newTime

	def setPriority(self, newPriority):
		self.priority = newPriority

	def getName(self):
		return self.name

	def getTime(self):
		return self.time

	def getPriority(self):
		return self.priority

	def enqueue(self, procedure, time):
		self.instructions.append([procedure,time])

	def dequeue(self):
		return self.instructions.pop()

	def showQueue(self):
		return self.instructions

class Iron_Chef():
	def __init__(self):
		self.dishAtStove = ""		
		self.dishWaiting = []

	def readFile(self):
	
		"""TASKLIST READING and RECIPE READING:
		Read file includes reading tasklist, reading recipes
		If a tasklist has a formatting error, we terminate.
		If a recipe file is missing, we ommit that dish in dishes to be cooked"""

		f = open("tasklist.txt", "r")					

		for lineList in f.readlines():					# Iterate through all the lines in the file
			dish = Dish()								# Instantiate Dish Class.

			lineList = lineList.strip("\n")				#Remove /n per line
			singleLine = lineList.split(" ")			#Separate the line into two elements [name and time respectively]

			#Putting it as dish attributes...
			dish.setName(singleLine[0])					
			dish.setTime(int(singleLine[1]))			#Typecast since time is char initially

			#Append the object in the dishWaiting list
			self.dishWaiting.append(dish)

		f.close()


		for x in range(0, len(self.dishWaiting)):		#Iterate throughout all the dishes declared at tasklist

			dishFilename = self.dishWaiting[x].getName()
			dishFilename = dishFilename + ".txt"		
			f = open(dishFilename, "r")
			
			temp = f.readline()							#Temp would hold the priority value
			temp = ((temp.strip("\n")).split(" "))[1]
		
			self.dishWaiting[x].setPriority(temp)		#Put Priority into respective object

			for instruction in f.readlines():			#Parse instructions, put the instructions into the object
				instruction = (instruction.strip("\n")).split(" ")
				self.dishWaiting[x].enqueue(instruction[0], instruction[1])

			f.close()

	def start(self):

		self.readFile()
		b = Scheduler(self.dishWaiting)
		b.FCFS()

		"""TEST PRINTING IF DISH WORKED
		for dish in self.dishWaiting:
			print "Dish Name: ", dish.getName()
			print "Dish Time: ", dish.getTime()
			print "Dish Priority: ", dish.getPriority()
			print "Instructions:"
			print dish.showQueue()
		"""

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


ironChefInstance = Iron_Chef()
ironChefInstance.start()			#Read file ka muna

