import sys
import speech_recognition as speech
import os

listener = speech.Recognizer()
with speech.Microphone() as audioSource:
    print('Speak!')
    audio = listener.listen(audioSource)

try:
    print(listener.recognize_google(audio))

except speech.UnknownValueError:
    print('Speech was not recognized!')

except:
    print('Error: ' + str(sys.exc_info()[0]))
