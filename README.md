# TinolangAdoboSilog
### Developed by TigerTopher - CyanVille

### Progress So Far: 
*See Readme.md. "+ -> Topher", "- -> Cyan" *


FCFS Algorithm
---
	"""First come, first serve steps:
		
		Iterate time.

		1. Check all the dishes in dishWaiting. Check if there is an upcoming dish by matching the time of arrival with the current time.
			a. If it matches, assign the incoming dish: whether it goes to the preparation or to the ready state.
				If it is to be put in the preparation state, note that the time should be incremented by 1. (it would be mistakenly decremented in preparation)

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

Arc 5
---
+ Finished FCFS
+ Output to output.csv completed

Arc 4
---
+ Added scheduler class
+ Instantiated Scheduler class inside Iron Chef class
+ Send dishwaiting as parameter
+ FCFS

Arc 3
---
+ Finished implementing in self.dishWaiting object. This includes name, arrival time, priority, and instructions(procedure, time)
+ Added Readfile for all other files.
+ Added Tiger Picture. (It's something >.<)
+ Revised Readfile for Tasklist.
- Added ReadFile() 

Arc 2
---
- Added main.py
- Removed aa_colors.py, a_git_guide.txt and aa_main.py
- Run aa_colors.py to see the choice of colors for GUI.
- Renamed Main.py to aa_main.py
- Initialized GUI Window (Difficult tho)

Arc 1
---
+ Added List Files
+ Edited README.md
+ Created Main

![alt text][logo]
[logo]: http://www.auburn.edu/cspd/promo/cd/images/tigereyes_big.gif "TigerTopher | CyanVille"
