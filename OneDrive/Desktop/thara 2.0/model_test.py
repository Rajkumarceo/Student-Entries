import json
import pickle
import numpy as np
import random
import pyttsx3
from tensorflow import keras

# Handle different TensorFlow versions for pad_sequences import
try:
    # Try the standard import path (works for TensorFlow < 2.10)
    from tensorflow.keras.preprocessing.sequence import pad_sequences  # type: ignore
except ImportError:
    try:
        # Fallback for newer TensorFlow versions (2.10+)
        from tensorflow.keras.utils import pad_sequences  # type: ignore
    except ImportError:
        # Alternative fallback for standalone keras
        from keras.preprocessing.sequence import pad_sequences  # type: ignore

def initialize_engine():
    engine = pyttsx3.init("sapi5")
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)
    rate = engine.getProperty('rate')
    engine.setProperty('rate', 150)
    volume = engine.getProperty('volume')
    engine.setProperty('volume', volume + 0.25)
    return engine

def speak(text):
    engine = initialize_engine()
    engine.say(text)
    engine.runAndWait()

with open("intents.json") as file:
    data = json.load(file)

model = keras.models.load_model("chat_model.h5")

with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)

with open("label_encoder.pkl", "rb") as encoder_file:
    label_encoder = pickle.load(encoder_file)

while True:
    try:
        input_text = input("Enter your command-> ")
        if input_text.lower() in ['quit', 'exit', 'bye']:
            print("Goodbye!")
            break
        
        padded_sequences = pad_sequences(tokenizer.texts_to_sequences([input_text]), maxlen=20, truncating='post')
        result = model.predict(padded_sequences, verbose=0)
        tag = label_encoder.inverse_transform([np.argmax(result)])[0]

        response_found = False
        for i in data['intents']:
            if i['tag'] == tag:
                speak(random.choice(i['responses']))
                response_found = True
                break
        
        if not response_found:
            print("Sorry boss, can't understand you")
    except KeyboardInterrupt:
        speak("\nGoodbye!")
        break
    except Exception as e:
        print(f"Error: {e}")