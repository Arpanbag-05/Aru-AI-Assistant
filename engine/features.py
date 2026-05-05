from playsound import playsound
import eel

#sound function for playing sound
def playAssistantSound():
    music_dir = "www\\assets\\audio\\start _sound.mp3"
    playsound(music_dir)

#click sound for mic button
@eel.expose
def playMicSound():
    music_dir = "www\\assets\\audio\\Click_Mic.mp3"
    playsound(music_dir)    