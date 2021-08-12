import wikipedia
import os
import webbrowser
import pyttsx3
import random
import speech_recognition as sr
# from googlesearch import search
import datetime

till=True
engine=pyttsx3.init('sapi5')
voices=engine.getProperty("voices")
engine.setProperty("voices",voices[1].id)

def speak(audio):
	engine.say(audio)
	engine.runAndWait()


def wish_me():
	hour=int(datetime.datetime.now().hour)
	# print(hour)
	if (hour>=0 & hour<12):
		speak("GOOD MORNING SIR")
		print("GOOD MORNING SIR")
	elif (hour>=12 & hour<16):
		speak("GOOD AFTERNOON SIR")
		print("GOOD AFTERNOON SIR")
	else:
		speak("GOOD EVENING SIR")
		print("GOOD EVENING SIR")
def takeCommand():
    #It takes microphone input from the user and returns string output

    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        r.pause_threshold = 2
        audio = r.listen(source)

    try:
        print("Recognizing...")    
        query = r.recognize_google(audio)
        print("User said:"+query)

    except Exception as e:
        print("Say that again please...Couldnt hear")  
        return "None"
    return query




wish_me()
while till:
	speak("i am spardha assistant sir... how may i help you?")
	print("i am spardha assistant sir... how may i help you?")
	takeCommand()
	if 'open' in query:
		webbrowser.open(query[r.find('open')+5:len(query)])
	elif 'stop' in query:
		till=False
	else:
		pass
