import os
import sys
import time
import subprocess
import speech_recognition as sr
import threading
import psutil

def listen_for_hotword(hotword="hello purple"):
    recognizer = sr.Recognizer()
    mic = None
    print("[Hotword Service] Starting... Press Ctrl+C to exit cleanly")
    while True:
        try:
            if mic is None:
                mic = sr.Microphone()
            with mic as source:
                print("\r[Hotword Service] Listening for 'hello purple'...", end="", flush=True)
                recognizer.adjust_for_ambient_noise(source, duration=0.5)
                # Responsive hotword detection: short listen window
                audio = recognizer.listen(source, timeout=5, phrase_time_limit=3)
            try:
                query = recognizer.recognize_google(audio, language='en-in').lower().strip()
                print(f"\r[Hotword Service] Heard: {query}" + " "*20)
                if hotword in query:
                    print(f"[Hotword Service] Hotword '{hotword}' detected! Launching assistant...")
                    launch_assistant()
                    time.sleep(10)  # Prevent rapid re-trigger
            except sr.UnknownValueError:
                pass  # Ignore unrecognized speech
            except sr.RequestError as e:
                print(f"\r[Hotword Service] Speech recognition error: {e}" + " "*20)
                time.sleep(5)
        except Exception as e:
            print(f"\r[Hotword Service] Error: {e}" + " "*20)
            time.sleep(5)
        except KeyboardInterrupt:
            print("\n[Hotword Service] Shutting down cleanly...")
            break

def launch_assistant():
    """Launch the main assistant script in a new process"""
    try:
        # Get the absolute path to main.py
        script_dir = os.path.dirname(os.path.abspath(__file__))
        main_script = os.path.join(script_dir, "main.py")
        
        if os.path.exists(main_script):
            # If an instance of main.py is already running, do not spawn another
            for p in psutil.process_iter(['pid', 'name', 'cmdline']):
                try:
                    cmdline = p.info.get('cmdline') or []
                    if any('main.py' in str(x) for x in cmdline):
                        print(f"[Hotword Service] Assistant already running (pid={p.pid}). Skipping launch.")
                        return
                except (psutil.NoSuchProcess, psutil.AccessDenied):
                    continue

            # Use CREATE_NEW_CONSOLE flag to open in new window
            CREATE_NEW_CONSOLE = 0x00000010
            subprocess.Popen([sys.executable, main_script],
                           creationflags=CREATE_NEW_CONSOLE,
                           cwd=script_dir)
            print(f"[Hotword Service] Launched assistant: {main_script}")
        else:
            print(f"[Hotword Service] Error: main.py not found at {main_script}")
    except Exception as e:
        print(f"[Hotword Service] Error launching assistant: {e}")

def main():
    """Main service loop with error handling"""
    running = True
    while running:
        try:
            print("[Hotword Service] Starting background hotword listener...")
            listen_for_hotword()
        except KeyboardInterrupt:
            print("\n[Hotword Service] Received shutdown signal...")
            running = False
        except Exception as e:
            print(f"[Hotword Service] Error in main loop: {e}")
            print("[Hotword Service] Restarting in 5 seconds...")
            time.sleep(5)
    
    print("[Hotword Service] Exiting normally...")

if __name__ == "__main__":
    main()
