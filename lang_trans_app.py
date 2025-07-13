# voice_translator_app.py

import streamlit as st
import speech_recognition as sr
from googletrans import Translator
from gtts import gTTS
import tempfile
import os
from pydub import AudioSegment

# ✅ Set path to ffmpeg manually
AudioSegment.converter = r"C:\\ffmpeg\\ffmpeg.exe"

# ========== Streamlit Setup ==========
st.set_page_config(page_title="🌍 Real-Time Voice Translator", layout="centered", page_icon="🗣️")

# ========== Custom CSS ==========
st.markdown("""
    <style>
    .stApp {
        background: url("https://i.gifer.com/VgR.gif");
        background-size: cover;
        background-attachment: fixed;
        background-position: center;
        background-repeat: no-repeat;
        font-family: 'Segoe UI', sans-serif;
        color: #ffffff;
        padding: 2rem;
    }
    .big-title {
        font-size: 3rem;
        font-weight: 700;
        text-align: center;
        margin-bottom: 2rem;
        color: #ffffff;
        text-shadow: 2px 2px 10px rgba(0,0,0,0.6);
    }
    .lang-box, .result-box {
        background: rgba(255, 255, 255, 0.15);
        border: 1px solid rgba(255, 255, 255, 0.25);
        backdrop-filter: blur(16px);
        border-radius: 16px;
        padding: 1.2rem;
        box-shadow: 0 4px 30px rgba(0, 0, 0, 0.2);
        color: #ffffff;
        font-size: 18px;
    }
    .result-box {
        margin-top: 2rem;
        font-weight: 500;
    }
    .stSelectbox > div > div {
        color: #ffffff !important;
        background-color: rgba(0, 0, 0, 0.4) !important;
        padding: 0.5rem;
        border-radius: 8px;
    }

    /* === Characters with Speech Bubbles and Talking Animation === */
    .character-left, .character-right {
        position: fixed;
        bottom: 30px;
        z-index: 9999;
        text-align: center;
    }
    .character-left {
        left: 30px;
        animation: talk-left 3s infinite ease-in-out;
    }
    .character-right {
        right: 30px;
        animation: talk-right 3s infinite ease-in-out;
    }

    @keyframes talk-left {
        0%, 60%, 100%   { transform: scale(1); }
        20%, 40%        { transform: scale(1.08); }
    }
    @keyframes talk-right {
        0%, 20%, 40%    { transform: scale(1); }
        60%, 80%        { transform: scale(1.08); }
        100%            { transform: scale(1); }
    }

    .speech-bubble {
        position: relative;
        background: rgba(255, 255, 255, 0.9);
        color: black;
        font-size: 14px;
        padding: 10px 15px;
        border-radius: 10px;
        display: inline-block;
        max-width: 140px;
        margin-bottom: 8px;
    }
    .speech-bubble::after {
        content: '';
        position: absolute;
        bottom: -10px;
        width: 0;
        height: 0;
        border: 10px solid transparent;
    }
    .left .speech-bubble::after {
        left: 20px;
        border-top-color: rgba(255, 255, 255, 0.9);
        border-bottom: 0;
        margin-left: -10px;
        bottom: -10px;
    }
    .right .speech-bubble::after {
        right: 20px;
        border-top-color: rgba(255, 255, 255, 0.9);
        border-bottom: 0;
        margin-right: -10px;
        bottom: -10px;
    }
    </style>

    <!-- 👥 Left Speaker -->
    <div class="character-left left">
        <div class="speech-bubble">Hi, how are you?</div>
        <img src="https://cdn-icons-png.flaticon.com/512/2922/2922522.png" width="100" alt="Speaker">
    </div>

    <!-- 👤 Right Listener -->
    <div class="character-right right">
        <div class="speech-bubble">¡Estoy bien! ¿Y tú?</div>
        <img src="https://cdn-icons-png.flaticon.com/512/2922/2922510.png" width="100" alt="Listener">
    </div>
""", unsafe_allow_html=True)

# ========== Title ==========
st.markdown("<div class='big-title'>🗣️ Real-Time Voice Translator</div>", unsafe_allow_html=True)

# ========== Language Select ==========
st.markdown("<div class='lang-box'><strong>🌐 Select Target Language:</strong></div>", unsafe_allow_html=True)
LANGUAGES = {
    'English': 'en',
    'Hindi': 'hi',
    'Japanese': 'ja',
    'French': 'fr',
    'German': 'de',
    'Spanish': 'es',
    'Chinese': 'zh-cn',
    'Arabic': 'ar',
    'Russian': 'ru',
    'Korean': 'ko',
    'Marathi': 'mr',
}
target_lang_display = st.selectbox("", list(LANGUAGES.keys()))
target_lang_code = LANGUAGES[target_lang_display]

# ========== Mic Input ==========
st.markdown("<br><strong>🎙️ Click below and speak in any language:</strong>", unsafe_allow_html=True)

user_input = None
if st.button("🎧 Start Listening", type="primary"):
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        st.info("🎤 Listening... Please speak now.")
        try:
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=10, phrase_time_limit=10)
            user_input = recognizer.recognize_google(audio)
            st.success(f"🔈 Recognized Speech: `{user_input}`")
        except sr.WaitTimeoutError:
            st.error("⏰ Timeout: No speech detected.")
        except sr.UnknownValueError:
            st.error("❌ Could not understand audio.")
        except sr.RequestError:
            st.error("❌ Google Speech Recognition failed.")

# ========== Translate & Speak ==========
if user_input:
    translator = Translator()
    try:
        translated = translator.translate(user_input, src='auto', dest=target_lang_code)
        translated_text = translated.text
        st.markdown(
            f"<div class='result-box'>🌍 <strong>Translated to {target_lang_display}:</strong><br><br>{translated_text}</div>",
            unsafe_allow_html=True
        )

        tts = gTTS(text=translated_text, lang=target_lang_code)
        with tempfile.NamedTemporaryFile(delete=False, suffix=".mp3") as tmpfile:
            tts.save(tmpfile.name)
            st.audio(tmpfile.name, format="audio/mp3")

    except Exception as e:
        st.error(f"❌ Translation failed: {e}")
