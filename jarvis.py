# Install all required modules given below by using pip install module_name and only after installing import them 
from time import time
import pyttsx3 
from requests.api import head
import speech_recognition as sr 
import datetime
import wikipedia
import webbrowser
import os
import smtplib
import cv2
import requests
from wikipedia.wikipedia import random
from webbrowser import get
import pywhatkit as kit
import sys
import pyjokes
import pyautogui
import socket
import pywhatkit as pwk
from speedtest import Speedtest
import instaloader
import random 
#import platform
import PyPDF2
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QTimer, QTime, QDate, Qt
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from PyQt5.uic import loadUiType
from jarvisui import Ui_MainWindow
import numpy as np
import operator
from bs4 import BeautifulSoup
from pywikihow import search_wikihow
import MyAlarm

engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
#print(voices)
engine.setProperty('voice',voices[1].id)


app = instaloader.Instaloader()

def speak(audio):
    engine.say(audio)
    engine.runAndWait()

def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak("Good Moring sir!")
    elif hour>=12 and hour<18:
        speak("Good Afternoon sir!")
    else:
        speak("Good Evening sir!")

    speak("how can I help")

def sendEmail(to, content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('username@gmail.com','password') #Enter your email id and password
    server.sendmail('username@gmail.com',to,content) #Enter the email id of sender again
    server.close()

def news():
    main_url = 'http://newsapi.org/v2/top-headlines?sources=techcrunch&apikey=c8cd393d1bf84b759cae19e1f805db6f'

    main_page = requests.get(main_url).json()
    articles = main_page["articles"]
    head=[]
    day = ["first", "second", "third", "fourth", "fifth"]
    for ar in articles:
        head.append(ar["title"])
    for i in range (len(day)):
        speak(f"today's {day[i]} news is: {head[i]}") 

def pdf_reader():
    speak("Sir please enter the name of pdf")
    pdf_bk = input("Enter book name: ")
    book = open(f'{pdf_bk}', 'rb') 
    pdfReader = PyPDF2.PdfFileReader(book)
    pages = pdfReader.numPages
    speak("Total number pages in this book are {pages}") 
    speak("Sir please enter the page number you want me to read")
    readpg = int(input("Page No.: "))
    page = pdfReader.getPage(readpg)
    text = page.extractText()
    speak(text) 

class MainThread(QThread):
    def __init__(self):
        super(MainThread,self).__init__()

    def run(self):
        self.TaskExecution()

    def takeCommand(self):
        r = sr.Recognizer()
        with sr.Microphone() as source:
            print("Listening...")
            r.pause_threshold = 0.5
            audio = r.listen(source)

        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language = 'en-in') 
            print(f"User said: {query}\n")

        except Exception as e:
            # print(e)
            print("Say that again please...")
            return "None" 
        return query 

    def TaskExecution(self):
        wishMe()
        while True:
            self.query = self.takeCommand().lower()
            

            if 'wikipedia' in self.query: #for searching anything on youtube
                speak("Searching Wikipedia...")
                self.query = self.query.replace("wikipedia", "")
                results = wikipedia.summary(self.query, sentences=1)
                speak("According to Wikipedia")
                print(results)
                speak(results)

            elif 'open command prompt' in self.query:
                os.system('start cmd')

            elif 'open youtube' in self.query: #for opening any site
                webbrowser.open("https://youtube.com", new=0, autoraise=True)

            elif 'who are you' in self.query:
                speak("I am Jarvis")
                print("I am Jarvis")

            elif 'open camera' in self.query:
                cap = cv2.VideoCapture(0)
                while True:
                    ret, img = cap.read()
                    cv2.imshow('webcam', img)
                    k = cv2.waitKey(50)
                    if k == 27:
                        break;
                cap.release()
                cap.destryoAllWindows() 

            elif 'open google' in self.query: 
                speak("Sir, What should I search on google?")
                cm = self.takeCommand().lower()
                webbrowser.open("https://google.com//search?q="+f"{cm}")

            elif 'search on youtube' in self.query: 
                speak("Sir, What should I search on youtube?")
                cm = self.takeCommand().lower()
                webbrowser.open("https://youtube.com//search?q="+f"{cm}")

            elif 'send message' in self.query:
                speak("Whom should I send the message sir?")
                ab = int(input("Please Enter Number: "))
                speak("What message should be sent sir?")
                bc = self.takeCommand().lower()
                speak("Please Enter the hour in which message is to be sent")
                cd = int(input("Please Enter the hour in which message is to be sent: "))
                speak("Please Enter the minutes please enter 3 minutes more than actual time")
                
                de = int(input("Please Enter the minutes in which message is to be sent: "))
                kit.sendwhatmsg(f"+91 {ab}",f"{bc}", cd,de)
                
            elif 'play music' in self.query: #for playing music
                music_dir = 'D:\\Fav' #Add path of your songs
                songs = os.listdir(music_dir)
                rd = random.choice(songs)
                os.startfile(os.path.join(music_dir, rd))

            elif 'the time' in self.query:
                strTime = datetime.datetime.now().strftime("%H:%M:%S")
                print(strTime)
                speak(f"Sir the time is {strTime}") 
    
            elif 'open prime video' in self.query:
                webbrowser.open("https://primevideo.com")

            elif 'thank you' in self.query:
                speak("You're most welcome sir!")
                print("You're most welcome sir!")

            elif 'latest news' in self.query:
                speak("Please wait sir, fetching the news")
                news()

            elif 'play a song on youtube' in self.query:
                speak("Which song should I play sir?")
                yt = self.takeCommand().lower()
                kit.playonyt(f"{yt}")

            elif 'email' in self.query:
                try:
                    speak("Whom should I send the email sir")
                    to = input("Reciever's Email ID: ")
                    speak("What should I say sir?")
                    content = self.takeCommand().lower()
                    sendEmail(to, content)
                    speak("Email has been sent!")
                except Exception as e:
                    print(e)
                    speak("Sorry sir I was not able to send the email.")

            elif 'set alarm' in self.query:
                speak("Sir please tell me the time to set alarm. for example, set alarm to 17:45 pm")
                tt = self.takeCommand().lower()
                tt = tt.replace("set alarm to ", "")
                tt = tt.replace(".","")
                tt = tt.upper()
                MyAlarm.alarm(tt) 

            elif 'volume up' in self.query:
                pyautogui.press("volumeup")

            elif 'volume down' in self.query:
                pyautogui.press("volumedown")

            elif 'mute' in self.query or 'mute volume' in self.query:
                pyautogui.press("volumemute")


            elif 'tell me a joke' in self.query:
                joke = pyjokes.get_joke()
                speak(joke)
                print(joke)

            elif 'bad joke' in self.query:
                speak("Sorry to hear that sir. I will try another.")
                jok = pyjokes.get_joke()
                speak(jok)
                print(jok)

            elif 'satellite' in self.query:
                speak("Which satellite you want to see sir say random if not any specific")
                sat = self.takeCommand().lower()
                if sat == "random":
                    webbrowser.open("http://stuffin.space")
                else:
                    webbrowser.open("http://stuffin.space/?search="+f"{sat}")

            elif 'shut down' in self.query:
                os.system("shutdown /s /t 5")

            elif 'sleep' in self.query:
                os.system("rundll32.exe powrproof.dll,SetSuspendState 0,1,0")

            elif 'convert text to handwriting' in self.query:
                speak("Please input the text sir")
                txt = input("Enter your text here: ")
                try:
                    pwk.text_to_handwriting(f"{txt}", rgb=(0, 0, 255))
                    speak("Sir the converted picture is saved in the same folder")
                except Exception as exe:
                    print(exe)
                    speak("Sorry sir I was not able to convert that text")

            elif 'internet speed' in self.query:
                st = Speedtest()
                download = st.download()
                upload = st.upload()
                download_speed = round(download / (10**6), 2)
                upload_speed = round(upload / (10**6), 2)
                speak(f"Download speed is {download_speed} mb per second")
                print("Download speed is" ,{download_speed} ,"mb/s")
                speak(f"Upload speed is {upload_speed} mb per second")
                print("Upload speed is" ,{upload_speed} ,"mb/s")

            elif 'profile picture' in self.query:
                speak("Sir please input the user name")
                user_name = input("User Name: ")
                app.download_profile(user_name, profile_pic_only=True)
                speak("Sir profile picture is saved in the same folder")

            elif 'take screenshot' in self.query:
                mySS = pyautogui.screenshot()
                mySS.save("ss.png")

            elif 'calculate' in self.query:
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    speak("Say what you want to calculate, example 2 plus 2")
                    print("Listening...")
                    r.adjust_for_ambient_noise(source)
                    audio = r.listen(source)
                my_string = r.recognize_google(audio)
                print(my_string)
                def get_operator_fn(op):
                    return{
                        '+': operator.add, 
                        '-': operator.sub,
                        'x': operator.mul,
                        'divided by': operator.__truediv__,
                    }[op]
                def eval_binary_expr(op1, oper, op2):
                    op1, op2 = int(op1), int(op2)
                    return get_operator_fn(oper)(op1, op2)
                speak("your result is")
                print(eval_binary_expr(*(my_string.split())))
                speak(eval_binary_expr(*(my_string.split())))

            elif 'read pdf' in self.query:
                pdf_reader()

            elif "temperature" in self.query:
                speak("Enter your city name")
                inp = input("Enter your city: ")
                search = f"temperature in {inp}"
                ur = f"https://google.com/search?q={search}"
                r = requests.get(ur)
                data = BeautifulSoup(r.text,"html.parser")
                temp = data.find("div", class_="BNeawe").text
                speak(f"Current {search} is {temp}")

            elif "activate how to do mod" in self.query:
                speak("how to do mode is activated please tell me what you want to know")
                how = self.takeCommand().lower()
                max_result = 1
                how_to = search_wikihow(how, max_result)
                assert len(how_to)==1
                how_to[0].print()
                speak(how_to[0].summary)

            elif "are you listening" in self.query or 'jarvis' in self.query or 'are you still listening' in self.query:
                speak("Yes sir")

            elif "what else can you do" in self.query or "what can you do" in self.query:
                speak("I can google, open youtube, search wikipedia, share news, operate whatsapp, guess temperature, tell jokes and many more things")

            elif 'stop listening' in self.query:
                speak("Sure sir. Have a good day.")
                sys.exit()

startExecution = MainThread()

class Main(QMainWindow):
    def __init__(self):
        super().__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        self.ui.pushButton.clicked.connect(self.startTask)
        self.ui.pushButton_2.clicked.connect(self.close)

    def startTask(self):
        self.ui.movie = QtGui.QMovie("D:/Jarvis/JARVISUI.gif")
        self.ui.label.setMovie(self.ui.movie)
        self.ui.movie.start()
        self.ui.movie = QtGui.QMovie("D:/Jarvis/JARVIS2.gif")
        self.ui.label_2.setMovie(self.ui.movie)
        self.ui.movie.start()
        timer = QTimer(self)
        timer.timeout.connect(self.showTime)
        timer.start(1000)
        startExecution.start()

    def showTime(self):
        current_time = QTime.currentTime()
        current_date = QDate.currentDate()
        label_time = current_time.toString('hh:mm:ss')
        label_date = current_date.toString(Qt.ISODate)
        self.ui.textBrowser.setText(label_date)
        self.ui.textBrowser_2.setText(label_time)

app = QApplication(sys.argv)
jarvis = Main()
jarvis.show()
exit(app.exec_())
