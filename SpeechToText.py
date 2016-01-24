__author__ = 'sreeni'


import os
import subprocess
import speech_recognition as sr

# obtain path to "test.wav" in the same folder as this script
from os import path

VIDEO_FILE = path.join(path.dirname(path.realpath(__file__)), "HeapTutorial.mp4")
WAV_FILE = "HeapTutorial_audio.wav"

proc = subprocess.Popen(["ffmpeg -i " + WAV_FILE + " 2>&1 | awk '/Duration/ {split($2,a,\":\");print a[1]*3600+a[2]*60+a[3]}'"],
                        stdout = subprocess.PIPE, shell = True)

(duration, err) = proc.communicate()
duration = int(float(duration))
y = 0

'''for x in range(0, duration,5):
    print "x = " + str(x)
    print " "
    print "x+10 = " + str(x+10)
    os.system("ffmpeg -ss " + str(x) + " -t " + str(5) + " -i " + WAV_FILE + " file" + str(y) + ".wav")
    y = y+1'''


text = "";
r = sr.Recognizer()
with sr.WavFile("file18.wav") as source:
    audio = r.record(source)
    print r.recognize_google(audio)

'''for x in range(0, y-1):
    with sr.WavFile("file"+str(x)+".wav") as source:
        audio = r.record(source)
        print r.recognize_google(audio)'''

'''os.system("ffmpeg -i " + VIDEO_FILE + " " + WAV_FILE)

os.system("ffmpeg -ss 0 -t 10 -i " + WAV_FILE + " file.wav" )
# use "test.wav" as the audio source
r = sr.Recognizer()
with sr.WavFile("file.wav") as source:
    audio = r.record(source) # read the entire WAV file


# recognize speech using Google Speech Recognition
try:
    # for testing purposes, we're just using the default API key
    # to use another API key, use `r.recognize_google(audio, key="GOOGLE_SPEECH_RECOGNITION_API_KEY")`
    # instead of `r.recognize_google(audio)`
    print("Google Speech Recognition thinks you said " + r.recognize_google(audio))
except sr.UnknownValueError:
    print("Google Speech Recognition could not understand audio")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))'''
