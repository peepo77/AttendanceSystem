import pyttsx3

def read_out_message(message):
    engine = pyttsx3.init()
    engine.say(message)
    engine.runAndWait()
    voices = engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
# Example usage:
#read_out_message("John Doe, your attendance has been marked")
