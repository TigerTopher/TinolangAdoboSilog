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


	def FCFS(self):								# First come, First serve
		self.time = 0


		while( (self.ourStove.isOccupied == True) or (self.ready != []) or (self.preparing != []) or (self.switching == True) or (self.dishWaiting != [])):
			self.time = self.time + 1
	
			# 1. Check all the dishes in dishWaiting.

			for i in range(0, len(self.dishWaiting)):

				# Check if there is an upcoming dish by matching the time of arrival with the current time.

				if (self.dishWaiting[i].getTime() == self.time) :
					
					#If it matches, assign the incoming dish: whether it goes to the preparation or to the ready state. (SEE INSTRUCTION)
					if(self.dishWaiting[i].showQueue != []):			#Check if there is an instruction

						# Messed up yung code, could be more efficient. Ayusin ko mamaya.

						temp1 = self.dishWaiting[i].dequeue()			#Temp is a list which holds our instruction
						temp1.insert(0, self.dishWaiting[i].getName())	#Added the name
						# This last five lines were just for formatting. Temp contains the dish name, instruction, and time count
						# print self.time, temp

						if(temp1[1] == "cook"):						#Go to ready state
							self.ready.insert(0, temp1)

						elif(temp1[1] == "prep"):
							temp1[2] == temp1[2] + 1 				# We added this +1 because it will be subtracted in the preparation...
							self.preparing.insert(0, temp1)
						

			
			#2. PREPARATION

			#a. Check if preparation is not empty

			if(self.preparing != []):

				#b. If not, iterate through the list, and subtract 1 in preparation timer. 
				for x in range(0, len(self.preparing)):
					print self.preparing[x][2]
					self.preparing[x][2] = int(self.preparing[x][2]) - 1

					#-> If the current time is zero, pop its current instruction. Now check whether there is still an instruction.
					
					if self.preparing[x][2] == 0:
						nameToMatch = (self.preparing.pop(x))[0]
						
						# You have the name at temp[0] so you need to match this with dishWaiting para macheck kung may instructions pa
						# If there is, (transfer it to the ready state -if cooking yung next state)

						for y in range(0, len(self.dishWaiting)):
							# This asks kung saan yun at kung may kasunod pa na instruction...
							if( (self.dishWaiting[y].getName() == nameToMatch) and (self.dishWaiting[y].showQueue != [] )):
								temp = self.dishWaiting[y].dequeue()
								temp.insert(0, self.dishWaiting[y].getName())

								if(temp[1][0] == "cook"):						#Go to ready state
									self.ready.insert(0, temp)

								elif(temp[1][0] == "prep"):
									self.preparing.insert(0, temp)				# No need to add 1 since no more deduction from preparation to be done


			# COOKING
			
			# Check if the stove is occupied
			
			#a. Empty
			if self.ourStove.isOccupied == False:

				# Check if the stove is clean
				if self.ourStove.isClean == False:

					# If not, set the stove to clean
					self.ourStove.isClean = True

				# Check if there is a dish in the temp list or check if the stove is not clean
				if self.temporary != []:

						# If there is, remove the one in temp list and assign to ready/prep queue
						for y in range(0, len(self.temporary)):
							# This asks kung saan yun at kung may kasunod pa na instruction...
							if( (self.temporary[y].getName() == nameToMatch) and (self.dishWaiting[y].showQueue != [] )):
								temp = self.temporary[y].dequeue()
								temp.insert(0, self.temporary[y].getName())

								if(temp[1][0] == "cook"):						#Go to ready state
									self.ready.insert(0, temp)

								elif(temp[1][0] == "prep"):
									self.preparing.insert(0, temp)	

				# If there are no more dish in the temp list, print
				else:
					self.printStatus()

				# Check if there is a ready dish
				if self.ready != []:

					# If there is a ready dish, check if stove is warm
					if self.ourStove.isHot == True:

						# If stove is hot, transfer dish to cook and change state to occupied
						self.ourStove.cook(self.ready[0])	# Not sure kung tama ito? Tranfer to cook
						self.ready.pop(0)					# So remove from ready list...
						self.ourStove.isOccupied = True

					# If there is none in the ready list
					else:
						# Preheat the stove, then print?
						self.ourStove.isHot = True
						self.printStatus()


			#b. Occupied
			elif self.ourStove.isOccupied == True:
				# Subtract 1 time in cook time of the current dish
				# Di ko sure saan ko kukunin ung cook time so dun na lng sa instruction set, or...
				# I think I missed something heheh
				self.ourStove.current[0].instructions[0][1] = int(self.ourStove.current[0].instructions[0][1]) - 1
				
				# Check if the cook time is 0
				if self.ourStove.current[0].instructions[0][1] == 0:
					# If it is 0, remove the instruction set
					self.ourStove.current[0].instructions.pop(0)

					# Check if there are still remaining instruction
					if self.ourStove.current[0].instructions != []:
						# If there is, put it in temporary list
						self.temporary.append(self.ourStove.current[0])
						# Remove it from cooking
						self.ourStove.remove()
						# Change the value to unoccupied
						self.ourStove.isOccupied = False
				# If it is not zero
				else:
					# Proceed with printing
					self.printStatus()

			# If the instruction is empty, we remove it in dishWaiting...
			for x in range(0, len(self.dishWaiting)):
				if(self.dishWaiting[x].showQueue == []):
					self.dishWaiting.pop(x)

						

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
		return self.instructions.pop(0)

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
				self.dishWaiting[x].enqueue(instruction[0], int(instruction[1]))

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

