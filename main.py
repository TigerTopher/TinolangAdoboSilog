# CS 140 MP1: The Next Iron Chef
# This Project uses Python 2.7
# Team Cypher-VizVille

# Christopher Vizcarra 2013-58235
# Cyan Villarin 2013-10940

from Tkinter import * 		# For python version 2.7 only. Built-in GUI Module.
import copy					# For copy.deepcopy function - makes self.dishWaiting list uneditable by functions
import os 					# For os.system()

class Stove():
	def __init__(self):
		self.current = []
		self.isHotVar = False
		self.isCleanVar = True
		self.isOccupiedVar = False
		self.TQ = 0

	def getCurrentList(self):
		return self.current

	def decrTime(self):
		self.current[0][2] = self.current[0][2] - 1

	def getTime(self):
		if(self.current!= []):
			return self.current[0][2]
		else:
			return ""

	def getName(self):
		if(self.current != []):
			return self.current[0][0]
		else:
			return ""

	def cook(self, newDish):
		if (self.isHotVar == True) and (self.isCleanVar == True) and (self.isOccupiedVar == False):
			
			self.current.append(newDish)
			self.isOccupiedVar = True
			self.isCleanVar = False

			return True
		else:
			return False

	def remove(self):
		if(self.isOccupiedVar == False):		
			return False

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
		self.isCleanVar = True

