import sys
import speech_recognition as speech
import os

listener = speech.Recognizer() #create an object that will take audio and detect speech patterns
with speech.Microphone() as audioSource: #uses the computers defualt audio as an audio source
    print('Speak!')
    audio = listener.listen(audioSource) #picks up audio from the microphone and stores the data

try:
    print(listener.recognize_google(audio)) #uses googles speech recognition to detect human speech

except speech.UnknownValueError: #if the speech was unclear
    print('Speech was not recognized!')

except: #catching any other errors
    print('Error: ' + str(sys.exc_info()[0]))
