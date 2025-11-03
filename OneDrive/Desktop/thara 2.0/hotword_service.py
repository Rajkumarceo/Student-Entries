import os
import sys
import time
import subprocess
import speech_recognition as sr
import threading

def listen_for_hotword(hotword="hello purple"):
    recognizer = sr.Recognizer()
    mic = None
    while True:
        try:
            if mic is None:
                mic = sr.Microphone()
            with mic as source:
                print("[Hotword Service] Listening for hotword... (say 'hello purple')")
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                audio = recognizer.listen(source, timeout=10, phrase_time_limit=5)
            try:
                query = recognizer.recognize_google(audio, language='en-in').lower().strip()
                print(f"[Hotword Service] Heard: {query}")
                if hotword in query:
                    print(f"[Hotword Service] Hotword '{hotword}' detected! Launching assistant...")
                    launch_assistant()
                    time.sleep(10)  # Prevent rapid re-trigger
            except sr.UnknownValueError:
                pass  # Ignore unrecognized speech
            except sr.RequestError as e:
                print(f"[Hotword Service] Speech recognition error: {e}")
                time.sleep(5)
        except Exception as e:
            print(f"[Hotword Service] Error: {e}")
            time.sleep(5)

def launch_assistant():
    # Launch the main assistant script in a new process
    script_path = os.path.join(os.path.dirname(__file__), "main.py")
    if os.path.exists(script_path):
        subprocess.Popen([sys.executable, script_path], shell=True)
    else:
        print(f"[Hotword Service] main.py not found at {script_path}")

def main():
    print("[Hotword Service] Starting background hotword listener...")
    listen_thread = threading.Thread(target=listen_for_hotword, daemon=True)
    listen_thread.start()
    while True:
        time.sleep(60)  # Keep the service alive

if __name__ == "__main__":
    main()
