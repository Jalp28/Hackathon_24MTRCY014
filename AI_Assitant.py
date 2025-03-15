import speech_recognition as sr
import pyttsx3
import openai
import pyaudio
import datetime
import os
import webbrowser

# Initialize AI Engine
openai.api_key = "Your _API_KEY"

# Initialize Speech Engine
engine = pyttsx3.init()

# Function: Speak AI Responses
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Function: Recognize Speech Commands
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

# Function: Get AI Response (Using GPT-4)
def get_ai_response(prompt):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4",
            messages=[{"role": "user", "content": prompt}]
        )
        return response['choices'][0]['message']['content']
    except Exception as e:
        return f"Error: {str(e)}"

# Function: Perform Actions Based on Commands
def perform_task(command):
    if "hello" in command:
        response = f"Hallo"
        speak(response)
    
    elif "how are you?" in command:
        response = f"I m Fine"
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
        # Get AI-generated response if no direct command matches
        response = get_ai_response(command)
        speak(response)

    return response

# Main Loop
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
