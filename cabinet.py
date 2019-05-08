#!/usr/bin/python
# -*- coding: utf-8 -*-

# import only system from os 
from os import system, name

# import all the UI elements
from Tkinter import Tk, Label, Button, Entry

# import sleep to show output for some time period 
from time import sleep

# define our clear function 
def clear(): 
    _ = system('clear') 

class GUI:
    def __init__(self, master):
        def updateList():
            for i in range(20):
                # automatic indenting so it all lines up and looks pretty
                numStr = str(i + 1)
                if len(drawers) > 9 and i < 9:
                    numStr = numStr + " "
                if len(drawers) > 99 and i < 99:
                    numStr = numStr + " "

                # translate 0 and 1 into readable text
                if drawers[i][0] == True:
                    lockState = "Locked"
                else:
                    lockState = "Unlocked"

                if drawers[i][1] == True:
                    openState = "Closed"
                else:
                    openState = "Open"

                labelList[i]['text'] = numStr + ": " + lockState + ", " + openState

        # testing stuff
        def entryInput(self):
            entryText = entry_box.get()
            entry_box.delete(0,len(entryText))
            entry_box.insert(0,"")

            action = entryText
            if action[:4] == "open":
                # number parsing
                drawerToOpen = ""
                # length will be 6 if single digit, 7 if double digit
                if len(action) == 7:
                    drawerToOpen = int(action[-2:]) # slicing magic
                else:
                    drawerToOpen = int(action[-1:]) # slicing magic
                drawerToOpen -= 1 # shift one because list starts at 0


                if drawers[drawerToOpen][0] == True:
                    print("Sorry, you can not open this drawer. It is locked.")
                    sleep(2)
                elif drawers[drawerToOpen][1] == False:
                    print("Sorry, you can not open this drawer. It is already open.")
                    sleep(2)
                else:
                    drawers[drawerToOpen][1] = False
                    if drawers[drawerToOpen][4] == False:
                        drawers[newDrawer][4] = True
                clear()
            elif action[:5] == "close":
                # number parsing
                drawerToClose = ""
                # length will be 7 if single digit, 8 if double digit
                if len(action) == 8:
                    drawerToClose = int(action[-2:]) # slicing magic
                else:
                    drawerToClose = int(action[-1:]) # slicing magic
                drawerToClose -= 1 # shift one because list starts at 0


                if drawers[drawerToClose][1] == True:
                    print("Sorry, you can not close this drawer. It is already closed.")
                    sleep(2)
                else:
                    drawers[drawerToClose][1] = True
                    drawers[drawerToClose][0] = True
                    if drawers[drawerToClose][2] == None:
                        drawers[drawerToClose][4] = False # unreserve when a surface is taken out

                        #note: I am a massive idiot. i spent 2 hours trying to find why i wasn't setting the flag to false, when i said flag == false instead of flag = false

                    # lock a drawer after it is closed, because locked is the default state
                    # and it should only be open when a surface is being taken in or out 
                clear()

            elif len(action) == 10:
                drawerToClose = None
                for i in range(len(drawers)):
                    if drawers[i][1] == False:
                        drawerToClose = i
                        break
                if drawerToClose != None:
                    print("Please close drawer number " + str(drawerToClose + 1) + ".")
                else:
                    unlockedDrawer = None
                    for i in range(len(drawers)):
                        if drawers[i][0] == False:
                            unlockedDrawer = i
                            break
                    if unlockedDrawer != None:
                        if drawers[unlockedDrawer][4] == False:
                            print("Please put your surface in drawer number " + str(unlockedDrawer + 1) + ".")
                            drawers[unlockedDrawer][2] = action[-10:] # if a new barcode is scanned when an old drawer is still unlocked and doesn't have a surface in it, repurpose the drawer
                        else:
                            print("Please remove the surface from drawer number " + str(unlockedDrawer + 1) + ".")
                    else:
                        code = action[-10:] # because student ids are always 10 digits
                        removeDrawer = None
                        for i in range(len(drawers)): # check if you are removing or adding
                            if drawers[i][2] == code:
                                removeDrawer = i
                        if removeDrawer == None: # add functionality
                            newDrawer = None
                            # find an open drawer
                            for i in range(len(drawers)):
                                if drawers[i][4] == False:
                                    newDrawer = i
                                    break
                            if newDrawer == None:
                                print("Sorry, all drawers are being used right now.")
                            else:
                                # set information
                                drawers[newDrawer][2] = code
                                # unlock the drawer until it is opened and closed
                                drawers[newDrawer][0] = False
                                print("Please put your surface in drawer number " + str(newDrawer + 1) + ".")
                        else: # remove functionality
                            drawers[removeDrawer][0] = False
                            drawers[removeDrawer][2] = None
                            drawers[removeDrawer][3] = None
                            print("Please remove your surface from drawer number " + str(removeDrawer + 1) + ".")
                sleep(2)
                clear() 
            else:
                clear()

            updateList()
        
        # setup
        master = master
        master.title("Cabinet")

        # create the 20 labels
        labelList = []
        for i in range(20):
            labelList.append(Label(master, text = ""))
            labelList[i].pack()


        # create the textbox
        entry_box = Entry(master)
        entry_box.pack()

        clear()

        # main data structure
        # 0: locked/unlocked status, true = locked, false = unlocked
        # 1: closed/open status, true = closed, false = open
        # 2: Username, None = no user
        # 3: Password, None = no user
        # 4: Flag, True = drawer is reserved, False = drawer is not reserved
        drawers = [ 
        ]

        # populate the list
        for i in range(20):
            drawers.append([
                True,
                True,
                None,
                None,
                False
            ])

        updateList()


        entry_box.bind('<Return>',entryInput)

root = Tk()
my_gui = GUI(root)
root.mainloop()
