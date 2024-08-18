import speech_recognition as sr
from gtts import gTTS
import os

recognizer = sr.Recognizer()

# Define command stages
commands = {
    "set reminder": {"response": "Sure, for what time?", "next": "reminder_time"},
    "reminder_time": {"response": "Reminder set for {time}.", "final": True},
    "what is your name": {"response": "I am your voice assistant."},
    "hello": {"response": "Hello! How can I help you today?"},
    "exit": {"response": "Goodbye!", "final": True}
}

# Store state
current_state = None

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
    global current_state

    if current_state and command in commands[current_state]:
        response_data = commands[current_state]
        if "{time}" in response_data["response"]:
            response_text = response_data["response"].format(time=command)
        else:
            response_text = response_data["response"]
        print(response_text)
        speak_response(response_text)
        if "final" in response_data and response_data["final"]:
            current_state = None
    elif command in commands:
        response_data = commands[command]
        response_text = response_data["response"]
        print(response_text)
        speak_response(response_text)
        if "next" in response_data:
            current_state = response_data["next"]
        elif "final" in response_data and response_data["final"]:
            current_state = None
    else:
        print("Command not recognized.")
        speak_response("Sorry, I did not understand that.")

def speak_response(response_text):
    tts = gTTS(response_text, lang='en')
    tts.save("response.mp3")
    os.system("ffplay -nodisp -autoexit response.mp3")
    # os.system("afplay response.mp3")  # On macOS
    # os.system("start response.mp3")  # On Windows

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
