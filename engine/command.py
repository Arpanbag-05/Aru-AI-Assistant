import psutil
import datetime
import time
from urllib.parse import quote_plus
import pyttsx3
import eel
import webbrowser
import speech_recognition as sr


# ---------------- TEXT TO SPEECH ----------------

is_speaking = False
def speak(text):
    global is_speaking
    try:
        # Prevent overlapping voice
        if is_speaking:
            return
        is_speaking = True
        eel.DisplayMessage(text)

        # Create fresh engine every time
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        engine.setProperty('voice',voices[1].id)
        engine.setProperty('rate',170)

        engine.say(text)
        engine.runAndWait()
        engine.stop()
        is_speaking = False

    except Exception as e:
        is_speaking = False
        print("Speech Error:", e)

#-----------------TAKE COMMAND-----------------
@eel.expose
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        eel.DisplayMessage("Listening...")

        # Better ambient noise adjustment
        r.adjust_for_ambient_noise(
            source,
            duration=1
        )

        # Voice sensitivity
        r.energy_threshold = 250
        r.dynamic_energy_threshold = True

        # Wait longer before stopping
        r.pause_threshold = 1.5

        # Minimum silence before phrase complete
        r.non_speaking_duration = 0.8
        try:
            audio = r.listen(
                source,

                # Wait longer for user to start speaking
                timeout=15,

                # Allow longer speech
                phrase_time_limit=12
            )

        except sr.WaitTimeoutError:
            print("No speech detected")
            eel.DisplayMessage("No speech detected")
            return ""

        except Exception as e:
            print("Listening Error:", e)
            eel.DisplayMessage("Microphone error")
            return ""

    try:
        print("Recognizing...")
        eel.DisplayMessage("Recognizing...")
        query = r.recognize_google(audio,language='en-IN')

        query = query.lower().strip()
        print(f"User said: {query}")
        eel.DisplayMessage(query)
        return query

    except sr.UnknownValueError:

        print("Could not understand audio")
        eel.DisplayMessage("Could not understand")
        return ""
    
    except sr.RequestError as e:
        print("Internet connection error:", e)
        eel.DisplayMessage("Internet connection issue")
        return ""
    
    except Exception as e:
        print("Recognition Error:", e)
        eel.DisplayMessage("Recognition failed")
        return ""


def safe_execute(func, fallback="Sorry, something went wrong"):
    try:
        return func()
    except Exception as e:
        print("Error:", e)
        return fallback


#------------------ALL COMMANDS-----------------
@eel.expose
def allCommands():
    response = ""
    try:
        query = takeCommand()
        if not query:

            response = ("I couldn't hear you properly")
            print(response)
            speak(response)

            try:
                eel.updateResponse(response)
            except:
                pass

            try:
                eel.ShowHood()
            except:
                pass

            return
        print(query)


# ---------------- GENERIC OPEN COMMAND ----------------
        if 'open' in query:
            try:
                from engine.features import openCommand
                success = openCommand(query)
                if success:
                    app_name = (query.replace("open", "").strip())
                    response = (f"Opening {app_name}")

                else:
                    response = ("Sorry, I couldn't open that application or website")

            except Exception as e:
                print("Open Command Error:", e)
                response = ("Something went wrong while opening")


        # ---------------- DATE + TIME + DAY COMBINATIONS ----------------
        elif any(word in query for word in [
            'date and time',
            'time and date',
            'date and day',
            'day and date',
            'day and time',
            'time and day'
        ]):

            now = datetime.datetime.now()
            current_day = now.strftime('%A')
            current_date = now.strftime('%d %B %Y')
            current_time = now.strftime('%I:%M %p')


            # DATE + TIME
            if (
                'date and time' in query
            ):
                response = (
                    f"Today's date is {current_date} "
                    f"and the current time is {current_time}"
                )

            elif (
                'time and date' in query
            ):
                response = (
                    f"The current time is {current_time} "
                    f"and today's date is {current_date}"
                )

            # DATE + DAY
            elif (
                'date and day' in query
            ):
                response = (
                    f"Today's date is {current_date} "
                    f"and today is {current_day}"
                )

            elif (
                'day and date' in query
            ):
                response = (
                    f"Today is {current_day}, "
                    f"and today's date is {current_date}"
                )

            # DAY + TIME
            elif (
                'day and time' in query
            ):
                response = (
                    f"Today is {current_day} "
                    f"and the current time is {current_time}"
                )      

            elif (
                'time and day' in query
            ):
                response = (
                    f"The current time is {current_time} "
                    f"and today is {current_day}"
                )


        # ---------------- TIME ----------------
        elif any(word in query for word in [
            'time',
            'current time',
            'what time'
        ]):
            now = datetime.datetime.now()
            current_time = now.strftime('%I:%M %p')
            response = f"The current time is {current_time}"


        # ---------------- DATE ----------------
        elif any(word in query for word in [
            'date',
            "today's date",
            'current date'
        ]):

            today = datetime.date.today()
            current_date = today.strftime('%d %B %Y')
            response = f"Today's date is {current_date}"


        # ---------------- DAY ----------------
        elif any(word in query for word in [
            'day',
            'what day'
        ]):
            today = datetime.date.today()
            current_day = today.strftime('%A')
            response = f"Today is {current_day}"
           
