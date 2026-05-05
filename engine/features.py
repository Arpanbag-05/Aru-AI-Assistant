import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playsound import playsound
import eel

from engine.command import speak
from engine.config import ASSISTANT_NAME

#sound function for playing sound
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start_sound.mp3"
    playsound(music_dir)

#click sound for mic button
@eel.expose
def playMicSound():
    music_dir = "www\\assets\\audio\\Click_Mic.mp3"
    playsound(music_dir)

def openCommand(query):
    query = query.replace(ASSISTANT_NAME, "")
    query = query.replace("open", "")
    query.lower()

    if query != "":
        speak("Opening" + query)
        os.system('start ' + query)

    else:
        speak(f"{query} not found")