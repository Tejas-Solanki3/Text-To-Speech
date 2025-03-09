#!/usr/bin/env python
# coding: utf-8

import streamlit as st
from gtts import gTTS
import os
from deep_translator import GoogleTranslator
from pydub import AudioSegment
from pydub.utils import which

# Ensure ffmpeg is set correctly
AudioSegment.converter = which("ffmpeg")
AudioSegment.ffprobe = which("ffprobe")

# Fix for inotify watch limit (optional, required for some servers)
os.system("echo fs.inotify.max_user_watches=524288 | sudo tee -a /etc/sysctl.conf && sudo sysctl -p")

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

# Function to translate and convert text to speech
def translate_and_convert_to_speech(text, target_language, speed):
    try:
        text = text.strip()
        if not text:
            st.error("❌ Please enter some text or upload a file.")
            return None

        # Translate the text if needed
        if target_language != "en":
            translator = GoogleTranslator(source="auto", target=target_language)
            text = translator.translate(text)
            st.text_area("Translated text:", text, height=100)

        slow = True if speed == "Slow" else False

        # Generate speech using gTTS
        tts = gTTS(text=text, lang=target_language, tld="com", slow=slow)
        tts.save("output.mp3")

        # Convert MP3 to a universal format for better compatibility
        audio = AudioSegment.from_file("output.mp3", format="mp3")
        audio.export("fixed_output.mp3", format="mp3")

        return "fixed_output.mp3"
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

# Speed Options
speed_option = st.selectbox("⚡ Select Speed:", ["Normal", "Slow"])

# Convert Button
if st.button("🔊 Translate and Play"):
    with st.spinner("Translating and converting to speech..."):
        output_file = translate_and_convert_to_speech(text, language_code, speed_option)

        if output_file and os.path.exists(output_file):
            st.success("✅ Conversion successful! You can play or download the speech below.")

            # Play audio using Streamlit's native player
            with open(output_file, "rb") as audio_file:
                audio_bytes = audio_file.read()
                st.audio(audio_bytes, format="audio/mpeg")

            # Download Button
            with open(output_file, "rb") as f:
                st.download_button("⬇️ Download Speech", f, file_name="speech.mp3", mime="audio/mpeg")

            # Delay before cleanup to avoid premature deletion
            import time
            time.sleep(2)
            os.remove(output_file)
        else:
            st.error("❌ Failed to generate audio. Please try again.")
