import pyttsx3

# Initialize the TTS engine
engine = pyttsx3.init()

# Get the list of available voices
voices = engine.getProperty('voices')

# Print each voice's details
for voice in voices:
    gender = getattr(voice, 'gender', '').lower()
    if gender == "male":
        print(f"Voice ID: {voice.id}")
        print(f"Name: {voice.name}")
        print(f"Languages: {voice.languages}")
        print(f"Gender: {gender}")
        print(f"Age: {getattr(voice, 'age', 'unknown')}")
        print("---------")

 # print(f"Voice ID: {voice.id}")
 # print(f"Name: {voice.name}")
 # print(f"Languages: {voice.languages}")
 # print(f"Gender: {voice.gender}")
 # print(f"Age: {voice.age}")
 # print("---------")