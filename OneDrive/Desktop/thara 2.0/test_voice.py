"""Quick test script for voice recognition and Google opening"""
import speech_recognition as sr
import webbrowser

print("="*60)
print("Voice Recognition & Google Test")
print("="*60)

# Test 1: Check microphone
print("\n[Test 1] Checking microphone...")
try:
    r = sr.Recognizer()
    mics = sr.Microphone.list_microphone_names()
    print(f"✓ Found {len(mics)} microphone(s)")
    if len(mics) > 0:
        print(f"   Default: {mics[0]}")
except Exception as e:
    print(f"✗ Error: {e}")

# Test 2: Test voice recognition
print("\n[Test 2] Testing voice recognition...")
print("Speak something (will timeout in 5 seconds)...")
try:
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source, duration=0.5)
        print("Listening...", end="", flush=True)
        audio = r.listen(source, timeout=5, phrase_time_limit=10)
        print("\rRecognizing...", end="", flush=True)
        query = r.recognize_google(audio, language='en-in')
        print(f"\r✓ Recognized: '{query}'")
except sr.WaitTimeoutError:
    print("\r✗ Timeout - no speech detected")
except sr.UnknownValueError:
    print("\r✗ Could not understand audio")
except Exception as e:
    print(f"\r✗ Error: {e}")

# Test 3: Test Google opening
print("\n[Test 3] Testing Google opening...")
try:
    webbrowser.open("https://www.google.com/")
    print("✓ Google should have opened in your browser")
except Exception as e:
    print(f"✗ Error: {e}")

print("\n" + "="*60)
print("Tests completed!")
print("="*60)

