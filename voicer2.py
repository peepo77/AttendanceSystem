import pyttsx3
from pyttsx3 import Engine

engine: Engine = pyttsx3.init('sapi5')
voices = engine.getProperty('voices')
# engine.setProperty('voice',voices[int(input('Choose your assistant:\n1. Jarvis\n2. Edith\nEnter(1/2): '))-1].id)
engine.setProperty('voice',voices[1].id)
def read_out_message(audio):
    engine.say(audio)
    engine.runAndWait()

#read_out_message('Hello Legendary MKM Sir, Pranaaam! Shoooooobbbhhhum Jaiswal, your attendance is marked')
# while True:
#     x=int(input('What do you want your assistant to do?\n1. To Read\n2. To Quit\nEnter(1/2): '))
#     if x==1:
#         y=int(input('What do you want your assistant to read?\n1. Enter a File path to read\n2. Enter text to read\nEnter(1/2): '))
#         if y==1:
#             fh=open(input('Enter path: ')).read()
#             print(fh)
#             speak(fh)

#         elif y==2:
#             t=input('Enter text: ')
#             speak(t)
#     else:
#         break

