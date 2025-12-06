"""OCR translator for SafeWonder - extract and translate text from images."""
import json
import streamlit as st
from dataclasses import dataclass
from typing import Optional, Tuple
from PIL import Image, ImageEnhance
import pytesseract
from langdetect import detect, LangDetectException
from utils.groq_client import GroqClient


@dataclass
class OCRResult:
    """OCR result data structure."""
    extracted_text: str
    detected_language: str
    translated_text: str
    warning_level: str
    explanation: str
    suspicious_elements: list


def preprocess_image(image: Image.Image) -> Image.Image:
    """
    Preprocess image for better OCR results.
    
    Args:
        image: PIL Image object
        
    Returns:
        Preprocessed PIL Image
    """
    # Convert to grayscale for better OCR
    image = image.convert('L')
    
    # Resize if too small (min 1000px on longest side for better accuracy)
    min_size = 1000
    if max(image.size) < min_size:
        ratio = min_size / max(image.size)
        new_size = tuple(int(dim * ratio) for dim in image.size)
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    # Resize if too large (max 3000px on longest side)
    max_size = 3000
    if max(image.size) > max_size:
        ratio = max_size / max(image.size)
        new_size = tuple(int(dim * ratio) for dim in image.size)
        image = image.resize(new_size, Image.Resampling.LANCZOS)
    
    # Enhance contrast significantly for better text detection
    enhancer = ImageEnhance.Contrast(image)
    image = enhancer.enhance(2.0)
    
    # Enhance sharpness
    enhancer = ImageEnhance.Sharpness(image)
    image = enhancer.enhance(2.0)
    
    # Enhance brightness
    enhancer = ImageEnhance.Brightness(image)
    image = enhancer.enhance(1.2)
    
    return image


def extract_text_from_image(image: Image.Image) -> Tuple[str, str]:
    """
    Extract text from image using Tesseract OCR.
    
    Args:
        image: PIL Image object
        
    Returns:
        Tuple of (extracted_text, detected_language)
    """
    try:
        # Preprocess image
        processed_image = preprocess_image(image)
        
        # Try multiple language combinations for better accuracy
        # Include common languages: English, Hindi, Spanish, French, German, Japanese, Chinese, Arabic
        lang_configs = [
            'eng+hin+spa+fra+deu',  # English + Hindi + Spanish + French + German
            'eng+jpn+chi_sim+ara',   # English + Japanese + Chinese + Arabic
            'eng',                    # English only as fallback
        ]
        
        best_text = ""
        best_confidence = 0
        
        for lang_config in lang_configs:
            try:
                # Extract text with specific language configuration
                custom_config = f'--oem 3 --psm 6 -l {lang_config}'
                text = pytesseract.image_to_string(processed_image, config=custom_config)
                text = text.strip()
                
                # Use the result with most text extracted
                if len(text) > len(best_text):
                    best_text = text
                    
            except Exception:
                continue
        
        text = best_text
        
        if not text or len(text) < 2:
            return "", "unknown"
        
        # Detect language
        try:
            lang_code = detect(text)
            language = get_language_name(lang_code)
        except LangDetectException:
            language = "unknown"
        
        return text, language
        
    except Exception as e:
        st.error(f"<i class='fas fa-exclamation-triangle'></i> OCR Error: {str(e)}", unsafe_allow_html=True)
        return "", "unknown"


def get_language_name(lang_code: str) -> str:
    """
    Convert language code to language name.
    
    Args:
        lang_code: ISO language code
        
    Returns:
        Language name
    """
    language_map = {
        'en': 'English',
        'es': 'Spanish',
        'fr': 'French',
        'de': 'German',
        'it': 'Italian',
        'pt': 'Portuguese',
        'hi': 'Hindi',
        'ja': 'Japanese',
        'ko': 'Korean',
        'zh-cn': 'Chinese',
        'zh-tw': 'Chinese',
        'ar': 'Arabic',
        'ru': 'Russian',
        'bn': 'Bengali',
        'pa': 'Punjabi',
        'te': 'Telugu',
        'mr': 'Marathi',
        'ta': 'Tamil',
        'ur': 'Urdu',
        'gu': 'Gujarati'
    }
    return language_map.get(lang_code, lang_code.upper())


def build_ocr_analysis_prompt(text: str, source_lang: str, target_lang: str) -> str:
    """
    Build prompt for OCR text analysis and translation.
    
    Args:
        text: Extracted text from image
        source_lang: Detected source language
        target_lang: Target language for translation
        
    Returns:
        Formatted prompt string
    """
    prompt = f"""You are analyzing text extracted from an image for a traveler.

EXTRACTED TEXT: {text}
DETECTED LANGUAGE: {source_lang}
TRANSLATE TO: {target_lang}

TASK:
1. Translate the text accurately and naturally
2. Analyze if this text contains:
   - Scam indicators (unusual charges, fake fees, suspicious requests)
   - Overpricing or hidden charges
   - Misleading information
   - Important warnings or alerts
   - Official notices
3. Explain what the text means in context
4. Assess warning level

OUTPUT FORMAT (respond ONLY with valid JSON):
{{
  "translated_text": "<accurate translation>",
  "warning_level": "<none|low|medium|high>",
  "explanation": "<what this text means and its context>",
  "suspicious_elements": ["<list any suspicious items found, or empty array if none>"]
}}

Warning levels:
- none: Normal text, no concerns
- low: Minor attention needed
- medium: Caution advised, verify information
- high: Potential scam or danger, avoid"""
    
    return prompt


def translate_and_analyze(
    text: str,
    source_lang: str,
    target_lang: str,
    groq_client: GroqClient
) -> Optional[OCRResult]:
    """
    Translate extracted text and analyze for suspicious content.
    
    Args:
        text: Extracted text from OCR
        source_lang: Detected source language
        target_lang: Target language for translation
        groq_client: Groq API client
        
    Returns:
        OCRResult object or None if failed
    """
    if not text or len(text.strip()) < 3:
        st.warning("⚠️ No text detected in image. Please try a clearer photo.")
        return None
    
    # Build prompt
    prompt = build_ocr_analysis_prompt(text, source_lang, target_lang)
    
    # Call Groq API
    with st.spinner("🔍 Analyzing and translating text..."):
        response_text = groq_client.call_api(prompt, temperature=0.3)
    
    if not response_text:
        st.error("❌ Analysis failed. Please try again.")
        return None
    
    # Parse response
    try:
        # Extract JSON from response
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        analysis_data = json.loads(response_text)
        
        # Create result object
        result = OCRResult(
            extracted_text=text,
            detected_language=source_lang,
            translated_text=analysis_data.get('translated_text', text),
            warning_level=analysis_data.get('warning_level', 'none'),
            explanation=analysis_data.get('explanation', 'Text translated successfully'),
            suspicious_elements=analysis_data.get('suspicious_elements', [])
        )
        
        return result
        
    except json.JSONDecodeError as e:
        st.error(f"❌ Failed to parse analysis: {str(e)}")
        st.code(response_text)
        return None
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        return None
