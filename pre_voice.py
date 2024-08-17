import speech_recognition as sr
from gtts import gTTS
import os

# Initialize recognizer
recognizer = sr.Recognizer()

# Define preset commands and responses
commands = {
    "hello": "Hello! How can I help you today?",
    "what is your name": "I am your voice assistant.",
    "exit": "Goodbye!"
}

def listen_command():
    with sr.Microphone() as source:
        print("Listening...")
        try:
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=5)
            command = recognizer.recognize_google(audio).lower()
            print(f"You said: {command}")
            return command
        except sr.WaitTimeoutError:
            print("Listening timed out while waiting for phrase to start")
            return ""
        except sr.UnknownValueError:
            print("Sorry, I did not understand that.")
            return ""
        except sr.RequestError:
            print("Sorry, my speech service is down.")
            return ""

def respond_to_command(command):
    if command in commands:
        response = commands[command]
        print(response)
        
        # Convert text to speech using gTTS
        tts = gTTS(response, lang='en')
        tts.save("response.mp3")
        
        # Play the response audio (use 'afplay' for macOS, 'start' for Windows)
        os.system("afplay response.mp3")  # On macOS
        # os.system("start response.mp3")  # On Windows
        
        if command == "exit":
            return False
    else:
        print("Command not recognized.")
    return True

def main():
    running = True
    while running:
        command = listen_command()
        if command:
            running = respond_to_command(command)

if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nProgram interrupted by user. Exiting...")
