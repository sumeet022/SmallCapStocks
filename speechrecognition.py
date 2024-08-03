import speech_recognition as sr

# Initialize recognizer
recognizer = sr.Recognizer()

# Capture audio from the microphone
with sr.Microphone() as source:
    print("Speak something...")
    recognizer.adjust_for_ambient_noise(source)  # Adjust for ambient noise
    audio = recognizer.listen(source, timeout=5)  # Listen for up to 5 seconds

# Recognize speech using Google Web Speech API
try:
    print("Recognizing...")
    recognized_text = recognizer.recognize_google(audio)
    print(f"Recognized text: {recognized_text}")
except sr.UnknownValueError:
    print("Sorry, could not understand audio.")
except sr.RequestError as e:
    print(f"Error occurred during request to Google Web Speech API: {e}")
    
