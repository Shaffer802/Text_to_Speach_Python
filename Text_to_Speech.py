
'''

The program to be run needs to have the edge-tts, edge-tts langcodes
It also needs to have deep-translator downloaded 
This is because the program depends on the packages to be downloaded as
most of the commands are coming from those libraries

I am also running it in a venv with python 3.13.5

'''
import datetime
import asyncio
import edge_tts
from langcodes import Language
from deep_translator import GoogleTranslator
from pathlib import Path
import re 

# Choice of the library of the voices available (can add other ones also)
VOICES = {
    # English
    "en-US-EmmaNeural": {
        "language": "en",
        "gender": "Female",
        "locale": "en-US"
    },
    "en-US-ChristopherNeural": {
        "language": "en",
        "gender": "Male",
        "locale": "en-US"
    },
    # Greek
    "el-GR-AthinaNeural": {
        "language": "el",
        "gender": "Female",
        "locale": "el-GR"
    },
    "el-GR-NestorasNeural": {
        "language": "el",
        "gender": "Male",
        "locale": "el-GR"
    },
}

#This function will prompt the user to change the rate of the audio that is generated
def speech_rate(default_rate: str = "-20%") -> str:
    while True:
        input_rate = input(
            f"Enter speech rate [+/-%] (Default: {default_rate}, press Enter for default): "
        ).strip()
        
        if not input_rate:
            return default_rate
        
        if input_rate.endswith('%') and (input_rate.startswith('+') or input_rate.startswith('-')):
            return input_rate
        
        print("Please input a rate in the form of '+10%' or '-10%': ")

#This function is used when you enter [[ ]] around a word to be excluded from the translation
def translate_with_skip(text: str, target_lang: str) -> str:

    # Split text into translatable and non-translatable parts
    parts = re.split(r'(\[\[.*?\]\])', text)
    translated_parts = []
    
    for part in parts:
        if part.startswith('[[') and part.endswith(']]'):
            #This command will exclude the brackets and only take the inside of the brackets and append it
            translated_parts.append(part[2:-2])
        else:
            #This will translate the whole text without excluding anything
            if part.strip():
                try:
                    translated = GoogleTranslator(source='auto', target=target_lang).translate(part)
                    translated_parts.append(translated)
                except Exception as e:
                    print(f"Translation failed for: '{part}'. Error: {e}")
                    translated_parts.append(part)

    #the return will get the two lists which have the texts inside them and will join them together
    return ' '.join(translated_parts)
# function to display the available voices and the selection from the user for what language he wants (and also male or female)
async def generate_speech():
    
    # Displays the information for the user about the available languages: male or female and the respective language
    print("Available Voices:")
    for i, (voice_id, details) in enumerate(VOICES.items(), 1):
        lang_name = Language.get(details['language']).display_name()
        print(f"{i}. {lang_name} ({details['language']}) | "
              f"Gender: {details['gender']} | "
              f"Voice: {voice_id}")

    # Loop to control the user input for language selection (1-4 for now maybe more if more languages are added)
    while True:
        try:
            choice = int(input("\nSelect voice by number: "))
            if 1 <= choice <= len(VOICES):
                voice_id = list(VOICES.keys())[choice-1]
                voice_details = VOICES[voice_id]
                break
            print(f"Please enter 1-{len(VOICES)}")
        except ValueError:
            print("Invalid input. Enter a number.")

     # The user will input the text he or she wants to input to make it into speech and how to exclude text from translation
    print("\nEnter text to convert to speech.")
    print("Wrap text in [[double brackets]] to skip translation (e.g., Hello [[world]]).")
    text = input("> ").strip()
    
    # Get speech rate
    rate = speech_rate()

#...........................................................................................
# New export feature for exporting both Greek and English audio files based on the selected
# Written by Shaffer Patchias
#...........................................................................................

    # Ask if user wants both Greek and English audio files for the selected voice gender
    export_both = input("\nExport both Greek and English audio files for this gender? (y/n): ").strip().lower() == 'y'

    downloads_path = Path.home() / 'Downloads'

    async def save_audio(text, voice_id, voice_details):
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        communicate = edge_tts.Communicate(text=text, voice=voice_id, rate=rate)
        output_file = downloads_path / f"output_{voice_details['language']}__{voice_details['gender']}__{timestamp}.wav"
        print(f"\nGenerating {voice_details['gender'].lower()} speech in "
              f"{Language.get(voice_details['language']).display_name()}...")
        await communicate.save(output_file)
        print(f"Audio saved to: {output_file}")

    if export_both:
        # Find English and Greek voices of the selected gender
        english_voice = next((v for v, d in VOICES.items() if d['language'] == 'en' and d['gender'] == voice_details['gender']), None)
        greek_voice = next((v for v, d in VOICES.items() if d['language'] == 'el' and d['gender'] == voice_details['gender']), None)

        if english_voice:
            print(f"\nGenerating English audio...")
            await save_audio(text, english_voice, VOICES[english_voice])
        else:
            print("No English voice available for this gender.")
        
        if greek_voice:
            print("\nPreparintg Greek audio (translating text, skipping [[bracketed]] parts)...")
            translated = translate_with_skip(text, 'el')
            print(f"Original: {text}")
            print(f"Translated: {translated}")
            await save_audio(translated, greek_voice, VOICES[greek_voice])
        else:
            print("No Greek voice found for this gender.")
    
    else:
        if voice_details['language'] == 'en':
            lang_name = Language.get(voice_details['language']).display_name()
            print(f"\nTranslating to {lang_name} (skipping [[bracketed]] parts)...")
            translated = translate_with_skip(text, voice_details['language'])
            print(f"Original: {text}")
            print(f"Translated: {translated}")
            text_to_speak = translated
        else:
            text_to_speak = text
        await save_audio(text_to_speak, voice_id, voice_details)
if __name__ == "__main__":
    # asyncio needed because edge-tts runs asynchronously and needs to be run inside an asyncio loop
    asyncio.run(generate_speech())

'''
Older file export function
Written by Andreas Karpasitis
'''
#     if voice_details['language'] != 'en':
#         lang_name = Language.get(voice_details['language']).display_name()
#         print(f"\nTranslating to {lang_name} (skipping [[bracketed]] parts)...")

#         # Function i found that will help to translate the given text to another language taken from the list
#         # User will choose the language he wants the audio to be in and after providing the text the respected text
#         # will be translated to the chosen language
#         translated = translate_with_skip(text, voice_details['language'])

#         # Printing the translated text and the original one
#         print(f"Original: {text}")
#         print(f"Translated: {translated}")
#         text_to_speak = translated
#     else:
#         text_to_speak = text

#     # this will put the audio file into the downloads folder of the user
#     communicate = edge_tts.Communicate(text=text_to_speak, voice=voice_id, rate=rate)
#     downloads_path = Path.home() / 'Downloads'
#     output_file = downloads_path / f"output_{voice_details['language']}_{voice_details['gender']}.wav"
#      #confirmation of the file and the name of the file to be generated
#     print(f"\nGenerating {voice_details['gender'].lower()} speech in "
#           f"{Language.get(voice_details['language']).display_name()}...")
#     await communicate.save(output_file)
#     print(f"Audio saved to: {output_file}")

# if __name__ == "__main__":
#     #asynchio needed because the edge-tts is run asynchronously and need to be run inside a asyncio loop to run without errors
#     asyncio.run(generate_speech())