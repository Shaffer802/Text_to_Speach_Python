import pyttsx3
from pathlib import Path

# Initialize the text-to-speech engine
engine = pyttsx3.init()

# Set speech rate (optional)
engine.setProperty('rate', 150)

# Select a male voice if available
voices = engine.getProperty('voices')

for voice in voices:
    if 'female' in voice.gender:
        engine.setProperty('voice', voice.id)
        break

# Set output to a WAV file in Downloads
downloads_path = Path.home() / 'Downloads'
output_wav = downloads_path / 'voice-output.wav'

# Save speech to WAV file
engine.save_to_file("Thank you for calling. However, we are closed for the day. Please leave a message after the tone.", str(output_wav))
engine.runAndWait()

print(f"Audio generated and saved to: {output_wav}")