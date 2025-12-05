"""Polite culture translator for SafeWonder."""
import json
import streamlit as st
from dataclasses import dataclass
from typing import Dict, Any, Optional
from gtts import gTTS
import io
from utils.groq_client import GroqClient
from utils.database_loader import get_cultural_info, get_local_phrases


@dataclass
class TranslationResult:
    """Translation result data structure."""
    original_text: str
    translated_text: str
    source_language: str
    target_language: str
    pronunciation: str
    tone_guidance: str
    cultural_notes: str
    audio_data: Optional[bytes]


def get_language_code(language: str) -> str:
    """
    Convert language name to language code for TTS.
    
    Args:
        language: Language name
        
    Returns:
        Language code (e.g., 'en', 'es', 'hi')
    """
    language_map = {
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
        'Russian': 'ru'
    }
    return language_map.get(language, 'en')


def get_target_language_from_country(country_name: str) -> str:
    """
    Get primary language for a country.
    
    Args:
        country_name: Name of the country
        
    Returns:
        Primary language name
    """
    country_language_map = {
        'India': 'Hindi',
        'Japan': 'Japanese',
        'United States': 'English',
        'Spain': 'Spanish',
        'France': 'French',
        'Germany': 'German',
        'Italy': 'Italian',
        'Portugal': 'Portuguese',
        'Korea': 'Korean',
        'China': 'Chinese',
        'Saudi Arabia': 'Arabic',
        'Russia': 'Russian'
    }
    return country_language_map.get(country_name, 'English')


def text_to_speech(text: str, language: str) -> Optional[bytes]:
    """
    Generate audio from text using gTTS.
    
    Args:
        text: Text to convert to speech
        language: Language name
        
    Returns:
        Audio data as bytes or None if failed
    """
    try:
        lang_code = get_language_code(language)
        tts = gTTS(text=text, lang=lang_code, slow=False)
        
        # Save to bytes buffer
        audio_buffer = io.BytesIO()
        tts.write_to_fp(audio_buffer)
        audio_buffer.seek(0)
        
        return audio_buffer.read()
    except Exception as e:
        st.warning(f"⚠️ Could not generate audio: {str(e)}")
        return None


def build_translation_prompt(phrase: str, source_lang: str, target_lang: str, cultural_info: Dict[str, Any]) -> str:
    """
    Build prompt for culturally-appropriate translation.
    
    Args:
        phrase: Phrase to translate
        source_lang: Source language
        target_lang: Target language
        cultural_info: Cultural context from database
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""You are a cultural translation expert. Translate the following phrase with cultural appropriateness:

PHRASE: {phrase}
FROM: {source_lang}
TO: {target_lang}

CULTURAL CONTEXT:
Greetings: {cultural_info.get('greetings', 'Standard greetings')}
Dos: {', '.join(cultural_info.get('dos', []))}
Don'ts: {', '.join(cultural_info.get('donts', []))}

REQUIREMENTS:
1. Translate accurately and naturally
2. Make it culturally polite and appropriate
3. Provide pronunciation guide (phonetic, easy to read)
4. Explain tone, body language, and etiquette
5. Note any cultural sensitivities

OUTPUT FORMAT (respond ONLY with valid JSON):
{{
  "translated_text": "<natural, polite translation>",
  "pronunciation": "<phonetic guide that's easy to read>",
  "tone_guidance": "<how to say it: tone, body language, context>",
  "cultural_notes": "<important cultural context and tips>"
}}"""
    
    return prompt


def translate_phrase(
    phrase: str,
    source_lang: str,
    target_lang: str,
    country_data: Dict[str, Any],
    groq_client: GroqClient
) -> Optional[TranslationResult]:
    """
    Translate phrase with cultural context.
    
    Args:
        phrase: Phrase to translate
        source_lang: Source language
        target_lang: Target language
        country_data: Country-specific data
        groq_client: Groq API client
        
    Returns:
        TranslationResult object or None if failed
    """
    if not phrase or len(phrase.strip()) < 2:
        st.warning("⚠️ Please enter a phrase to translate.")
        return None
    
    # Get cultural context
    cultural_info = get_cultural_info(country_data)
    
    # Build prompt
    prompt = build_translation_prompt(phrase, source_lang, target_lang, cultural_info)
    
    # Call Groq API
    with st.spinner("🌍 Translating with cultural context..."):
        response_text = groq_client.call_api(prompt, temperature=0.3)
    
    if not response_text:
        st.error("❌ Translation failed. Please try again.")
        return None
    
    # Parse response
    try:
        # Extract JSON from response
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        translation_data = json.loads(response_text)
        
        # Generate audio
        translated_text = translation_data.get('translated_text', '')
        audio_data = text_to_speech(translated_text, target_lang)
        
        # Create result object
        result = TranslationResult(
            original_text=phrase,
            translated_text=translated_text,
            source_language=source_lang,
            target_language=target_lang,
            pronunciation=translation_data.get('pronunciation', 'Pronunciation not available'),
            tone_guidance=translation_data.get('tone_guidance', 'Speak clearly and politely'),
            cultural_notes=translation_data.get('cultural_notes', 'No specific cultural notes'),
            audio_data=audio_data
        )
        
        return result
        
    except json.JSONDecodeError as e:
        st.error(f"❌ Failed to parse translation: {str(e)}")
        st.code(response_text)
        return None
    except Exception as e:
        st.error(f"❌ Error during translation: {str(e)}")
        return None


def get_common_phrases_list(country_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Retrieve pre-defined common phrases from database.
    
    Args:
        country_data: Country-specific data
        
    Returns:
        Dictionary of common phrases
    """
    return get_local_phrases(country_data)
