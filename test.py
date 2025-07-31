import asyncio
import edge_tts
from langcodes import Language
import deepl
from pathlib import Path
from datetime import datetime
import os

VOICES = {
    # English
    "en-US-JennyNeural": {
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

def setup_deepl_translator():
    """Initialize DeepL translator with API key"""
    while True:
        api_key = "873cad37-60a4-4b51-829e-70a7eb7b8ee2:fx"
       
        try:
            translator = deepl.Translator(api_key)
            usage = translator.get_usage()
            remaining = usage.character.limit - usage.character.count
            print(f"DeepL connected (Remaining characters: {remaining})")
            return translator
        except Exception as e:
            print(f"Connection failed: {str(e).split('https')[0]}")

def speech_rate(default_rate: str = "-0%") -> str:
    while True:
        input_rate = input(
            f"Enter speech rate [+/-%] (Default: {default_rate}, press Enter for default): "
        ).strip()
        
        if not input_rate:
            return default_rate
        
        if input_rate.endswith('%') and (input_rate.startswith('+') or input_rate.startswith('-')):
            return input_rate
        
        print("Please input a rate in the form of '+10%' or '-10%': ")

async def translate_with_deepl(text: str, target_lang: str, translator: deepl.Translator) -> str:
    """Translate text using DeepL with proper language mapping"""
    lang_map = {
        'en': 'EN-US',
        'el': 'EL',
        # Add more languages as needed
    }
    
    try:
        result = translator.translate_text(
            text,
            target_lang=lang_map.get(target_lang, target_lang.upper()),
            preserve_formatting=True
        )
        return result.text
    except Exception as e:
        print(f"Translation error: {e}")
        return text

async def generate_speech():
    # Initialize DeepL
    deepl_translator = setup_deepl_translator()

    # Voice selection
    print("\nAvailable Voices:")
    for i, (voice_id, details) in enumerate(VOICES.items(), 1):
        lang_name = Language.get(details['language']).display_name()
        print(f"{i}. {lang_name} | {details['gender']} | {voice_id}")

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

    # Text input
    text = input("\nEnter text to convert to speech: ").strip()

    # Path selection
    while True:
        save_path = input("\nEnter save folder path (or press Enter for default): ").strip()
        if not save_path:
            save_path = Path.home() / "Audio_Outputs"
            break
            
        try:
            save_path = Path(save_path)
            save_path.mkdir(parents=True, exist_ok=True)
            test_file = save_path / "test.tmp"
            test_file.touch()
            test_file.unlink()
            break
        except Exception as e:
            print(f"Invalid path: {e}")

    # Translation
    if voice_details['language'] != 'en':
        print(f"\nTranslating to {Language.get(voice_details['language']).display_name()}...")
        translated = await translate_with_deepl(text, voice_details['language'], deepl_translator)
        print(f"Original: {text}")
        print(f"Translated: {translated}")
    else:
        translated = text

    # Speech generation
    rate = speech_rate()
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"output_{voice_details['language']}_{voice_details['gender']}_{timestamp}.wav"
    output_path = save_path / filename

    communicate = edge_tts.Communicate(text=translated, voice=voice_id, rate=rate)
    print(f"\nGenerating {voice_details['gender'].lower()} voice...")
    await communicate.save(output_path)
    
    print(f"\n✅ Successfully saved to:\n{output_path}")
   

if __name__ == "__main__":
    asyncio.run(generate_speech())
