import speech_recognition as sr
import pyttsx3
import openai
import pyaudio
import datetime
import os
import webbrowser

openai.api_key = "Your _API_KEY"

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def recognize_speech():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        try:
            audio = recognizer.listen(source, timeout=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"User said: {command}")
            return command
        except sr.UnknownValueError:
            print("Sorry, I couldn't understand that.")
            speak("Sorry, I couldn't understand that.")
        except sr.RequestError:
            print("Speech service error.")
            speak("Speech service error.")
    return ""

def get_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"


def perform_task(command):
    if "hello" in command:
        response = f"Hallo"
        speak(response)

    elif "time" in command:
        current_time = datetime.datetime.now().strftime("%I:%M %p")
        response = f"The current time is {current_time}."
        speak(response)
    
    elif "date" in command:
        current_date = datetime.datetime.now().strftime("%A, %B %d, %Y")
        response = f"Today's date is {current_date}."
        speak(response)

    elif "open notepad" in command:
        os.system("notepad.exe")
        response = "Opening Notepad."
        speak(response)

    elif "open youtube" in command:
        webbrowser.open("https://www.youtube.com")
        response = "Opening YouTube."
        speak(response)

    elif "search" in command:
        query = command.replace("search", "").strip()
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        response = f"Searching for {query} on Google."
        speak(response)

    else:
        response = get_ai_response(command)
        speak(response)

    return response

if __name__ == "__main__":
    speak("Hello! I am your AI assistant. How can I help you today?")
    while True:
        command = recognize_speech()
        if "exit" in command or "stop" in command:
            speak("Goodbye!")
            break
        elif command:
            response = perform_task(command)
            print("Assistant:", response)