class Scheduler():
	def __init__(self, dishWaiting):
		self.dishWaiting = dishWaiting
		self.time = 0
		self.ourStove = Stove()
		self.ready = []				
		self.preparing = []			
		self.temporary = []
		self.remarks = []

	def printStatus(self):

		print str(self.time) + "  | " + str(self.ourStove.getCurrentList()) + " | " + str(self.ready) + " | " + str(self.preparing) + " | ",
		for x in range(0, len(self.remarks)):
			if x == 0:
				print self.remarks[x],
			else:
				print ", " + self.remarks[x],
		print "\n"

	def printToFile(self, filePointer):
		filePointer.write(str(self.time) + ",")

		# Printing the Stove's Current
		if (self.ourStove.current != []):
			filePointer.write(self.ourStove.current[0][0] + "(" + self.ourStove.current[0][1] + "=" + str(self.ourStove.current[0][2]) + ")")
		else:
			filePointer.write("empty")
		filePointer.write(" ,")

		# Printing the Ready Queue
		if (self.ready != []):
			for x in self.ready:
				filePointer.write(x[0] + "(" + x[1] + "=" + str(x[2]) + ") ")
		else:
			filePointer.write("none ")
		filePointer.write(",")

		# Printing the Assistants Queue
		if (self.preparing != []):
			for x in self.preparing:
				filePointer.write(x[0] + "(" + x[1] + "=" + str(x[2]) + ") ")
			
		else:
			filePointer.write("none ")
		filePointer.write(",")

		# Printing the Remarks
		if (self.remarks != []):
			for x in self.remarks:
				filePointer.write(x + ". ")
		else:
			filePointer.write("---")

		filePointer.write("\n")

	def FCFS(self):						# First come, First serve
		self.time = 0
		# Open the file with append mode
		f = open("output.csv", "w")
		f.write("Time, Stove, Ready, Assistants, Remarks\n")

		while( (self.ourStove.isOccupied == True) or (self.ready != []) or (self.preparing != []) or (self.temporary != []) or (self.dishWaiting != [])):
			self.remarks = []
			self.time = self.time + 1

			# 1. Check all the dishes in dishWaiting. Check for arrival

			for i in range(0, len(self.dishWaiting)):

				# Check if there is an upcoming dish by matching the time of arrival with the current time.

				if (self.dishWaiting[i].getTime() == self.time) :
					
					#If it matches, assign the incoming dish: whether it goes to the preparation or to the ready state. (SEE INSTRUCTION)
					if(self.dishWaiting[i].showQueue != []):			#Check if there is an instruction

						# Messed up yung code, could be more efficient. Ayusin ko mamaya.

						temp = self.dishWaiting[i].dequeue()			#Temp is a list which holds our instruction
						temp.insert(0, self.dishWaiting[i].getName())	#Added the name
						# The last five lines were just for formatting. Temp contains the dish name, instruction, and time count

						if(temp[1] == "cook"):						#Go to ready state
							self.ready.append(temp)
							self.remarks.append(temp[0]+" is added to ready state")

						elif(temp[1] == "prep"):
							temp[2] == temp[2] + 1 				# We added this +1 because it will be subtracted in the preparation...
							self.preparing.append(temp)
							self.remarks.append(temp[0]+" is added to preparing")						
						

			
			#2. PREPARATION

			#a. Check if preparation is not empty

			if(self.preparing != []):

				#b. If not, iterate through the list, and subtract 1 in preparation timer.
				x = 0

				while( x < len(self.preparing)):
					self.preparing[x][2] = int(self.preparing[x][2]) - 1

					#-> If the current time is zero, pop its current instruction. Now check whether there is still an instruction.
					
					if self.preparing[x][2] == 0:
						nameToMatch = (self.preparing.pop(x))[0]
						
						# You have the name at temp[0] so you need to match this with dishWaiting para macheck kung may instructions pa
						# If there is, (transfer it to the ready state -if cooking yung next state)

						for y in range(0, len(self.dishWaiting)):
							# This asks kung saan yun at kung may kasunod pa na instruction...

							if( (self.dishWaiting[y].getName() == nameToMatch)):
								if self.dishWaiting[y].showQueue() == []:
									self.remarks.append(self.dishWaiting[y].getName() +" finished.")
									self.dishWaiting.pop(y)

								else:
									temp = self.dishWaiting[y].dequeue()
									temp.insert(0, self.dishWaiting[y].getName())
									if(temp[1] == "cook"):						#Go to ready state
										self.ready.append(temp)
										self.remarks.append(temp[0]+" is added to ready state")
									elif(temp[1] == "prep"):
										self.preparing.append(temp)				# No need to add 1 since no more deduction from preparation to be done
										self.remarks.append(temp[0]+" is added to preparation")
								break
						x = x - 1
					x = x + 1

			# COOKING
			if(self.temporary != []):
				#get name then match in dish waiting
				nameToMatch = self.temporary[0][0]
				self.temporary.pop(0)

				#Assign
				for y in range(0, len(self.dishWaiting)):
					if(self.dishWaiting[y].getName() == nameToMatch):
						name = self.dishWaiting[y].getName()
						if self.dishWaiting[y].showQueue() == []:
							self.dishWaiting.pop(y)
							self.remarks.append(name+" finished")

						else:
							temp = self.dishWaiting[y].dequeue()
							temp.insert(0,self.dishWaiting[y].getName())

							if(temp[1] == "cook"):						#Go to ready state
								self.ready.append(temp)
								self.remarks.append(temp[0]+" is added to ready state")

							elif(temp[1] == "prep"):
								self.preparing.append( temp)
								self.remarks.append(temp[0]+" is added to cooking state")

						break

			if(self.ourStove.isOccupied() == True):						#Occupied
				self.ourStove.decrTime()
				if ( self.ourStove.getTime() == 0):
					self.remarks.append(self.ourStove.getName() + " cooking ended")
					returned = self.ourStove.remove()
					#Check if there is still an instruction
					nameToFind = returned[0]
					match = 0

					for y in range(0, len(self.dishWaiting)):
						if( self.dishWaiting[y].getName() == nameToFind):
							if self.dishWaiting[y].showQueue() == []:
								name = self.dishWaiting[y].getName()
								self.dishWaiting.pop(y)
								self.remarks.append(name +" finished")
							else:
								match = 1

							break

					if(match == 1):
						self.temporary.append(returned)


			if(self.ourStove.isOccupied() == False):	#Empty

				if(self.ourStove.isClean() == False):	#Kung hindi siya clean.Edi
					self.ourStove.clean()
					self.remarks.append("Cleaning stove")
						
				else:								#Kung clean siya
					if(self.ready != []):
						if(self.ourStove.isHot() == True):
							newToCook = self.ready.pop(0)
							self.ourStove.cook(newToCook)		#This already sets it to occupied
							self.remarks.append("Started Cooking " + newToCook[0])
						else:
							self.ourStove.preheat()
							self.remarks.append("Preheating stove")

			# PRINTING IS HERE
			# self.printStatus()

			# Print to file
			self.printToFile(f)

		# Close the file	
		f.close()

	def RRTQ3(self):					# RoundRobin TQ = 3
		self.GenRR(3)
	
	def GenRR(self, TQ):				# Generalized Round Robin
		self.time = 0
		# Open the file with append mode
		f = open("output.csv", "w")
		f.write("Time, Stove, Ready, Assistants, Remarks\n")

		while( (self.ourStove.isOccupied == True) or (self.ready != []) or (self.preparing != []) or (self.temporary != []) or (self.dishWaiting != [])):
			self.remarks = []

			self.time = self.time + 1

			# 1. Check all the dishes in dishWaiting. Check for arrival

			for i in range(0, len(self.dishWaiting)):

				# Check if there is an upcoming dish by matching the time of arrival with the current time.

				if (self.dishWaiting[i].getTime() == self.time) :
					
					#If it matches, assign the incoming dish: whether it goes to the preparation or to the ready state. (SEE INSTRUCTION)
					if(self.dishWaiting[i].showQueue != []):			#Check if there is an instruction

						# Messed up yung code, could be more efficient. Ayusin ko mamaya.

						temp = self.dishWaiting[i].dequeue()			#Temp is a list which holds our instruction
						temp.insert(0, self.dishWaiting[i].getName())	#Added the name
						# This last five lines were just for formatting. Temp contains the dish name, instruction, and time count

						if(temp[1] == "cook"):						#Go to ready state
							self.ready.append(temp)
							self.remarks.append(temp[0]+" is added to ready state")

						elif(temp[1] == "prep"):
							temp[2] == temp[2] + 1 				# We added this +1 because it will be subtracted in the preparation...
							self.preparing.append(temp)
							self.remarks.append(temp[0]+" is added to preparing")						
						

			
			#2. PREPARATION

			#a. Check if preparation is not empty

			if(self.preparing != []):

				#b. If not, iterate through the list, and subtract 1 in preparation timer. 
				
				x = 0

				while(x < len(self.preparing)):
					self.preparing[x][2] = int(self.preparing[x][2]) - 1
					#-> If the current time is zero, pop its current instruction. Now check whether there is still an instruction.

					if self.preparing[x][2] == 0:
						nameToMatch = (self.preparing.pop(x))[0]

						# You have the name at temp[0] so you need to match this with dishWaiting para macheck kung may instructions pa
						# If there is, (transfer it to the ready state -if cooking yung next state)

						for y in range(0, len(self.dishWaiting)):
							# This asks kung saan yun at kung may kasunod pa na instruction...

							if( (self.dishWaiting[y].getName() == nameToMatch)):
								if self.dishWaiting[y].showQueue() == []:
									self.remarks.append(self.dishWaiting[y].getName() +" finished.")
									self.dishWaiting.pop(y)

								else:
									temp = self.dishWaiting[y].dequeue()
									temp.insert(0, self.dishWaiting[y].getName())
									if(temp[1] == "cook"):						#Go to ready state
										self.ready.append(temp)
										self.remarks.append(temp[0]+" is added to ready state")
									elif(temp[1] == "prep"):
										self.preparing.append(temp)				# No need to add 1 since no more deduction from preparation to be done
										self.remarks.append(temp[0]+" is added to preparation")
						
								break
						
						x = x - 1
					x = x + 1


			# COOKING
			# Check if the stove is occupied
			if(self.temporary != []):
				#Assign
				if (self.temporary[0][2] != 0):
					self.ready.append(self.temporary[0])
					self.temporary.remove(self.temporary[0])	
				else:
					#get name then match in dish waiting
					nameToMatch = self.temporary[0][0]
					self.temporary.pop(0)

					for y in range(0, len(self.dishWaiting)):
						if(self.dishWaiting[y].getName() == nameToMatch):
							name = self.dishWaiting[y].getName()
							if self.dishWaiting[y].showQueue() == []:
								self.dishWaiting.pop(y)
								self.remarks.append(name+" finished")

							else:
								temp = self.dishWaiting[y].dequeue()
								temp.insert(0, self.dishWaiting[y].getName())

								if(temp[1] == "cook"):						#Go to ready state
									self.ready.append(temp)
									self.remarks.append(temp[0]+" is added to ready state")

								elif(temp[1] == "prep"):
									self.preparing.append(temp)
									self.remarks.append(temp[0]+" is added to cooking state")

							break

			if(self.ourStove.isOccupied() == True):						#Occupied
				self.ourStove.decrTime()
				self.ourStove.TQ = self.ourStove.TQ + 1

				if ( self.ourStove.getTime() == 0):
					self.remarks.append(self.ourStove.getName() + " cooking ended")
					returned = self.ourStove.remove()
					#Check if there is still an instruction
					nameToFind = returned[0]
					match = 0

					for y in range(0, len(self.dishWaiting)):
						if( self.dishWaiting[y].getName() == nameToFind):
							if self.dishWaiting[y].showQueue() == []:
								name = self.dishWaiting[y].getName()
								self.dishWaiting.pop(y)
								self.remarks.append(name +" finished")
								self.ourStove.TQ = 0

							else:
								match = 1

							break

					if(match == 1):
						self.temporary.append(returned )

				elif ( self.ourStove.TQ == TQ):
					# Checks if TQ is reached. If it is, reset TQ = 0
					self.ourStove.TQ = 0

					# We are not sure automatically if we are going to pre-empt. Let's check ready first.
					if(self.ready != []):
					# Preempt the current dish, put to temp queue
						self.remarks.append(self.ourStove.getName() + " pre-empted.")
						toTemp = self.ourStove.remove()
						self.temporary.append(toTemp)


			if(self.ourStove.isOccupied() == False):
				if(self.ourStove.isClean() == False):	#Kung hindi siya clean. Possibleng mayroong nasa temporary
					self.ourStove.clean()
					self.remarks.append("Cleaning stove")

				else:								#Kung clean siya
					if(self.ready != []):
						if(self.ourStove.isHot() == True):
							newToCook = self.ready.pop(0)
							self.ourStove.cook(newToCook)		#This already sets it to occupied
							self.remarks.append("Started Cooking " + newToCook[0])
						else:
							self.ourStove.preheat()
							self.remarks.append("Preheating stove")



			# PRINTING IS HERE
			# self.printStatus()

			# Print to file
			self.printToFile(f)

		# Close the file	
		f.close()

	def SJF(self):						# Shortest Job First
		pass

	def Prio(self):						# Priority with Aging
		pass

	def Multi(self):					# Multiqueue
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

	def FCFS(self):
		dupli = copy.deepcopy(self.dishWaiting)
		b = Scheduler(list(dupli))
		b.FCFS()

	def RRTQ3(self):
		dupli = copy.deepcopy(self.dishWaiting)
		c = Scheduler(list(dupli))
		c.RRTQ3()

	def GenRR(self, TQ):
		dupli = copy.deepcopy(self.dishWaiting)
		d = Scheduler(list(dupli))
		d.GenRR(TQ)

	def SJF(self):
		dupli = copy.deepcopy(self.dishWaiting)
		e = Scheduler(list(dupli))
		e.SJF()

	def Prio(self):
		dupli = copy.deepcopy(self.dishWaiting)
		f = Scheduler(list(dupli))
		f.Prio()

	def Multi(self):
		dupli = copy.deepcopy(self.dishWaiting)
		g = Scheduler(list(dupli))
		g.Multi()

