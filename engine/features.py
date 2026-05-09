import re
import sqlite3
import sys
import os
import pywhatkit as kit
from urllib.parse import quote_plus
import webbrowser

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from playsound import playsound
import eel

from engine.command import speak
from engine.config import ASSISTANT_NAME


# ---------------- DATABASE ----------------
conn = sqlite3.connect("aru.db")
cursor = conn.cursor()


# ---------------- STARTUP SOUND ----------------
def playAssistantSound():

    try:
        music_dir = "www\\assets\\audio\\start_sound.mp3"
        playsound(music_dir)

    except Exception as e:
        print("Startup Sound Error:", e)


# ---------------- MIC CLICK SOUND ----------------
@eel.expose
def playMicSound():

    try:
        music_dir = "www\\assets\\audio\\Click_Mic.mp3"
        playsound(music_dir)

    except Exception as e:
        print("Mic Sound Error:", e)


# ---------------- OPEN APPLICATIONS / WEBSITES ----------------
def openCommand(query):

    try:
        query = query.lower()

        # Remove assistant name
        query = query.replace(ASSISTANT_NAME.lower(),"")

        # Remove open keyword
        query = query.replace("open","").strip()

        if not query:
            return False
        

# ---------------- WEBSITES ----------------
        if "youtube" in query:

            webbrowser.open(
                "https://www.youtube.com"
            )

        elif "google" in query:

            webbrowser.open(
                "https://www.google.com"
            )

        elif (
            "chat gpt" in query
            or "chatgpt" in query
        ):

            webbrowser.open(
                "https://chat.openai.com"
            )

        elif "gemini" in query:

            webbrowser.open(
                "https://gemini.google.com/"
            )

        # ---------------- WINDOWS APPS ----------------

        elif "notepad" in query:
            os.system("start notepad")

        elif "calculator" in query or "calc" in query:
            os.system("start calc")

        elif "chrome" in query:
            os.system("start chrome")

        elif "command prompt" in query or "cmd" in query:
            os.system("start cmd")

        elif "file explorer" in query or "explorer" in query:
            os.system("start explorer")

        elif "paint" in query:
            os.system("start mspaint")

        elif "wordpad" in query:
            os.system("start write")

        elif "settings" in query:
            os.system("start ms-settings:")

        elif "camera" in query:
            os.system("start microsoft.windows.camera:")

        elif "control panel" in query:
            os.system("start control")

        elif "task manager" in query:
            os.system("start taskmgr")

        elif "vs code" in query or "visual studio code" in query:
            os.system("start code")

        else:
            return False
        return True

    except Exception as e:
        print("OpenCommand Error:", e)
        return False


# ---------------- EXTRACT YOUTUBE SEARCH TERM ----------------
def extract_yt_term(command):
    try:
        command = command.lower()
        patterns = [
            r'play\s+(.*?)\s+on\s+youtube',
            r'watch\s+(.*?)\s+on\s+youtube',
            r'search\s+(.*?)\s+on\s+youtube',
            r'play\s+(.*)',
            r'watch\s+(.*)'
        ]
        for pattern in patterns:
            match = re.search(
                pattern,
                command,
                re.IGNORECASE
            )

            if match:
                term = match.group(1).strip()

                # Prevent Google overlap
                if (term and 'google' not in term):

                    return term
        return None

    except Exception as e:
        print("ExtractYT Error:", e)
        return None


# ---------------- PLAY YOUTUBE VIDEO ----------------
def PlayYoutube(search_term):
    try:
        if not search_term:
            webbrowser.open(
                "https://www.youtube.com"
            )
            return True
        
        kit.playonyt(search_term)
        return True

    except Exception as e:
        print("PlayYoutube Error:", e)
        return False


# ---------------- SEARCH YOUTUBE ----------------
def SearchYoutube(search_term):
    try:
        encoded_query = quote_plus(search_term)
        url = (
            f"https://www.youtube.com/results?"
            f"search_query={encoded_query}"
        )
        webbrowser.open(url)
        return True

    except Exception as e:
        print("SearchYoutube Error:", e)
        return False