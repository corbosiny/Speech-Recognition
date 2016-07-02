import sys
import speech_recognition as speech
import os
import subprocess
import threading
from tkinter import *

class cmdButler(speech_recognition):

    def __init__(self):
        print('Initializing...')
        self.fileName = 'commandFile.txt' #loads in all custom made speech commands, the command and what will be executed in the command line are seperated by a ;

        with open(self.fileName, 'r') as file: 
            self.specialCommands = file.readLines().strip('\n')

        for command in specialCommands: #seperates the speech command from the command line execution into an array inside of specialCommands
            self.specialCommands[specialCommands.index(command)] = command.split(';')

        print('Special commands loaded')

        self.listener = self.Recognizer() #creates object that picks up human speech from audio sources 
        self.audioSource = self.Microphone() #creates an audio source from the computers default microphone

        self.lock = threading.Lock() #used to prevent corruption of data when two threads try and access the same data

        self.monitorInput = threading.Thread(target= lambda: self.inputWindow()) #creates a small input window for adding commands during operation
        self.monitorInput.start() #starts up the input window

        print('Speech recognition and Audio source prepared')

    #####Updating, adding, removing, or editing commands#####
    #the lock is used in all these functions so that the command list is not changed when iterating through it in the main loop
    def updateCommandFile(self):
        with open(self.fileName, 'w') as file:
            for command in self.specialCommands:
                cmd = ';'.join(command) + '\n'
                file.write(cmd)


    def addCommand(self, trigger, execution): #adds a command to the list of custom commands and also adds it to the command file
        self.lock.acquire()
        with open(self.fileName, 'a') as file:
            file.write('\n')
            file.write(trigger + ';' + execution)
        self.lock.release()

    def delCommand(self, commandNum): #deletes a custom command from the command list and command file
        self.lock.acquire()
        del self.specialCommands[commandNum]
        self.updateCommandFile()
        self.lock.release()

    def changeExecution(self, commandNum, newExec): #changes what gets executed when a certain command is spoken
        self.lock.acquire()
        self.specialCommands[commandNum][1] = newExec
        self.updateCommandFile()
        self.lock.release()
            
    def changeTrigger(self, commandNum, newTrig): #changes the speech that is to be said to activate a certain cmd line execution
        self.lock.acquire()
        self.specialCommands[commandNum][0] = newTrig
        self.updateCommandFile()
        self.lock.release()

    def inputWindow(self): #sets up a window for the user to add in or edit custom commands
        root = Tk()
        #adds in a hotkey for the enter button to enter in the current typed out command
        root.bind('<Return>', lambda event: self.appendTextDisplay(entry, textDisplay))

        outputFrame = Frame(root)
        outputFrame.pack(side= TOP)

        #creates a text display with a scroll bar that will display user changes or additions to the current custom commands
        textDisplay = Text(outputFrame, relief= RAISED, background= "black", foreground= "green", wrap= WORD)
        yScrollBar = Scrollbar(outputFrame, command= textDisplay.yview, relief= "sunken")
        textDisplay['yscrollcommand'] = yScrollBar.set
        yScrollBar.pack(side= RIGHT, fill= Y)
        textDisplay.config(state= DISABLED)
        textDisplay.pack()

        inputFrame = Frame(root)
        frame.pack(side= BOTTOM)

        #makes an input text bar for user commands to be entered
        entry = Entry(inputFrame, bd= 5)
        entry.pack()

        #creates a button that when clicked enters in the current typed out command in the entry bar
        button = Button(inputFrame, text= 'Enter', command= lambda: self.appendTextDisplay(entry, textDisplay))
        button.pack()

        #starts up the gui loop
        root.mainloop()

    def appendTextDisplay(self, inputBar, textDisplay): #adds in any typed command and the results of that to the text display
        textDisplay.config(state= "normal")
        textDisplay.insert(INSERT, "\n" + inputBar.get())
        textDisplay.insert(INSERT, '\n' + self.userInput(inputBar.get()))
        inputBar.delete(0, END)
        textDisplay.config(state= DISABLED)
        textDisplay.see(END)
    
    def userInput(self, userInput): #checks if the user command is a valid one, and executes if it is valid, whatever is returned is added to the text display
        userInput = userInput.split()
        if userInput[0] == 'addCommand':
            self.addCommand(userInput[1], userInput[2])
            return 'DONE\n'
        elif userInput[0] == 'delCommand':
            self.delCommand(userInput[1])
            return 'DONE\n'
        elif userInput[0] == 'changeExecution':
            self.changeExecution(userInput[1], userInput[2])
            return 'DONE\n'
        elif userInput[0] == 'changeTrigger':
            self.changeTrigger(userInput[1], userInput[2])
            return 'DONE\n'
        elif userInput[0] == 'displayCommands':
            commands = []
            for command in self.specialCommands:
                commands.append(' : '.join(command))
            commands.append('DONE\n')
            return '\n'.join(commands)
        else:
            return 'Command Not Recognized\nDONE'
        
    def main(self):
        print('Beginning Speech Recognition..')
        cmd = None
        while True: 
            cmd = None
            while cmd is None:
                try:
                    cmd = self.listener.recognize_google(audio)
                    if 'nova' not in str(cmd):
                        cmd = None
                    
                except self.UnknownValueError:
                    cmd = None
                    
                except:
                    print('Error encounterd: ' + str(sys.exc_info()[0]))
                    break
                
            print('Heard command: ' + str(cmd))

            cmd.replace('nova', '')

            if 'write quit' in cmd: #this command closes down the program
                break

            self.lock.acquire() #the lock is acquired to prevent any changes of the size of the command list while iterating through it
            for command in self.specialCommands: #looks to see if the speech command is recognized as a special command
                if cmd in command[0]:
                    #sends the custom cmd line execution to the command line when the trigger phrase is detected
                    results = subprocess.Popen(specialCommands[self.specialCommands.index(command)][1], shell= True, stdout= subproces.PIPE, stderr= subprocess.PIPE)
                    print('\n' + str(results))
                    self.lock.release() #opens the special command list back up the be modified by ohter functions
                    break
                
            else: #this else triggers only if no special command was detected
                self.lock.release()
                #pipes the user speech to the command line and prints the results
                results = subprocess.Popen(cmd, shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
                print('\n' + str(results))

            
        print('Ending Speech Recognition')


if __name__ == '__main__':
    manager = cmdButler()
    
