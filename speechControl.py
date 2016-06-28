import sys
import speech_recognition as speech
import os
import subprocess
import threading
from tkinter import *

class theHammer(speech_recognition):

    def __init__(self):
        print('Initializing...')
        self.fileName = 'commandFile.txt'

        with open(self.fileName, 'r') as file:
            self.specialCommands = file.readLines().strip('\n')

        for command in specialCommands:
            self.specialCommands[specialCommands.index(command)] = command.split(';')

        print('Special commands loaded')

        self.listener = self.Recognizer()
        self.audioSource = self.Microphone()

        self.lock = threading.Lock()

        self.monitorInput = threading.Thread(target= lambda: self.inputWindow())
        self.monitorInput.start()

        print('Speech reoognition and Audio source prepared')

    def updateCommandFile(self):
        with open(self.fileName, 'w') as file:
            for command in self.specialCommands:
                cmd = ';'.join(command) + '\n'
                file.write(cmd)


    def addCommand(self, trigger, execution):
        self.lock.acquire()
        with open(self.fileName, 'a') as file:
            file.write('\n')
            file.write(trigger + ';' + execution)
        self.lock.release()

    def delCommand(self, commandNum):
        self.lock.acquire()
        del self.specialCommands[commandNum]
        self.updateCommandFile()
        self.lock.release()

    def changeExecution(self, commandNum, newExec):
        self.lock.acquire()
        self.specialCommands[commandNum][1] = newExec
        self.updateCommandFile()
        self.lock.release()
            
    def changeTrigger(self, commandNum, newTrig):
        self.lock.acquire()
        self.specialCommands[commandNum][0] = newTrig
        self.updateCommandFile()
        self.lock.release()

    def inputWindow(self):
        root = Tk()
        root.bind('<Return>', lambda event: self.appendTextDisplay(entry, textDisplay))

        outputFrame = Frame(root)
        outputFrame.pack(side= TOP)

        textDisplay = Text(outputFrame, relief= RAISED, background= "black", foreground= "green", wrap= WORD)
        yScrollBar = Scrollbar(outputFrame, command= textDisplay.yview, relief= "sunken")
        textDisplay['yscrollcommand'] = yScrollBar.set
        yScrollBar.pack(side= RIGHT, fill= Y)
        textDisplay.config(state= DISABLED)
        textDisplay.pack()

        inputFrame = Frame(root)
        frame.pack(side= BOTTOM)

        entry = Entry(inputFrame, bd= 5)
        entry.pack()

        root.bind
        button = Button(inputFrame, text= 'Enter', command= lambda: self.appendTextDisplay(entry, textDisplay))
        button.pack()

        root.mainloop()

    def appendTextDisplay(self, inputBar, textDisplay):
        textDisplay.config(state= "normal")
        textDisplay.insert(INSERT, "\n" + inputBar.get())
        textDisplay.insert(INSERT, '\n' + self.userInput(inputBar.get()))
        inputBar.delete(0, END)
        textDisplay.config(state= DISABLED)
        textDisplay.see(END)
    
    def userInput(self, userInput):
        userInput = userInput.split()
        if userInput[0] == 'addCommand':
            self.addCommand(userInput[1], userInput[2])
        elif userInput[0] == 'delCommand':
            self.delCommand(userInput[1])
        elif userInput[0] == 'changeExecution':
            self.changeExecution(userInput[1], userInput[2])
        elif userInput[0] == 'changeTrigger':
            self.changeTrigger(userInput[1], userInput[2])
        elif userInput[0] == 'displayCommands':
            commands = []
            for command in self.specialCommands:
                commands.append(' : '.join(command))
            commands.append('DONE\n')
            return '\n'.join(commands)
        
        return 'DONE\n'
        
    def main(self):
        print('Beginning Speech Recognition..')
        cmd = None
        while cmd != 'write quit':
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

            self.lock.acquire()
            for command in self.specialCommands:
                if cmd in command[0]:
                    results = subprocess.Popen(specialCommands[self.specialCommands.index(command)][1], shell= True, stdout= subproces.PIPE, stderr= subprocess.PIPE)
                    print('\n' + str(results))
                    self.lock.release()
                    break
                
            else:
                self.lock.release()
                results = subprocess.Popen(cmd, shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
                print('\n' + str(results))

            
        print('Ending Speech Recognition')


if __name__ == '__main__':
    manager = theHammer()
