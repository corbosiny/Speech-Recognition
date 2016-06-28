import sys
import speech_recognition as speech
import os
import subprocess

listener = speech.Recognizer()
audioSource = speech.Microphone()

cmd = ""
while cmd != 'write quit':
    cmd = None
    while cmd is None:
        try:
            audio = listener.listen(audioSource)
            cmd = listener.recognize_google(audio)
            if 'nova' not in str(cmd):
                cmd = None
            
        except speech.UnknownValueError:
            cmd = None
            
        except:
            print('Error encounterd: ' + str(sys.exc_info()[0]))
            break
        
    print('Heard command: ' + str(cmd))
    results = subprocess.Popen(cmd, shell= True, stdout= subprocess.PIPE, stderr= subprocess.PIPE)
    print('\n' + str(results))

print('Quitting Voice Recognition')
