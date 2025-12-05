"""UI components for Polite Culture Translator."""
import streamlit as st
from components.culture_translator import (
    translate_phrase,
    get_common_phrases_list,
    get_target_language_from_country
)
from utils.session_manager import get_user_profile, get_country_data, cache_translation, get_cached_translation
from utils.groq_client import get_groq_client


def show_culture_translator():
    """Display the polite culture translator interface."""
    
    st.title("🗣️ Polite Culture Translator")
    st.markdown("Translate phrases with cultural appropriateness and pronunciation guidance.")
    
    # Get user data
    user_profile = get_user_profile()
    country_data = get_country_data()
    
    if not user_profile or not country_data:
        st.error("❌ Profile not found. Please complete onboarding first.")
        return
    
    # Get Groq client
    groq_client = get_groq_client()
    if not groq_client:
        return
    
    # Custom CSS
    st.markdown("""
        <style>
        .translation-card {
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 16px;
            margin: 1rem 0;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }
        .language-badge {
            display: inline-block;
            background: linear-gradient(135deg, #6366F1 0%, #EC4899 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            margin: 0.5rem 0;
        }
        .pronunciation-box {
            background: rgba(99, 102, 241, 0.1);
            border-left: 4px solid #6366F1;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
            font-family: 'Courier New', monospace;
            font-size: 1.1rem;
        }
        .cultural-tip {
            background: rgba(236, 72, 153, 0.1);
            border-left: 4px solid #EC4899;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        .phrase-button {
            margin: 0.25rem;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Get languages
    source_lang = user_profile.get('native_language', 'English')
    target_lang = get_target_language_from_country(country_data.get('name', 'Unknown'))
    
    # Language selection and swap
    col1, col2, col3 = st.columns([2, 1, 2])
    
    with col1:
        st.markdown(f'<div class="language-badge">🌐 From: {source_lang}</div>', unsafe_allow_html=True)
    
    with col2:
        if st.button("🔄 Swap", use_container_width=True):
            # Swap languages in session
            if 'swap_languages' not in st.session_state:
                st.session_state.swap_languages = False
            st.session_state.swap_languages = not st.session_state.swap_languages
            st.rerun()
    
    with col3:
        st.markdown(f'<div class="language-badge">🌍 To: {target_lang}</div>', unsafe_allow_html=True)
    
    # Check if languages are swapped
    if st.session_state.get('swap_languages', False):
        source_lang, target_lang = target_lang, source_lang
    
    # Common phrases section
    st.subheader("⚡ Quick Phrases")
    common_phrases = get_common_phrases_list(country_data)
    
    if common_phrases:
        phrase_cols = st.columns(4)
        for idx, (phrase_type, phrase_text) in enumerate(common_phrases.items()):
            with phrase_cols[idx % 4]:
                if st.button(
                    f"{phrase_type.replace('_', ' ').title()}",
                    key=f"phrase_{phrase_type}",
                    use_container_width=True,
                    help=f"Click to translate: {phrase_text}"
                ):
                    st.session_state.selected_phrase = phrase_text
    
    # Translation input
    st.subheader("💬 Your Phrase")
    
    col1, col2 = st.columns([5, 1])
    
    with col1:
        default_text = st.session_state.get('selected_phrase', '')
        phrase_input = st.text_area(
            "Enter phrase to translate",
            value=default_text,
            placeholder="Example: Where is the nearest hospital?",
            height=100,
            help="Type any phrase you want to translate with cultural context"
        )
        # Clear selected phrase after using it
        if 'selected_phrase' in st.session_state:
            del st.session_state.selected_phrase
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        voice_btn = st.button("🎤 Voice", use_container_width=True, help="Voice input (coming soon)")
        if voice_btn:
            st.info("🎤 Voice input coming soon!")
    
    translate_button = st.button(
        "🌍 Translate with Cultural Context",
        use_container_width=True,
        type="primary"
    )
    
    # Translation results
    if translate_button and phrase_input:
        # Check cache first
        cache_key = f"{phrase_input}_{source_lang}_{target_lang}"
        cached_result = get_cached_translation(cache_key)
        
        if cached_result:
            st.info("💾 Using cached translation")
            result = cached_result
        else:
            result = translate_phrase(
                phrase_input,
                source_lang,
                target_lang,
                country_data,
                groq_client
            )
            
            if result:
                # Cache the result
                cache_translation(cache_key, result)
        
        if result:
            st.markdown("---")
            st.subheader("✨ Translation Result")
            
            # Two-column layout for original and translated
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown(f"""
                    <div class="translation-card">
                        <h4>📝 Original ({result.source_language})</h4>
                        <p style="font-size: 1.2rem; margin-top: 1rem;">{result.original_text}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            with col2:
                st.markdown(f"""
                    <div class="translation-card">
                        <h4>🌍 Translation ({result.target_language})</h4>
                        <p style="font-size: 1.2rem; margin-top: 1rem; font-weight: 600;">{result.translated_text}</p>
                    </div>
                """, unsafe_allow_html=True)
            
            # Pronunciation guide
            st.markdown(f"""
                <div class="pronunciation-box">
                    <strong>🔊 Pronunciation:</strong><br>
                    {result.pronunciation}
                </div>
            """, unsafe_allow_html=True)
            
            # Audio playback
            if result.audio_data:
                st.audio(result.audio_data, format='audio/mp3')
            else:
                st.info("🔇 Audio generation unavailable for this language")
            
            # Tone guidance
            with st.expander("🎭 How to Say It (Tone & Etiquette)", expanded=True):
                st.markdown(result.tone_guidance)
            
            # Cultural notes
            if result.cultural_notes and result.cultural_notes != "No specific cultural notes":
                st.markdown(f"""
                    <div class="cultural-tip">
                        <strong>🌸 Cultural Tips:</strong><br>
                        {result.cultural_notes}
                    </div>
                """, unsafe_allow_html=True)
    
    elif translate_button:
        st.warning("⚠️ Please enter a phrase to translate.")
    
    # Cultural tips section
    st.markdown("---")
    st.subheader("🌍 Cultural Etiquette Tips")
    
    cultural_info = country_data.get('culture', {})
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("**✅ Do:**")
        dos = cultural_info.get('dos', [])
        if dos:
            for item in dos:
                st.markdown(f"- {item}")
        else:
            st.markdown("- Be respectful and polite")
    
    with col2:
        st.markdown("**❌ Don't:**")
        donts = cultural_info.get('donts', [])
        if donts:
            for item in donts:
                st.markdown(f"- {item}")
        else:
            st.markdown("- Avoid offensive gestures")
    
    # Greetings
    greetings = cultural_info.get('greetings', 'Standard greetings')
    st.markdown(f"**👋 Greetings:** {greetings}")
