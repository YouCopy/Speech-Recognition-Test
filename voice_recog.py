import speech_recognition as sr
from playsound import playsound
import urllib.request
import urllib.parse
import re
import webbrowser

key = "Bertram"

def waitForWord():
    with sr.Microphone() as source:
        bertram = False
        r = sr.Recognizer()
        r.adjust_for_ambient_noise(source, duration = 0.2)
        print("Speak: ")
        while True:
            try:
                voice = r.listen(source, phrase_time_limit=5)
                text = r.recognize_google(voice, language = 'en-IN')

                print(text)
                start = getFirstWord(text)

                if(text == key):
                    playsound('bertram.mp3')
                    bertram = True
                elif(start == "play" and bertram == True):
                    command = getOtherWords(text)
                    html = urllib.request.urlopen("https://www.youtube.com/results?search_query=" + command)
                    video_ids = re.findall(r"watch\?v=(\S{11})", html.read().decode())
                    id = "https://www.youtube.com/watch?v=" + video_ids[0]
                    webbrowser.open(id, new=2)
                    bertram = False

            except sr.UnknownValueError:
                r = sr.Recognizer()
                r.adjust_for_ambient_noise(source, duration = 0.2)
                continue

def getFirstWord(input):
    return input.split()[0]

def getOtherWords(input):
    output = '+'.join(input.split()[1:])
    return output

waitForWord()