import speech_recognition as sr
import pyttsx3
import pywhatkit as kt
import datetime
import wikipedia
import pyjokes
import calendar
from datetime import date, time, datetime
import webbrowser
import site
import random
import requests
import json
from playsound import playsound
from plyer import notification
import wolframalpha

chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe %s"
listener = sr.Recognizer()
engine = pyttsx3.init()
voices = engine.getProperty("voices")
engine.setProperty("voice", voices[1].id)


def talk(text):
    engine.say(text)
    engine.runAndWait()


def take_command():
    command = ""
    try:
        with sr.Microphone() as source:
            print("listening...")
            voice = listener.listen(source)
            command = listener.recognize_google(voice)
            command = command.lower()
            if "buddy" in command:
                command = command.replace("buddy", "")
                print(command)
    except Exception as err:
        print("Issue in take_command(): {}".format(err))
        return ""  # return empty string instead of None

    return command


def run_alexa():
    command = take_command()
    if not command:
        return  # skip if command is empty

    print(command)

    if "play" in command:
        song = command.replace("play", "")
        talk("playing " + song)
        kt.playonyt(song)
    elif "hai" in command or "hello" in command or "let's get started" in command:
        talk("Hey what can I do for you")
    elif "top 10 news" in command:
        r = requests.get(
            "https://newsapi.org/v2/top-headlines?country=in&apiKey=6721a0266ede408a9daffb592cec380a"
        )
        data = json.loads(r.content)
        for i in range(10):
            News = data["articles"][i]["title"]
            print("News ", i + 1, ":", News)
            talk(News)
    elif "weather" in command:
        talk("Please enter the name of city")
        CITY = take_command()
        API_KEY = "a3296ddf78aa6b7a9f32ff2e6e55575d"
        BASE_URL = "https://api.openweathermap.org/data/2.5/weather?"
        URL = BASE_URL + "q=" + CITY + "&appid=" + API_KEY
        response = requests.get(URL)
        if response.status_code == 200:
            data = response.json()
            main = data["main"]
            temperature = main["temp"]
            humidity = main["humidity"]
            pressure = main["pressure"]
            report = data["weather"]
            des = report[0]["description"]
            print(f"{CITY:-^30}")
            print(f"Temperature: {temperature}")
            print(f"Humidity: {humidity}")
            print(f"Pressure: {pressure}")
            print(f"Weather Report:{des}")
            talk(
                f"Temperature is {temperature} kelvin Humidity is {humidity} percent Pressure is {pressure} hPa and it is {des} right now"
            )
        else:
            print("Error in the HTTP request")
    elif "how are you" in command:
        greeting = random.choice([
            "I'm okay.",
            "I'm doing well. Thank you.",
            "I am doing okay."
        ])
        talk(greeting)
        talk("How are you")
    elif "fine" in command or "good" in command:
        talk("It's good to know that you're fine")
    elif "where is" in command:
        location = command.replace("where is", "")
        talk("User asked to Locate")
        talk(location)
        webbrowser.open("https://www.google.com/maps/place/" + location)
    elif "time" in command:
        now = datetime.now()
        current_time = time(now.hour, now.minute, now.second).strftime("%I:%M %p")
        talk("Current time is " + current_time)
    elif "search" in command:
        talk("What do you want to search for?")
        Search = take_command()
        kt.search(Search)
    elif "who are you" in command or "define yourself" in command:
        speak = """Hello, I am Buddy. Your personal Assistant.
            I am here to make your life easier. You can command me to perform
            various tasks such as play songs, tell jokes, set alarms, etc."""
        talk(speak)
    elif "write a note" in command:
        talk("What should I write?")
        note = take_command()
        file = open("jarvis.txt", "w")
        talk("Should I include date and time?")
        snfm = take_command()
        if "yes" in snfm or "sure" in snfm:
            strTime = datetime.now().strftime("%d/%m/%Y %H:%M:%S")
            file.write(strTime + " :- " + note)
        else:
            file.write(note)
        file.close()
        talk("Note added")
    elif "show note" in command:
        talk("Showing Notes")
        file = open("jarvis.txt", "r")
        note = file.read()
        print(note)
        talk(note)
        file.close()
    elif "who is" in command:
        person = command.replace("who is", "")
        info = wikipedia.summary(person, 1)
        print(info)
        talk("According to Wikipedia, " + info)
    elif "open google" in command:
        talk("Opening Google")
        webbrowser.open("https://google.com")
    elif "wish me" in command:
        hour = datetime.now().hour
        if hour < 12:
            talk("Good morning sir!")
        elif hour < 18:
            talk("Good afternoon sir!")
        else:
            talk("Good evening sir!")
    elif "date" in command:
        today = date.today()
        talk(f"Today's date is {today}")
    elif "question" in command:
        talk("What is your question?")
        question = take_command()
        app_id = "G5JUAG-5TRE8XAT2Q"
        client = wolframalpha.Client(app_id)
        res = client.query(question)
        answer = next(res.results).text
        print(answer)
        talk(answer)
    elif "next birthday" in command:
        talk("Enter your next birth date")
        birthday = input("What is your next B'day Date? (in DD/MM/YYYY): ")
        birthdate = datetime.strptime(birthday, "%d/%m/%Y").date()
        today = date.today()
        days = abs(birthdate - today)
        print(days.days)
        talk(f"There are {days.days} days left for your next birthday")
    elif "open youtube" in command:
        talk("Opening YouTube")
        webbrowser.open("https://youtube.com")
    elif "are you single" in command or "i love you" in command:
        talk("I am in a relationship with WiFi.")
    elif "joke" in command:
        talk(pyjokes.get_joke())
    elif "show calendar" in command:
        talk("Enter the year you want me to display")
        yy = int(input("Enter year: "))
        talk("Enter the month you want me to display")
        mm = int(input("Enter month: "))
        print(calendar.month(yy, mm))
    elif "set alarm" in command:
        talk("Please enter the time")
        alarmHour = int(input("Enter hour: "))
        alarmMin = int(input("Enter Minutes: "))
        alarmAm = input("am/pm: ")
        if alarmAm.lower() == "pm":
            alarmHour += 12
        while True:
            now = datetime.now()
            if alarmHour == now.hour and alarmMin == now.minute:
                print("Playing alarm...")
                playsound("C:/ALEXA_MP/Standard Alarm Clock.mp3")
                break
        talk("Time up")
    elif "set reminder" in command:
        while True:
            notification.notify(
                title="Drink Water!",
                message="You need water to stay hydrated and maintain an adequate amount of fluid in your body.",
                app_icon="E:/python_alexa/icon.ico",
                timeout=5,
            )
            time.sleep(20)
    elif "stop" in command or "goodbye" in command:
        talk("See you next time!")
        exit()
    else:
        talk("Please say the command again.")


while True:
    run_alexa()