class GUI:
	def __init__(self):
		self.root = Tk()
		self.root.geometry("270x360")
		self.root.config(bg="LIGHTCYAN2")
		self.root.resizable(width=FALSE, height=FALSE)
		self.root.title("Iron Chef v1.03")

		self.chefInstance = Iron_Chef()
		self.chefInstance.start()

	def ButtonFCFS(self):
		self.chefInstance.FCFS()
		os.system("output.csv")

	def ButtonRRTQ3(self):
		self.chefInstance.RRTQ3()
		os.system("output.csv")

	def ButtonGenRR(self):
		self.chefInstance.GenRR(int(self.TQEntry.get()))
		os.system("output.csv")
		
	def ButtonSJF(self):
		self.chefInstance.SJF()
		os.system("output.csv")

	def ButtonPrio(self):
		self.chefInstance.Prio()
		os.system("output.csv")

	def ButtonMulti(self):
		self.chefInstance.Multi()
		os.system("output.csv")

	def show(self):
		# Upper border
		Up = Label(self.root, text="IRON CHEF", font=("Tahoma", 30, "bold"), bd=10, bg="DODGER BLUE", fg="LIGHTCYAN1")
		Up.pack(side=TOP, fill=X)

		# Center Frame
		MainFrame = Frame(self.root, bg="LIGHTCYAN1")
		MainFrame.pack(side=TOP)

		# Buttons
		FCFS = Button(MainFrame, text="First Come, First Serve", font=("Consolas", 11), cursor="hand2", relief=FLAT, bg="LIGHTCYAN2", command=lambda: self.ButtonFCFS())
		FCFS.pack(pady=5, padx=5, fill=X)

		RRTQ3 = Button(MainFrame, text="Round Robin (TQ = 3)", font=("Consolas", 11), cursor="hand2", relief=FLAT, bg="LIGHTCYAN2", command=lambda: self.ButtonRRTQ3())
		RRTQ3.pack(pady=5, padx=5, fill=X)

		# Frame of Generalized RR Button plus Input
		GerRREntryFrame = Frame(MainFrame, bg="LIGHTCYAN2")
		GerRREntryFrame.pack(pady=5, padx=5, fill=X)

		GenRR = Button(GerRREntryFrame, text="Generalized Round Robin", font=("Consolas", 11), cursor="hand2", relief=FLAT, bg="LIGHTCYAN2", command=lambda: self.ButtonGenRR())
		GenRR.pack(pady=5, padx=5, fill=X, side=LEFT)

		self.TQEntry = Entry(GerRREntryFrame, width=4, justify=CENTER, relief=FLAT, font=("Consolas", 11))
		self.TQEntry.pack(side=LEFT, pady=5, padx=5, fill=X,)
		self.TQEntry.focus_set()

		# Buttons again
		SJF = Button(MainFrame, text="Shortest Job First", font=("Consolas", 11), cursor="hand2", relief=FLAT, bg="LIGHTCYAN2", command=lambda: self.ButtonSJF())
		SJF.pack(pady=5, padx=5, fill=X)

		Prio = Button(MainFrame, text="Priority With Aging", font=("Consolas", 11), cursor="hand2", relief=FLAT, bg="LIGHTCYAN2", command=lambda: self.ButtonPrio())
		Prio.pack(pady=5, padx=5, fill=X)

		Multi = Button(MainFrame, text="Multiqueue", font=("Consolas", 11), cursor="hand2", relief=FLAT, bg="LIGHTCYAN2", command=lambda: self.ButtonMulti())
		Multi.pack(pady=5, padx=5, fill=X)

		# Lower border
		Down = Label(self.root, text="CS 140 MP1", font=("Tahoma", 13, "italic"), width=600, height=50, bg="DODGER BLUE", fg="LIGHTCYAN1")
		Down.pack(side=BOTTOM, fill=X)

		self.root.mainloop()

a = GUI()
a.show()			

