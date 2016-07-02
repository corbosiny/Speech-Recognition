import sys
import speech_recognition as speech
import os
import subprocess

listener = speech.Recognizer() #creates object that takes audio and detects human speech
audioSource = speech.Microphone() #designates the computers default audio as an audio source to listen from

cmd = ""
while cmd != 'write quit': #speech command to end the program
    cmd = None
    while cmd is None:
        try:
            audio = listener.listen(audioSource) #trys to listen for audio
            cmd = listener.recognize_google(audio) #uses google speech to recognize any human speech in the audio
            if 'nova' not in str(cmd): #nova is the key word to signify a command is being sent
                cmd = None
            
        except speech.UnknownValueError: #if the command was not recognized than wait for a clearer command by setting cmd to None to keep the loop going
            cmd = None
            
        except: #ends the test if an error was encountered
            print('Error encounterd: ' + str(sys.exc_info()[0]))
            break
        
    print('Heard command: ' + str(cmd)) #used for testing, to see what the speech recognizer picked up
    results = subprocess.Popen(cmd, shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE) #sends the users command to the command line and prints out the results
    print('\n' + str(results))

print('Quitting Voice Recognition')
