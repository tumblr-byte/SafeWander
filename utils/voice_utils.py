"""Voice input and output utilities for SafeWonder."""
import streamlit as st
from gtts import gTTS
import io
import tempfile
import os


def text_to_speech(text: str, language: str = 'en') -> bytes:
    """
    Convert text to speech audio.
    
    Args:
        text: Text to convert to speech
        language: Language code (e.g., 'en', 'es', 'hi', 'ja')
        
    Returns:
        Audio bytes in MP3 format
    """
    try:
        # Map language names to gTTS codes
        lang_map = {
            'English': 'en',
            'Spanish': 'es',
            'French': 'fr',
            'German': 'de',
            'Italian': 'it',
            'Portuguese': 'pt',
            'Hindi': 'hi',
            'Japanese': 'ja',
            'Korean': 'ko',
            'Chinese': 'zh',
            'Arabic': 'ar',
            'Russian': 'ru',
            'Bengali': 'bn',
            'Thai': 'th'
        }
        
        # Get language code
        lang_code = lang_map.get(language, language.lower()[:2])
        
        # Create TTS object
        tts = gTTS(text=text, lang=lang_code, slow=False)
        
        # Save to bytes
        audio_bytes = io.BytesIO()
        tts.write_to_fp(audio_bytes)
        audio_bytes.seek(0)
        
        return audio_bytes.read()
        
    except Exception as e:
        st.error(f"<i class='fas fa-exclamation-triangle'></i> Audio generation error: {str(e)}", unsafe_allow_html=True)
        return None


def get_language_code_for_tts(language_name: str) -> str:
    """
    Get gTTS language code from language name.
    
    Args:
        language_name: Full language name
        
    Returns:
        Two-letter language code
    """
    lang_map = {
        'English': 'en',
        'Spanish': 'es',
        'French': 'fr',
        'German': 'de',
        'Italian': 'it',
        'Portuguese': 'pt',
        'Hindi': 'hi',
        'Japanese': 'ja',
        'Korean': 'ko',
        'Chinese': 'zh',
        'Arabic': 'ar',
        'Russian': 'ru',
        'Bengali': 'bn',
        'Thai': 'th',
        'Vietnamese': 'vi',
        'Turkish': 'tr',
        'Polish': 'pl',
        'Dutch': 'nl',
        'Swedish': 'sv',
        'Indonesian': 'id',
        'Filipino': 'tl',
        'Malay': 'ms'
    }
    
    return lang_map.get(language_name, 'en')