# ---------------- SEARCH YOUTUBE ----------------
        elif (
            'search' in query
            and 'youtube' in query
        ):

            from engine.features import SearchYoutube

            clean_query = (
                query.replace("search", "")
                    .replace("on youtube", "")
                    .replace("youtube", "")
                    .strip()
            )

            success = SearchYoutube(clean_query)

            if success:

                response = (
                    f"Searching YouTube for {clean_query}"
                )

            else:

                response = (
                    "Sorry, I couldn't search YouTube"
                )


        # ---------------- SEARCH GOOGLE ----------------
        elif 'search' in query:

            search_query = (
                query.replace("search", "")
                    .replace("on google", "")
                    .replace("google", "")
                    .strip()
            )

            encoded_query = quote_plus(search_query)

            webbrowser.open(
                f"https://www.google.com/search?q={encoded_query}"
            )

            response = (
                f"Searching Google for {search_query}"
            )


# ---------------- PLAY YOUTUBE ----------------
        elif ('play' in query or 'watch' in query):
            from engine.features import PlayYoutube

            clean_query = (
                query.replace("play", "")
                    .replace("watch", "")
                    .replace("on youtube", "")
                    .replace("youtube", "")
                    .strip()
            )

            success = PlayYoutube(clean_query)

            if success:

                response = (
                    f"Playing {clean_query} on YouTube"
                )

            else:

                response = (
                    "Sorry, I couldn't play the video"
                )

#---------------- BATTERY ----------------
        elif 'battery' in query:

            try:
                battery = psutil.sensors_battery()

                if battery:

                    plugged = battery.power_plugged
                    status = "charging" if plugged else "not charging"

                    response = (
                        f"Battery is at {battery.percent} percent "
                        f"and the system is currently {status}"
                    )

                else:
                    response = "Battery information is not available on this device"

            except Exception as e:
                print("Battery Error:", e)
                response = "Sorry, I couldn't fetch battery information"


#---------------- CPU ----------------
        elif 'cpu' in query or 'processor' in query:
            try:
                cpu_usage = psutil.cpu_percent(interval=1)
                response = f"CPU usage is currently {cpu_usage} percent"

            except Exception as e:
                print("CPU Error:", e)
                response = "Sorry, I couldn't fetch CPU usage"


#---------------- RAM ----------------
        elif 'ram' in query or 'memory' in query:
            try:
                memory = psutil.virtual_memory()
                used_ram = round(memory.used / (1024 ** 3), 2)
                total_ram = round(memory.total / (1024 ** 3), 2)

                response = (
                    f"RAM usage is {memory.percent} percent. "
                    f"{used_ram} GB used out of {total_ram} GB"
                )

            except Exception as e:
                print("RAM Error:", e)
                response = "Sorry, I couldn't fetch memory usage"



#---------------- SYSTEM INFO ----------------
        elif 'system' in query or 'system status' in query or 'system info' in query:
            try:
                cpu = psutil.cpu_percent(interval=1)

                memory = psutil.virtual_memory()
                ram_percent = memory.percent

                battery = psutil.sensors_battery()

                if battery:
                    battery_info = f"Battery at {battery.percent} percent"
                else:
                    battery_info = "Battery info unavailable"

                response = (
                    f"System status: CPU usage is {cpu} percent, "
                    f"RAM usage is {ram_percent} percent, "
                    f"and {battery_info}"
                )

            except Exception as e:
                print("System Info Error:", e)
                response = "Sorry, I couldn't fetch system information"


        
# ---------------- UNKNOWN COMMAND ----------------
        else:
            response = (
                "Sorry, I didn't understand that command"
            )

    except Exception as e:
        print("Global Command Error:", e)

        response = (
            "Something went wrong"
        )

    speak(response)

    try:
        eel.updateResponse(response)
    except:
        pass

    time.sleep(0.2)

    try:
        eel.ShowHood()
    except:
        pass