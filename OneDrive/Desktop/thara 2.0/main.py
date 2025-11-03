import datetime
import os
import sys
import time
import webbrowser
import pyttsx3
import speech_recognition as sr
import pyautogui
import json
import pickle
import numpy as np
import random
import urllib.parse
import requests
import psutil
import subprocess
from bs4 import BeautifulSoup
try:
    from tensorflow import keras
    try:
        # Try the standard import path (works for TensorFlow < 2.10)
        from tensorflow.keras.preprocessing.sequence import pad_sequences  # type: ignore
    except ImportError:
        try:
            # Fallback for newer TensorFlow versions (2.10+)
            from tensorflow.keras.utils import pad_sequences  # type: ignore
        except ImportError:
            try:
                # Alternative fallback for standalone keras
                from keras.preprocessing.sequence import pad_sequences  # type: ignore
            except ImportError:
                # If all imports fail, pad_sequences will be None
                pad_sequences = None
except ImportError:
    keras = None
    pad_sequences = None

def initialize_engine():
    engine=pyttsx3.init("sapi5")
    voices=engine.getProperty('voices')
    engine.setProperty('voice',voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate',150)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume+0.25)
    return engine

def speak(text):
    engine=initialize_engine()
    engine.say(text)
    engine.runAndWait()

def command():
    r = sr.Recognizer()
    
    try:
        # Check if microphone is available
        try:
            mic_list = sr.Microphone.list_microphone_names()
            if len(mic_list) == 0:
                print("✗ No microphones found!")
                return None
            print(f"✓ Found {len(mic_list)} microphone(s)")
        except Exception as e:
            print(f"⚠ Warning: Could not list microphones: {e}")
            # Continue anyway
        
        try:
            with sr.Microphone() as source:
                print("Adjusting for ambient noise...", end="", flush=True)
                try:
                    # Shorter adjustment time for faster response
                    r.adjust_for_ambient_noise(source, duration=0.5)
                    print(" Done!")
                except Exception as e:
                    print(f" Warning: {e}")
                    # Continue anyway with default settings
                
                # Set reasonable thresholds - optimized for longer speech
                r.energy_threshold = 300  # Lower threshold for better sensitivity
                r.pause_threshold = 1.5  # Longer pause to allow for thinking/pauses in longer questions
                r.dynamic_energy_threshold = True
                r.dynamic_energy_adjustment_damping = 0.15
                r.dynamic_energy_ratio = 1.5
                
                print("🎤 Listening... (speak your question/command - you have up to 60 seconds)", end="", flush=True)
                
                try:
                    # Listen for audio with extended timeout for longer questions
                    # Increased timeout to 60 seconds and phrase_time_limit to 45 seconds
                    # This allows for longer, more detailed questions
                    audio = r.listen(source, timeout=60, phrase_time_limit=45)
                    print("\r✓ Audio captured! Processing your question...", end="", flush=True)
                except sr.WaitTimeoutError:
                    print("\r✗ Timeout: No speech detected within 60 seconds.")
                    print("   Troubleshooting:")
                    print("   - Make sure your microphone is not muted")
                    print("   - Check Windows microphone permissions")
                    print("   - Speak louder or closer to the microphone")
                    print("   - You have 60 seconds to speak - take your time")
                    print("   - Try typing 'text' to switch to text input")
                    return None
                except Exception as e:
                    print(f"\r✗ Error listening: {e}")
                    print(f"   Error type: {type(e).__name__}")
                    return None
            
            # Recognize the audio
            try:
                print("\r   Processing... This may take a moment for longer questions...", end="", flush=True)
                query = r.recognize_google(audio, language='en-in')
                query_clean = query.lower().strip()
                
                # Show length of recognized query
                word_count = len(query_clean.split())
                print(f"\r✓ Recognized ({word_count} words): '{query_clean[:100]}{'...' if len(query_clean) > 100 else ''}'")
                print(f"   Full query length: {len(query_clean)} characters")
                print(f"   Verification: Command received and will be processed\n")
                return query_clean
                
            except sr.UnknownValueError:
                print("\r✗ Could not understand audio. Please speak more clearly.")
                print("   Verification: Audio captured but unclear - please repeat")
                return None
            except sr.RequestError as e:
                print(f"\r✗ Speech recognition service error: {e}")
                print("   Please check your internet connection.")
                print("   Verification: Google Speech API connection failed")
                return None
                
        except OSError as e:
            if "Invalid input device" in str(e) or "No default input device" in str(e):
                print(f"\r✗ Microphone not accessible: {e}")
                print("   Please check Windows microphone settings.")
            else:
                print(f"\r✗ Microphone error: {e}")
            return None
            
    except Exception as e:
        print(f"\r✗ Unexpected error: {type(e).__name__}: {e}")
        import traceback
        traceback.print_exc()
        return None

def cal_day():
    day=datetime.datetime.today().weekday() + 1
    day_dict={
        1:"MONDAY",
        2:"TUESDAY",
        3:"WEDNESDAY",
        4:"THURSDAY",
        5:"FRIDAY",
        6:"SATURDAY",
        7:"SUNDAY"
    }
    if day in day_dict.keys():
        day_ofweek=day_dict[day]
        print(day_ofweek)
        return day_ofweek
    return None

def wishMe():
    hour = int(datetime.datetime.now().hour)
    t=time.strftime("%H:%M:%S")
    day = cal_day()
    day_str = day if day else "today"
    if hour>=0 and hour<12 and ("Am"in t):
        speak(f"Good Morning boss!,it's {day_str} and the time is {t}" )
    elif hour>=12 and hour<18:
        speak(f"Good Afternoon boss!,it's {day_str} and the time is {t}" )
    else:
        speak(f"Good Evening boss!,it's {day_str} and the time is {t}" )
    speak("I am purple,your personal assistant")
def social_media(command):
    if 'facebook' in command:
        speak("opening your facebook")
        webbrowser.open("https://www.facebook.com/")
    elif 'whatsapp' in command:
        speak("opening your whatsapp")
        webbrowser.open("https://web.whatsapp.com/")
    elif 'instagram' in command:
        speak("opening your instagramm")
        webbrowser.open("https://www.instagram.com/?__pwa=1")  
    elif 'youtube' in command:
        speak("opening your youtube")
        webbrowser.open("https://www.youtube.com/")
    elif 'chatgpt' in command:
        speak("opening your chatgpt")
        webbrowser.open("https://chatgpt.com/")
    else:
        speak("no result found")

def close_social_media(command):
    """Close social media apps/tabs using keyboard shortcuts and process termination"""
    app_info = {
        "facebook": "Facebook",
        "whatsapp": "WhatsApp",
        "instagram": "Instagram",
        "youtube": "YouTube",
        "chatgpt": "ChatGPT"
    }
    
    app_name = None
    
    # Find which app to close
    for key, name in app_info.items():
        if key in command:
            app_name = name
            break
    
    if not app_name:
        speak("I couldn't find that social media app to close")
        return False
    
    speak(f"boss closing {app_name}")
    
    # Method 1: Try keyboard shortcut (Ctrl+W) - works if browser is focused
    # This is the most reliable method for closing browser tabs
    try:
        time.sleep(0.3)
        pyautogui.hotkey('ctrl', 'w')
        time.sleep(0.5)
        print(f"✓ Sent Ctrl+W to close {app_name} tab")
        speak(f"{app_name} tab has been closed")
        return True
    except Exception as e:
        print(f"⚠ Keyboard shortcut method error: {e}")
    
    # Method 2: Try to find and activate browser window using win32gui (if available)
    try:
        import win32gui
        import win32con
        browser_keywords = ["chrome", "edge", "firefox", "brave", "opera"]
        
        def enum_handler(hwnd, windows):
            if win32gui.IsWindowVisible(hwnd):
                window_title = win32gui.GetWindowText(hwnd).lower()
                # Check if window title contains browser or social media keywords
                if any(keyword in window_title for keyword in browser_keywords) or \
                   any(app.lower() in window_title for app in app_info.values()):
                    windows.append((hwnd, window_title))
        
        windows = []
        win32gui.EnumWindows(enum_handler, windows)
        
        if windows:
            # Try to activate the browser window and close tab
            hwnd, window_title = windows[0]
            try:
                win32gui.ShowWindow(hwnd, win32con.SW_RESTORE)
                win32gui.SetForegroundWindow(hwnd)
                time.sleep(0.4)
                pyautogui.hotkey('ctrl', 'w')
                time.sleep(0.3)
                print(f"✓ Activated and closed {app_name} tab in browser window")
                speak(f"{app_name} tab has been closed")
                return True
            except Exception as e:
                print(f"⚠ Window activation error: {e}")
    except ImportError:
        print("⚠ win32gui not available, skipping window activation method")
    except Exception as e:
        print(f"⚠ Window management error: {e}")
    
    # Method 3: Try Alt+F4 to close active window (will close entire browser if focused)
    try:
        time.sleep(0.5)
        pyautogui.hotkey('alt', 'f4')
        time.sleep(0.3)
        print(f"✓ Sent Alt+F4 to close active window")
        speak(f"Closed window containing {app_name}")
        return True
    except Exception as e:
        print(f"⚠ Alt+F4 method error: {e}")
    
    # Method 4: Last resort - close browser processes (aggressive, closes all tabs)
    browser_processes = ["chrome.exe", "msedge.exe", "firefox.exe", "brave.exe", "opera.exe"]
    try:
        browser_procs = []
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name'].lower()
                if proc_name in [bp.lower() for bp in browser_processes]:
                    browser_procs.append(proc)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
        
        if browser_procs:
            # Close just one browser instance (the first one found)
            proc = browser_procs[0]
            try:
                proc.terminate()
                try:
                    proc.wait(timeout=2)
                except psutil.TimeoutExpired:
                    proc.kill()
                print(f"✓ Closed browser process for {app_name}")
                speak(f"Closed browser containing {app_name}")
                return True
            except Exception as e:
                print(f"⚠ Error closing browser process: {e}")
    except Exception as e:
        print(f"⚠ Process closing method error: {e}")
    
    speak(f"I tried to close {app_name}, but couldn't verify if it was successful. Please check manually.")
    return False 

def schedule ():
    day_obj = cal_day()
    if day_obj is None:
        speak("No schedule found for today")
        return
    day = day_obj.lower()
    speak("boss today's schedule is")  
    week={
        "monday": "boss, from 5:30 pm  to 6:30pm you have llm traing  ,from 6:30pm to 7:30pm you have to verify the pyhton backend class wheather that is going smooth,from 7:30pm to 8:00 pm your dinner time ,from 8:10pm to 9:10pm you have java class.",
        "tuesday": "boss, from 5:30 pm  to 6:30pm you have llm traing  ,from 6:30pm to 7:30pm you have to verify the pyhton backend class wheather that is going smooth,from 7:30pm to 8:00 pm your dinner time ,from 8:10pm to 9:10pm you have java class.",
        "wednesday":"boss you have an epic work ",
        "thursday":"boss you exams are going to come kindly prepare for it.",
        "friday":"boss you need to take survey of the class.",
        "saturday":"boss you can free working",
        "sunday":" boss you can be relaxed for today but ur exam on tomorrow so kindly prepare for it."
    }
    if day in week.keys():
        schedule_text = week[day]
        speak(schedule_text)
    else:
        speak("No schedule found for today")

            
def openApp(command):
    if "calculator" in command:
        speak("boss your calculator is opening")
        # Try newer Calculator app first (Windows 10+), then fallback to calc.exe
        try:
            os.system('start ms-calculator:')
        except:
            try:
                os.startfile('C:\\Windows\\System32\\calc.exe')
            except:
                os.system('calc')
    elif "notepad" in command:
        speak("boss your notepad is opening")
        os.startfile('C:\\Windows\\System32\\notepad.exe')    
    elif "paint" in command:
        speak("boss your paint is opening")
        os.system('start mspaint')
    elif "word" in command:
        speak("boss your ms word is opening")
        os.system('start winword')
    elif "excel" in command:
        speak("boss your ms excel is opening")
        os.system('start excel')       
    elif "visual studio code" in command or "vscode" in command or ("code" in command and "visual" in command):
        speak("boss opening Visual Studio Code")
        # Try common VS Code installation paths
        code_paths = [
            os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Microsoft VS Code', 'Code.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'), 'Microsoft VS Code', 'Code.exe'),
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Microsoft VS Code', 'Code.exe')
        ]
        opened = False
        for path in code_paths:
            try:
                if path and os.path.exists(path):
                    os.startfile(path)
                    opened = True
                    print(f"✓ Opened VS Code from: {path}")
                    break
            except Exception as e:
                print(f"⚠ VS Code open error for {path}: {e}")
        if not opened:
            # Fallback: try the 'code' CLI or open via start
            try:
                os.system('start code')
                opened = True
            except Exception as e:
                print(f"⚠ Fallback VS Code open failed: {e}")

        if not opened:
            # Final fallback: open VS Code download page
            webbrowser.open('https://code.visualstudio.com/')
            speak('Could not find installed VS Code. I opened the download page instead.')

    elif "cursor" in command:
        speak("boss opening Cursor")
        # Try to open a likely installed Cursor app; otherwise open the website
        cursor_paths = [
            os.path.join(os.environ.get('LOCALAPPDATA', ''), 'Programs', 'Cursor', 'Cursor.exe'),
            os.path.join(os.environ.get('PROGRAMFILES', 'C:\\Program Files'), 'Cursor', 'Cursor.exe'),
            os.path.join(os.environ.get('PROGRAMFILES(X86)', 'C:\\Program Files (x86)'), 'Cursor', 'Cursor.exe')
        ]
        opened_cursor = False
        for path in cursor_paths:
            try:
                if path and os.path.exists(path):
                    os.startfile(path)
                    opened_cursor = True
                    print(f"✓ Opened Cursor from: {path}")
                    break
            except Exception as e:
                print(f"⚠ Cursor open error for {path}: {e}")
        if not opened_cursor:
            # Fallback to web version
            try:
                webbrowser.open('https://www.cursor.so/')
                opened_cursor = True
                print('✓ Opened Cursor website')
            except Exception as e:
                print(f"✗ Could not open Cursor: {e}")
    else:
        speak("I couldn't find that application")

def closeApp(command):
    """Close applications using multiple methods for reliability"""
    app_processes = {
        "calculator": ["Calculator.exe", "calc.exe", "Calculator"],
        "notepad": ["notepad.exe", "Notepad"],
        "paint": ["mspaint.exe", "Paint"],
        "word": ["WINWORD.EXE", "winword.exe", "WINWORD"],
        "excel": ["EXCEL.EXE", "excel.exe", "EXCEL"],
        "vscode": ["Code.exe", "code.exe", "Code - Insiders.exe"],
        "cursor": ["Cursor.exe", "cursor.exe"]
    }
    
    app_name = None
    process_names = None
    
    # Find which app to close
    if "calculator" in command:
        app_name = "calculator"
        process_names = app_processes["calculator"]
    elif "notepad" in command:
        app_name = "notepad"
        process_names = app_processes["notepad"]
    elif "paint" in command:
        app_name = "paint"
        process_names = app_processes["paint"]
    elif "word" in command:
        app_name = "ms word"
        process_names = app_processes["word"]
    elif "excel" in command:
        app_name = "ms excel"
        process_names = app_processes["excel"]
    elif "visual studio code" in command or "vscode" in command or ("code" in command and "visual" in command):
        app_name = "visual studio code"
        process_names = app_processes["vscode"]
    elif "cursor" in command:
        app_name = "cursor"
        process_names = app_processes["cursor"]
    else:
        speak("I couldn't find that application to close")
        return False
    
    if not process_names:
        speak(f"I couldn't find that application to close")
        return False
    
    speak(f"boss closing {app_name}")
    processes_closed = []
    
    # Method 1: Use taskkill first (more reliable on Windows)
    for process_name in process_names:
        try:
            # Try taskkill with force flag
            result = subprocess.run(['taskkill', '/f', '/im', process_name], 
                                   capture_output=True, timeout=5, text=True)
            if result.returncode == 0:
                processes_closed.append(process_name)
                print(f"✓ Closed {process_name} using taskkill")
            elif "not found" not in result.stderr.lower() and "does not exist" not in result.stderr.lower():
                # Process might exist but couldn't close - try alternative
                print(f"⚠ taskkill returned: {result.stderr}")
        except subprocess.TimeoutExpired:
            print(f"⚠ Timeout closing {process_name}")
        except Exception as e:
            print(f"⚠ Error with taskkill for {process_name}: {e}")
    
    # Method 2: Use psutil to find and terminate ALL matching processes
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name = proc.info['name']
                proc_name_lower = proc_name.lower()
                for process_name in process_names:
                    if proc_name_lower == process_name.lower():
                        # Check if we already closed this
                        if proc_name not in processes_closed:
                            try:
                                proc.terminate()
                                try:
                                    proc.wait(timeout=2)
                                except psutil.TimeoutExpired:
                                    proc.kill()
                                    proc.wait(timeout=1)
                                processes_closed.append(proc_name)
                                print(f"✓ Closed {proc_name} (PID: {proc.info['pid']}) using psutil")
                            except psutil.NoSuchProcess:
                                pass  # Already closed
                            except psutil.AccessDenied as e:
                                # Try taskkill as alternative
                                try:
                                    subprocess.run(['taskkill', '/f', '/pid', str(proc.info['pid'])], 
                                                  capture_output=True, timeout=3)
                                    processes_closed.append(proc_name)
                                    print(f"✓ Closed {proc_name} (PID: {proc.info['pid']}) using taskkill /pid")
                                except:
                                    print(f"⚠ Access denied for {proc_name}: {e}")
                            except Exception as e:
                                print(f"⚠ Could not close {proc_name}: {e}")
            except (psutil.NoSuchProcess, psutil.AccessDenied, psutil.ZombieProcess):
                pass
    except Exception as e:
        print(f"⚠ psutil method error: {e}")
    
    # Method 3: Special handling for Calculator (Windows Store App)
    if "calculator" in command and not processes_closed:
        try:
            # Try closing Calculator using Windows App execution alias
            result = subprocess.run(['powershell', '-Command', 
                                    'Get-Process | Where-Object {$_.ProcessName -like "*Calculator*" -or $_.MainWindowTitle -like "*Calculator*"} | Stop-Process -Force'],
                                  capture_output=True, timeout=5)
            if result.returncode == 0:
                processes_closed.append("Calculator")
                print(f"✓ Closed Calculator using PowerShell")
        except Exception as e:
            print(f"⚠ PowerShell method error: {e}")
    
    # Verify processes are actually closed
    time.sleep(0.8)  # Give processes time to close
    
    still_running = []
    try:
        for proc in psutil.process_iter(['pid', 'name']):
            try:
                proc_name_lower = proc.info['name'].lower()
                for process_name in process_names:
                    if proc_name_lower == process_name.lower():
                        still_running.append(proc.info['name'])
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                pass
    except:
        pass
    
    if processes_closed and not still_running:
        speak(f"{app_name} has been closed")
        return True
    elif processes_closed:
        print(f"⚠ Some processes may still be running: {still_running}")
        speak(f"{app_name} closing attempted. Please check if it's closed.")
        return True
    elif still_running:
        print(f"⚠ Could not close processes: {still_running}")
        speak(f"I tried to close {app_name} but it may still be running.")
        return False
    else:
        speak(f"I couldn't find {app_name} running. It may already be closed.")
        print(f"⚠ Could not find {app_name} processes to close.")
        return False

def extract_search_term(query_text):
    """Extract search term from various command formats - improved"""
    query_lower = query_text.lower().strip()
    original_query = query_text.strip()
    
    # Extended list of prefixes and patterns
    prefixes_to_remove = [
        "search for", "search google for", "google search for", "search in google for",
        "search in edge for", "edge search for",
        "google search", "search google", "search in google",
        "tell me about", "information about", "info about",
        "what is", "what are", "what was", "what were",
        "who is", "who are", "who was", "who were",
        "where is", "where are", "where was",
        "when is", "when are", "when was",
        "why is", "why are", "why was",
        "how to", "how do", "how does", "how did",
        "find", "look for", "find information about",
        "search", "google", "find out"
    ]
    
    search_term = original_query
    
    # Try to match prefixes (case-insensitive)
    for prefix in prefixes_to_remove:
        if query_lower.startswith(prefix):
            search_term = original_query[len(prefix):].strip()
            break
    
    # Additional cleanup - remove common connector words
    connectors = ["for ", "about ", "on ", "regarding ", "concerning "]
    for connector in connectors:
        if search_term.lower().startswith(connector):
            search_term = search_term[len(connector):].strip()
    
    # Remove trailing punctuation and extra whitespace
    search_term = search_term.strip(".,!?;:")
    while "  " in search_term:
        search_term = search_term.replace("  ", " ")
    
    # If we ended up with nothing or very short, use original
    if not search_term or len(search_term.strip()) < 2:
        # Fallback: remove only obvious prefixes
        for prefix in ["search", "google", "find"]:
            if query_lower.startswith(prefix + " ") and len(query_lower.split()) > 1:
                search_term = " ".join(original_query.split()[1:])
                break
        else:
            search_term = original_query
    
    return search_term.strip()

def search_google(query_text, use_edge=False):
    """Search Google/Edge and extract information"""
    try:
        # Extract the actual search term
        search_term = extract_search_term(query_text)
        print(f"🔍 Extracted search term: '{search_term}'")
        
        if not search_term or len(search_term.strip()) < 2:
            print("⚠ Warning: Search term too short or empty")
            speak("I couldn't understand what to search for. Please specify a search term.")
            # Try to use original query as fallback
            if len(query_text.strip()) > 2:
                search_term = query_text.strip()
                print(f"   Using original query as fallback: '{search_term}'")
            else:
                return None
        
        # Encode the search query
        encoded_query = urllib.parse.quote_plus(search_term)
        search_url = f"https://www.google.com/search?q={encoded_query}"
        
        # Open in browser first
        try:
            if use_edge:
                # Try to open in Edge
                edge_paths = [
                    "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
                    "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe"
                ]
                for path in edge_paths:
                    if os.path.exists(path):
                        os.startfile(path)
                        time.sleep(1)
                        pyautogui.write(search_url)
                        pyautogui.press('enter')
                        break
                else:
                    webbrowser.open(search_url)
            else:
                webbrowser.open(search_url)
            
            print(f"✓ Opened search in browser: {search_term}")
            speak(f"Opening search for {search_term}")
            
            # After opening search, exit the program as requested
            print("\n✓ Search opened in browser. Exiting program...")
            speak("Search results are now open in your browser. Goodbye boss!")
            time.sleep(1)  # Brief delay before exit
            return "EXIT_PROGRAM"
        except Exception as e:
            print(f"⚠ Browser open error: {e}")
            # Still try to exit even if there was an error opening
            speak("I tried to open the search. Goodbye boss!")
            return "EXIT_PROGRAM"
        
    except Exception as e:
        print(f"✗ Search error: {e}")
        import traceback
        traceback.print_exc()
        speak("Sorry boss, I encountered an error performing the search")
        return None

def condition():
    speak("checking the system condition")
    try:
        os.system("systeminfo")
        speak("system condition checked")
        print("--------------------------------")
        print("CPU usage:")
        print("--------------------------------")
        
        # CPU usage
        cpu_percent = psutil.cpu_percent(interval=1)
        speak(f"CPU usage: {cpu_percent}%")
        print(f"CPU usage: {cpu_percent}%")

        if (cpu_percent > 80):
            speak("boss your cpu usage is high")
            print("boss your cpu usage is high")
        elif(cpu_percent > 60):
            speak("boss your cpu usage is medium")
            print("boss your cpu usage is medium")
        elif(cpu_percent > 40):
            speak("boss your cpu usage is medium")
            print("boss your cpu usage is medium")
        elif(cpu_percent > 20):
            speak("boss your cpu usage is low")
            print("boss your cpu usage is low")
        else:
            speak("boss your cpu usage is very low")
            print("boss your cpu usage is very low")
            speak("boss your cpu usage is low")
            print("boss your cpu usage is low")
        
        # Memory information
        memory = psutil.virtual_memory()
        memory_total_gb = memory.total / (1024**3)  # Convert to GB
        memory_used_gb = memory.used / (1024**3)
        memory_percent = memory.percent
        print(f"Virtual memory: {memory_total_gb:.2f} GB total, {memory_used_gb:.2f} GB used ({memory_percent}%)")
        speak(f"Memory usage is {memory_percent} percent")
        
        # Disk usage - Windows uses C: drive
        try:
            disk = psutil.disk_usage('C:\\')
            disk_total_gb = disk.total / (1024**3)
            disk_used_gb = disk.used / (1024**3)
            disk_percent = (disk.used / disk.total) * 100
            print(f"Disk usage (C:): {disk_total_gb:.2f} GB total, {disk_used_gb:.2f} GB used ({disk_percent:.1f}%)")
            speak(f"Disk usage is {disk_percent:.1f} percent")
        except Exception as e:
            print(f"Could not get disk usage: {e}")
        
        # Network I/O
        try:
            net_io = psutil.net_io_counters()
            bytes_sent_mb = net_io.bytes_sent / (1024**2)
            bytes_recv_mb = net_io.bytes_recv / (1024**2)
            print(f"Network I/O: {bytes_sent_mb:.2f} MB sent, {bytes_recv_mb:.2f} MB received")
        except Exception as e:
            print(f"Could not get network info: {e}")
        
        # Temperature sensors (might not be available on all systems)
        try:
            temps = psutil.sensors_temperatures()
            if temps:
                print(f"Sensors temperatures: {temps}")
            else:
                print("Temperature sensors not available")
        except AttributeError:
            print("Temperature sensors not supported on this system")
        except Exception as e:
            print(f"Could not get temperature: {e}")
        
        # Battery information (only for laptops)
        try:
            battery = psutil.sensors_battery()
            if battery:
                percentage = battery.percent
                plugged = battery.power_plugged
                status = "plugged in" if plugged else "not plugged in"
                speak(f"boss your battery percentage is {percentage}% and it is {status}")
                print(f"Battery: {percentage}% ({status})")
            else:
                speak("No battery detected. This appears to be a desktop computer")
                print("No battery detected (desktop system)")
        except Exception as e:
            print(f"Could not get battery info: {e}")
            speak("Could not retrieve battery information")
        
        print("--------------------------------")
        
    except Exception as e:
        print(f"Error checking system condition: {e}")
        speak("Sorry boss, there was an error checking the system condition")
        import traceback
        traceback.print_exc()


def load_settings(path="settings.json"):
    """Load assistant settings from a JSON file (creates default if missing)."""
    defaults = {"weather_enabled": False}
    try:
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                data = json.load(f)
            # Ensure defaults are present
            for k, v in defaults.items():
                data.setdefault(k, v)
            return data
        else:
            with open(path, "w", encoding="utf-8") as f:
                json.dump(defaults, f, indent=2)
            return defaults
    except Exception as e:
        print(f"⚠ Could not load settings: {e}")
        return defaults


def save_settings(settings, path="settings.json"):
    try:
        with open(path, "w", encoding="utf-8") as f:
            json.dump(settings, f, indent=2)
        return True
    except Exception as e:
        print(f"⚠ Could not save settings: {e}")
        return False


def enable_weather(settings, allow_offline=False):
    """Enable weather feature. If allow_offline=True will enable even without network.

    Returns a tuple (enabled: bool, message: str)
    """
    # quick network check: try a lightweight endpoint
    online = False
    try:
        resp = requests.get("http://clients3.google.com/generate_204", timeout=3)
        online = resp.status_code == 204
    except Exception:
        online = False

    if online:
        settings["weather_enabled"] = True
        save_settings(settings)
        msg = "Weather enabled and online — I'll fetch weather when requested."
        print("✓ Weather enabled (online)")
        speak(msg)
        return True, msg
    else:
        if allow_offline:
            settings["weather_enabled"] = True
            save_settings(settings)
            msg = "Weather enabled in offline mode. I will use cached data when available."
            print("✓ Weather enabled (offline)")
            speak(msg)
            return True, msg
        else:
            msg = "No internet connection. Weather not enabled."
            print("✗ Cannot enable weather — offline")
            speak(msg)
            return False, msg
if __name__ == "__main__":
    # Load chatbot model and components
    model = None
    tokenizer = None
    label_encoder = None
    chat_data = None
    
    if keras is None:
        print("⚠ TensorFlow/Keras not available. LLM features will be limited.")
    else:
        try:
            print("Loading LLM model and components...")
            if os.path.exists("chat_model.h5"):
                model = keras.models.load_model("chat_model.h5")
                print("✓ LLM model loaded")
            else:
                print("⚠ chat_model.h5 not found")
            
            if os.path.exists("tokenizer.pkl"):
                with open("tokenizer.pkl", "rb") as f:
                    tokenizer = pickle.load(f)
                print("✓ Tokenizer loaded")
            else:
                print("⚠ tokenizer.pkl not found")
            
            if os.path.exists("label_encoder.pkl"):
                with open("label_encoder.pkl", "rb") as encoder_file:
                    label_encoder = pickle.load(encoder_file)
                print("✓ Label encoder loaded")
            else:
                print("⚠ label_encoder.pkl not found")
            
            if os.path.exists("intents.json"):
                with open("intents.json") as file:
                    chat_data = json.load(file)
                print("✓ Intents data loaded")
            else:
                print("⚠ intents.json not found")
            
            if not all([model, tokenizer, label_encoder, chat_data, pad_sequences]):
                if pad_sequences is None:
                    print("⚠ pad_sequences import failed. LLM features will be disabled.")
                else:
                    print("⚠ Some LLM components are missing. LLM will work in limited mode.")
                model = None
                tokenizer = None
                label_encoder = None
                chat_data = None
        except Exception as e:
            print(f"⚠ Error loading chatbot model: {e}")
            print("   LLM features disabled, but other commands will work")
            model = None
            tokenizer = None
            label_encoder = None
            chat_data = None
    # Load assistant settings (persisted flags like weather_enabled)
    settings = load_settings()
    
    wishMe()
    speak("You can now speak your commands. Say 'exit' to quit. If voice recognition fails, you can also type commands.")
    
    # Ask user preference for input method
    use_voice = True
    print("\n" + "="*60)
    print("Voice Assistant Ready!")
    print("="*60)
    # Quick microphone check
    try:
        mics = sr.Microphone.list_microphone_names()
        print(f"\n✓ Detected {len(mics)} microphone(s)")
        if len(mics) > 0:
            print(f"  Default mic: {mics[0]}")
    except:
        print("\n⚠ Could not detect microphones")
    
    print("\nOptions:")
    print("1. Voice commands (requires working microphone)")
    print("2. Text commands (recommended if voice doesn't work)")
    print("\nEnter '1' or '2', or press Enter for voice (default): ", end="")
    
    try:
        choice = input().strip()
        if choice == "2":
            use_voice = False
            print("\n✓ Switched to text input mode.")
        else:
            print("\n✓ Using voice input mode.")
    except:
        print("\n✓ Using voice input mode (default).")
        pass  # Default to voice
    
    while True:
        try:
            # Use voice recognition or text input based on preference
            if use_voice:
                query = command()
                if query is None:
                    print("\n⚠ Voice recognition failed. Options:")
                    print("   1. Wait and try speaking again")
                    print("   2. Type 'text' to switch to text input")
                    print("   3. Type 'test' to test Google opening")
                    # Offer quick text input
                    try:
                        quick_input = input("\n   Or type command here (press Enter to retry voice): ").strip()
                        if quick_input:
                            if quick_input.lower() == "text":
                                use_voice = False
                                print("✓ Switched to text input mode.")
                                continue
                            elif quick_input.lower() == "test":
                                query = "open google"
                            else:
                                query = quick_input.lower()
                        else:
                            continue
                    except:
                        continue
                if query is None:
                    continue
            else:
                query = input("\nEnter your command: ").lower().strip()
                if not query:
                    continue
                print(f"DEBUG: Received command: '{query}'")
            
            if query == "text" and use_voice:
                use_voice = False
                print("Switched to text input mode.")
                continue
            elif query == "voice" and not use_voice:
                use_voice = True
                print("Switched to voice input mode.")
                continue
            
            if "exit" in query or query == "quit":
                speak("Goodbye boss!")
                sys.exit()
            elif "hello purple" in query_lower or query_lower.strip() == "hello purple":
                # User requested the special command to enable weather even if offline
                try:
                    # settings is loaded in __main__ (see below)
                    enabled, message = enable_weather(settings, allow_offline=True)
                    if enabled:
                        print(f"✓ hello purple command: {message}")
                    else:
                        print(f"✗ hello purple command: {message}")
                except Exception as e:
                    print(f"✗ Error handling 'hello purple' command: {e}")
                    speak("Sorry boss, I couldn't enable weather")
            elif("your timetable" in query) or ("schedule" in query) or ("my schedule" in query):
                print(f"✓ Schedule command detected: '{query}'")
                schedule()
                print("✓ Schedule completed")
            elif("volume up" in query) or ("increase the volume" in query):
                print(f"✓ Volume up command detected")
                pyautogui.press("volumeup")
                speak("boss your volume increased")
                print("✓ Volume increased")
            elif("volume down" in query) or ("decrease the volume" in query):
                print(f"✓ Volume down command detected")
                pyautogui.press("volumedown")
                speak("boss your volume decresed")
                print("✓ Volume decreased")
            elif("volume mute" in query) or ("mute the sound" in query):
                print(f"✓ Mute command detected")
                pyautogui.press("volumemute")
                speak("boss your volume muted")
                print("✓ Volume muted")
            # Check for close commands first (before open commands) - MUST be before open check
            else:
                query_lower = query.lower()
                is_close_command = ("close" in query_lower) or ("stop" in query_lower) or ("exit" in query_lower)
                has_app_name = ("calculator" in query_lower) or ("notepad" in query_lower) or ("paint" in query_lower) or ("word" in query_lower) or ("excel" in query_lower)
                
                if is_close_command and has_app_name:
                    print(f"✓ App closing command detected: '{query}'")
                    closeApp(query)
                    print("✓ App closing completed")
                elif has_app_name and not is_close_command:
                    print(f"✓ App opening command: '{query}'")
                    openApp(query)
                    print("✓ App opening completed")
                elif has_app_name:
                    print(f"⚠ Warning: App detected with close keyword but logic error: '{query}'")
                    print(f"   Debug: is_close_command={is_close_command}, has_app_name={has_app_name}")
                    speak("Detected close command. Attempting to close...")
                    closeApp(query)
                elif("search" in query_lower and "open" not in query_lower) or \
                 ("google" in query_lower and "open" not in query_lower and len(query.split()) > 1) or \
                 any(query_lower.startswith(prefix) for prefix in ["what is", "what are", "who is", "who are", "where is", "when is", "why is", "how to", "how do", "tell me about", "find", "look for", "information about"]):
                    print(f"✓ Search command detected: '{query}'")
                    use_edge = "edge" in query_lower or "microsoft edge" in query_lower
                    result = search_google(query, use_edge=use_edge)
                    if result == "EXIT_PROGRAM":
                        sys.exit()
                    elif result:
                        print(f"✓ Search result retrieved")
                        if len(result) > 50:
                            print(f"   Preview: {result[:100]}...")
                    else:
                        print("⚠ Search opened in browser but information extraction failed")
                elif("open google" in query_lower) or (query_lower.strip() == "google" and len(query.split()) == 1):
                    print(f"✓ Google open command detected: '{query}'")
                    speak("opening google")
                    success = False
                    try:
                        # Method 1: Using webbrowser module
                        webbrowser.open("https://www.google.com/")
                        time.sleep(0.3)
                        print("✓ Opened Google in browser")
                        success = True
                    except Exception as e:
                        print(f"  Method 1 failed: {e}")
                    
                    # Method 2: Using os.system
                    if not success:
                        try:
                            os.system('start https://www.google.com/')
                            print("✓ Opened Google using alternative method")
                            success = True
                        except Exception as e2:
                            print(f"  Method 2 failed: {e2}")
                    
                    if not success:
                        speak("Sorry boss, could not open Google. Please check your browser settings.")
                        print("✗ All methods to open Google failed")
                    else:
                        print("✓ Google is now open in your browser")
                        speak("Google has been opened in your browser")
                elif ("open edge" in query_lower) or (query_lower.strip() == "edge" and len(query.split()) == 1) or ('microsoft edge' in query_lower and "search" not in query_lower):
                    print(f"✓ Edge open command detected: '{query}'")
                    speak("opening microsoft edge")
                    # Try common Edge browser paths
                    edge_paths = [
                        "C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe",
                        "C:\\Program Files\\Microsoft\\Edge\\Application\\msedge.exe",
                        "C:\\Windows\\System32\\msedge.exe"
                    ]
                    edge_opened = False
                    for path in edge_paths:
                        if os.path.exists(path):
                            os.startfile(path)
                            time.sleep(0.5)
                            edge_opened = True
                            print(f"✓ Edge opened from: {path}")
                            speak("Microsoft Edge has been opened")
                            break
                    if not edge_opened:
                        # Fallback to opening Edge website
                        webbrowser.open("https://www.microsoft.com/en-us/edge")
                        print("✓ Opened Edge website")
                        speak("I've opened the Edge download page")
                # Check for close social media commands first (before open commands)
                elif any(word in query_lower for word in ["close", "stop", "exit"]) and \
                     (('facebook' in query_lower) or ('chatgpt' in query_lower) or ('youtube' in query_lower) or ('instagram' in query_lower) or ('whatsapp' in query_lower)):
                    print(f"✓ Social media closing command: '{query}'")
                    close_social_media(query)
                    print("✓ Social media closing completed")
                elif('facebook' in query_lower) or ('chatgpt' in query_lower) or ('youtube' in query_lower) or ('instagram' in query_lower) or ('whatsapp' in query_lower):
                    # Only open if "close", "stop", or "exit" is not in the query
                    if not any(word in query_lower for word in ["close", "stop", "exit"]):
                        social_media(query)
                elif ("system condition" in query_lower) or ("system status" in query_lower) or ("system information" in query_lower) or (query_lower.strip() in ["condition", "status", "information"] and len(query.split()) == 1):
                    print(f"✓ System condition command detected: '{query}'")
                    condition()
                elif model and tokenizer and label_encoder and chat_data and pad_sequences:
                    # Skip LLM for non-conversational queries (file paths, system commands, etc.)
                    skip_llm_patterns = [
                        '.exe', '.py', 'c:/', 'c:\\', 'python', '& ', '/', '\\',
                        'appdata', 'programs', 'onedrive', 'desktop', 'users',
                        'thara', 'main.py', 'local/programs'
                    ]
                    query_lower_for_check = query.lower()
                    should_skip_llm = any(pattern in query_lower_for_check for pattern in skip_llm_patterns)
                    
                    # Also skip if query is too short or seems like an error/misinterpretation
                    if len(query.strip()) < 3 or should_skip_llm:
                        print(f"⚠ Skipping LLM for query (looks like system command/path): '{query}'")
                        # Don't speak - just stay silent for unwanted commands
                        pass
                    else:
                        # Use chatbot model for general conversational queries (only if no specific command matched)
                        try:
                            print(f"Processing with LLM: '{query}'")
                            sequences = tokenizer.texts_to_sequences([query])
                            
                            if sequences and len(sequences[0]) > 0:
                                padded_sequences = pad_sequences(sequences, maxlen=20, truncating='post')
                                result = model.predict(padded_sequences, verbose=0)
                                predicted_index = np.argmax(result[0])
                                confidence = result[0][predicted_index]
                                
                                print(f"LLM Confidence: {confidence:.2f}")
                                
                                # Only use chatbot response if confidence is HIGH (reduced unwanted responses)
                                if confidence > 0.6:  # Higher threshold to reduce unwanted responses
                                    tag = label_encoder.inverse_transform([predicted_index])[0]
                                    print(f"LLM Tag: {tag}")
                                    
                                    response_found = False
                                    for i in chat_data['intents']:
                                        if i['tag'] == tag:
                                            response = random.choice(i['responses'])
                                            print(f"✓ LLM Response: {response}")
                                            speak(response)
                                            response_found = True
                                            break
                                    
                                    if not response_found:
                                        print("⚠ No response found for tag")
                                        # Only auto-search for clear informational queries
                                        if "?" in query or any(word in query_lower_for_check for word in ["what is", "what are", "who is", "who are", "where is", "when is", "why is", "how to", "tell me about"]):
                                            print("🔄 Auto-searching for informational query...")
                                            speak("I don't have that information. Let me search Google for you.")
                                            result = search_google(query)
                                            if result == "EXIT_PROGRAM":
                                                sys.exit()
                                            elif result:
                                                print(f"✓ Auto-search completed")
                                        else:
                                            # Don't speak for low confidence or unclear queries
                                            print("⚠ Query not understood, but not speaking to avoid unwanted messages")
                                else:
                                    print(f"⚠ Low confidence ({confidence:.2f}), skipping response to avoid unwanted messages")
                                    # Don't speak for low confidence - just stay silent
                            else:
                                print("⚠ No sequences generated from query")
                                # Query not in vocabulary - only search for clear informational queries, don't speak otherwise
                                if any(word in query_lower_for_check for word in ["what is", "what are", "who is", "who are", "where is", "when is", "why is", "how to", "tell me about"]):
                                    speak("I don't have that in my knowledge base. Let me search Google for you.")
                                    result = search_google(query)
                                    if result == "EXIT_PROGRAM":
                                        sys.exit()
                                else:
                                    # Don't speak for unclear queries - just stay silent
                                    print("⚠ Query not recognized, staying silent to avoid unwanted messages")
                        except Exception as e:
                            print(f"✗ LLM/Chatbot error: {e}")
                            import traceback
                            traceback.print_exc()
                            # Don't speak on errors - just log silently
                            print("⚠ LLM error occurred, staying silent to avoid unwanted messages")
                else:
                    print("⚠ LLM model not loaded")
                    # Only speak if it's a clear informational query
                    if any(word in query_lower for word in ["what is", "what are", "who is", "who are", "where is", "when is", "why is", "how to", "tell me about"]):
                        speak("My LLM model is not available. Let me search Google for that.")
                        result = search_google(query)
                        if result == "EXIT_PROGRAM":
                            sys.exit()
                    else:
                        # Don't speak for unclear queries when model is not loaded
                        print("⚠ LLM model not loaded and query unclear, staying silent")
                 
        except KeyboardInterrupt:
            print("\nGoodbye!")
            speak("Goodbye boss!")
            sys.exit()
        except Exception as e:
            print(f"Error: {e}")
            speak("Sorry boss, there was an error")            
                       

#speak("Hello, I am preethi,your personal assistant")
#print(command())"""
