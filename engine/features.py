import re
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from playsound import playsound
import eel

from engine.command import speak
from engine.config import ASSISTANT_NAME
import pywhatkit as kit

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

def PlayYoutube(query):
    search_term = extract_yt_term(query)
    if search_term:
        speak("Playing " + search_term + " on YouTube")
        kit.playonyt(search_term)
    else:
        speak("Sorry, I couldn't find the YouTube video you requested.")

def extract_yt_term(command):
    pattern = r'play\s+(.*?)\s+on\s+youtube'
    match = re.search(pattern, command, re.IGNORECASE)
    return match.group(1) if match else None