#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from gtts import gTTS
import os
from deep_translator import GoogleTranslator

# Supported languages for translation and TTS
LANGUAGES = {
    "English": "en",
    "Hindi (हिन्दी)": "hi",
    "Spanish (Español)": "es",
    "French (Français)": "fr",
    "German (Deutsch)": "de",
    "Italian (Italiano)": "it",
    "Chinese (中文)": "zh-CN",
    "Japanese (日本語)": "ja",
    "Russian (Русский)": "ru",
    "Arabic (العربية)": "ar",
    "Portuguese (Português)": "pt",
    "Korean (한국어)": "ko",
    "Bengali (বাংলা)": "bn",
    "Urdu (اردو)": "ur",
}

# Voice options for different languages
VOICE_OPTIONS = {
    "en": {
        "Female": "com",      # US English
        "Male": "co.uk",      # British English
        "Neutral": "co.in"    # Indian English
    },
    "hi": {
        "Female": "co.in",    # Indian Hindi
        "Male": "in"         # Alternative Indian voice
    }
}

# Function to translate and convert text to speech
def translate_and_convert_to_speech(text, target_language, voice_option, speed):
    try:
        if not text.strip():
            st.error("❌ Please enter some text or upload a file.")
            return None

        # First translate the text if not English
        if target_language != "en":
            translator = GoogleTranslator(source='auto', target=target_language)
            text = translator.translate(text)
            # Show translated text
            st.text_area("Translated text:", text, height=100)

        slow = True if speed == "Slow" else False

        # Set TLD based on language and voice option
        tld = "com"  # default
        if target_language in VOICE_OPTIONS and voice_option in VOICE_OPTIONS[target_language]:
            tld = VOICE_OPTIONS[target_language][voice_option]

        # Generate speech from translated text
        tts = gTTS(text=text, lang=target_language, tld=tld, slow=slow)
        
        output_file = "output.mp3"
        tts.save(output_file)
        
        return output_file
    except Exception as e:
        st.error(f"❌ Error during conversion: {str(e)}")
        return None

# Streamlit App
st.title("🎤 Multi-Language Text-to-Speech Converter")

# Input Section
text = st.text_area("Enter your text below:")
uploaded_file = st.file_uploader("Or upload a text file (.txt)", type=["txt"])

if uploaded_file:
    text = uploaded_file.read().decode("utf-8")
    st.text_area("File content:", text, height=150)

# Language Selection
language_option = st.selectbox("🌐 Select Target Language:", list(LANGUAGES.keys()))
language_code = LANGUAGES[language_option]

# Voice Options based on selected language
available_voices = list(VOICE_OPTIONS.get(language_code, {"Female": "com"}).keys())
voice_option = st.selectbox("🔊 Select Voice:", available_voices)

# Speed Options
speed_option = st.selectbox("⚡ Select Speed:", ["Normal", "Slow"])

# Convert Button
if st.button("🔊 Translate and Play"):
    with st.spinner("Translating and converting to speech..."):
        output_file = translate_and_convert_to_speech(text, language_code, voice_option, speed_option)

        if output_file and os.path.exists(output_file):
            st.success("✅ Conversion successful! You can play or download the speech below.")
            
            # Play audio using Streamlit's native audio player
            with open(output_file, "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mp3")

            # Download Button
            with open(output_file, "rb") as f:
                st.download_button("⬇️ Download Speech", f, file_name="speech.mp3", mime="audio/mp3")

            # Cleanup
            os.remove(output_file)
        else:
            st.error("❌ Failed to generate audio. Please try again.")
