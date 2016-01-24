__author__ = 'sreeni'
from os import path
import os
import subprocess
VIDEO_FILE = path.join(path.dirname(path.realpath(__file__)), "HeapTutorial.mp4")
FILE_NAME = VIDEO_FILE.split(".mp4")[0]


#Get the wav file from video file
os.system("ffmpeg -i " + VIDEO_FILE + " " + FILE_NAME+ ".wav")

#Detect silence of the video file and print it
proc = subprocess.Popen('ffmpeg -i '+VIDEO_FILE+ ' -af silencedetect=noise=0.5:duration=1 -f null -',
                        stdout = subprocess.PIPE,stderr=subprocess.STDOUT,shell=True)
stri = proc.communicate()[0]

#Outputs the timestamps for silences
print stri

words = stri.split(" ")


nextIsSilenceDuration = False
nextIsSilenceEnd = False
nextIsSilenceStart  = False

silenceEndTimeStamps = []
silenceStartTimeStamps = []
silenceDurations = []

#Find duration of the video to get the last chunk without silence
proc = subprocess.Popen(["ffmpeg -i " + VIDEO_FILE + " 2>&1 | awk '/Duration/ {split($2,a,\":\");print a[1]*3600+a[2]*60+a[3]}'"],
                        stdout = subprocess.PIPE, shell = True)

(duration, err) = proc.communicate()
duration = int(float(duration))

print duration

for w in words:
    if nextIsSilenceEnd:
        silenceEndTimeStamps.append(w.split("\r")[0])
        nextIsSilenceEnd = False
        continue
    elif nextIsSilenceStart:
        silenceStartTimeStamps.append(w.split("\r")[0])
        nextIsSilenceStart = False
        continue
    elif nextIsSilenceDuration:
        silenceDurations.append(w.split("\r")[0])
        nextIsSilenceDuration = False
        continue

    if w.startswith("silence_start"):
        nextIsSilenceStart = True;
    elif w.startswith("silence_end"):
        nextIsSilenceEnd = True;
    elif w.startswith("silence_duration"):
        nextIsSilenceDuration = True;


i = 0
for w in silenceStartTimeStamps:
    silenceStartTimeStamps[i] = w.split("\n")[0]
    i= i+1


i = 0
for w in silenceDurations:
    silenceDurations[i] = w.split("\n")[0]
    i = i+1


print silenceDurations
print silenceStartTimeStamps
print silenceEndTimeStamps

initialTime = 0

for i in range(0, len(silenceEndTimeStamps)):
    if float(silenceStartTimeStamps[i])<0:
        initialTime = silenceEndTimeStamps[i]
        continue

    print "Splitting at " + str(initialTime) + " to " + str(silenceStartTimeStamps[i])
    command = "ffmpeg -i "+VIDEO_FILE+ " -ss "+str(initialTime)+ " -t " + \
              str(float(silenceStartTimeStamps[i])- float(initialTime)) + \
              " " + FILE_NAME + str(i) + ".mp4"
    subprocess.call(command,shell = True)


    os.system("ffmpeg -ss " + str(initialTime) + " -t " + str(float(silenceStartTimeStamps[i])- float(initialTime)) + " -i " + FILE_NAME + ".wav file" + str(i) + ".wav")

    initialTime = silenceEndTimeStamps[i]

# Get the last chunk of video
command = "ffmpeg -i "+ VIDEO_FILE + " -ss "+str(initialTime) + " -t " + str(float(duration) - float(initialTime)) \
          + " " + FILE_NAME + str(i+1) + ".mp4"

subprocess.call(command,shell = True)

os.system("ffmpeg -ss " + str(initialTime) + " -t " + str(float(duration)- float(initialTime)) + " -i " + FILE_NAME + ".wav file" + str(i+1) + ".wav")


#All the video chunks are created and now extract the wav file and
i = 0


'''while os.path.isfile(VIDEO_FILE + str(i) + ".mp4"):'''

