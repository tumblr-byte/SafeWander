import streamlit as st
import json
import os
from groq import Groq
from PIL import Image, ImageDraw, ImageFont
import easyocr
from deep_translator import GoogleTranslator
from gtts import gTTS
import speech_recognition as sr
import tempfile
import io
import numpy as np

# Page config
st.set_page_config(
    page_title="SafeWander - AI Travel Safety",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS with Font Awesome
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    .main-header {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 1rem;
        margin: 2rem 0;
    }
    
    .app-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        font-weight: 500;
    }
    
    /* Threat level badges */
    .threat-high {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        display: inline-block;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    
    .threat-medium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        display: inline-block;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    
    .threat-low {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        display: inline-block;
        margin: 1rem 0;
        font-size: 1.1rem;
    }
    
    /* Response cards */
    .response-card {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        margin: 1.5rem 0;
        border: 2px solid #e2e8f0;
    }
    
    .quick-answer {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        padding: 1.2rem;
        border-radius: 12px;
        border-left: 4px solid #3b82f6;
        margin: 1rem 0;
        font-size: 1.1rem;
        line-height: 1.7;
        color: #1e40af;
    }
    
    .action-steps {
        background: #f8fafc;
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    .action-steps ol {
        margin: 0;
        padding-left: 1.5rem;
        color: #1e293b;
        font-size: 1.05rem;
        line-height: 2;
    }
    
    .action-steps ol li {
        margin: 0.5rem 0;
        font-weight: 500;
    }
    
    .emergency-alert {
        background: linear-gradient(135deg, #fef2f2 0%, #fee2e2 100%);
        padding: 1rem;
        border-radius: 12px;
        border-left: 4px solid #dc2626;
        margin: 1rem 0;
        font-size: 1.1rem;
        font-weight: 600;
        color: #991b1b;
    }
    
    /* Feature boxes */
    .feature-box {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
    }
    
    .feature-box h4 {
        color: #1e293b;
        font-size: 1.4rem;
        margin-bottom: 0.5rem;
    }
    
    /* Voice chat interface */
    .voice-container {
        display: flex;
        gap: 2rem;
        margin: 2rem 0;
    }
    
    .voice-side {
        flex: 1;
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        padding: 2rem;
        border-radius: 16px;
        border: 2px solid #cbd5e1;
    }
    
    .voice-side.tourist {
        border-left: 6px solid #3b82f6;
    }
    
    .voice-side.local {
        border-left: 6px solid #8b5cf6;
    }
    
    .voice-title {
        font-size: 1.3rem;
        font-weight: 700;
        margin-bottom: 1rem;
        color: #1e293b;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 600;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 12px;
        font-size: 1rem;
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        transform: scale(1.05);
        box-shadow: 0 8px 16px rgba(102, 126, 234, 0.3);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #667eea 0%, #764ba2 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .emergency-box {
        background: rgba(255,255,255,0.15);
        padding: 0.8rem;
        border-radius: 10px;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    /* Hide streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Icon styling */
    .fas, .fa {
        margin-right: 0.5rem;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_country' not in st.session_state:
    st.session_state.current_country = "India"

# Load dataset
@st.cache_data
def load_safety_data():
    if os.path.exists("dataset.json"):
        with open("dataset.json", "r") as f:
            return json.load(f)
    return {"countries": ["India", "Thailand", "Mexico", "USA", "Brazil"]}

# Initialize Groq
def init_groq():
    try:
        api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
        if api_key:
            return Groq(api_key=api_key)
    except Exception as e:
        st.warning(f"⚠️ Groq unavailable: {str(e)}")
    return None

# RAG Search
def search_safety_data(query, country, data):
    query_lower = query.lower()
    results = []
    
    for scam in data.get("transport_scams", []):
        if scam.get("country") == country:
            if any(word in query_lower for word in ["taxi", "driver", "uber", "transport", "price", "fare", "scam", "rupees", "₹"]):
                results.append({"type": "transport_scam", "data": scam})
    
    for safety in data.get("harassment_safety", []):
        if any(word in query_lower for word in ["follow", "harass", "touch", "stalk", "danger", "help", "emergency"]):
            results.append({"type": "harassment", "data": safety})
    
    emergency = data.get("emergency_numbers", {}).get(country, {})
    if emergency:
        results.append({"type": "emergency", "data": emergency})
    
    prices = data.get("price_reference", {}).get(country, {})
    if prices:
        results.append({"type": "price_reference", "data": prices})
    
    return results

# AI Advisor with BETTER formatting
def get_ai_advice(query, country, groq_client, safety_data):
    relevant_info = search_safety_data(query, country, safety_data)
    
    context = f"User in {country} asks: {query}\n\nData:\n"
    
    for item in relevant_info[:3]:
        if item["type"] == "transport_scam":
            data = item["data"]
            context += f"Normal rate: {data.get('normal_rate')}, Scam indicator: {data.get('scam_rate')}, Safety: {data.get('safety_advice')}\n"
        elif item["type"] == "emergency":
            context += f"Emergency: {item['data']}\n"
        elif item["type"] == "price_reference":
            context += f"Prices: {item['data']}\n"
    
    system_prompt = """You're SafeWander AI. Respond in this EXACT format using HTML tags:

<div class="threat-[high/medium/low]">🚨 THREAT: [HIGH/MEDIUM/LOW]</div>

<div class="quick-answer">
<strong>💡 Quick Answer:</strong><br/>
[2 clear sentences explaining if safe/scam and why]
</div>

<div class="action-steps">
<strong>✅ What To Do Now:</strong>
<ol>
<li>[Immediate action]</li>
<li>[Alternative option]</li>
<li>[Safety backup]</li>
</ol>
</div>

<div class="emergency-alert">
<strong>🆘 Emergency Help:</strong> Police: [number] | Tourist Help: [number]
</div>

Be direct, actionable, and use the data provided. Match threat level to severity."""
    
    try:
        if groq_client:
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=400
            )
            return chat_completion.choices[0].message.content
        else:
            return f"""<div class="threat-medium">🚨 THREAT: MEDIUM</div>

<div class="quick-answer">
<strong>💡 Quick Answer:</strong><br/>
Based on {country} rates, verify the price against typical fares. Use ride apps or metered taxis for transparency.
</div>

<div class="action-steps">
<strong>✅ What To Do Now:</strong>
<ol>
<li>Ask driver to use meter or check ride app prices</li>
<li>Negotiate or find alternative transport</li>
<li>Note vehicle details if you feel unsafe</li>
</ol>
</div>

<div class="emergency-alert">
<strong>🆘 Emergency Help:</strong> Check sidebar for local numbers
</div>"""
    except Exception as e:
        return f"<div class='quick-answer'>Error: {str(e)}</div>"

# Visual Translation - FIXED
def translate_image_text(image, source_lang='hi', target_lang='en'):
    try:
        reader = easyocr.Reader([source_lang, 'en'], gpu=False)
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image
        
        results = reader.readtext(img_array)
        
        if not results:
            return image, []
        
        translated_img = Image.fromarray(img_array) if not isinstance(image, Image.Image) else image.copy()
        draw = ImageDraw.Draw(translated_img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        translations = []
        
        for (bbox, text, prob) in results:
            if prob > 0.4:
                try:
                    translated_text = translator.translate(text)
                except:
                    translated_text = text
                
                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))
                
                draw.rectangle([top_left, bottom_right], fill=(0, 0, 0, 180), outline=(255, 215, 0), width=3)
                draw.text((top_left[0] + 5, top_left[1] + 5), translated_text, fill=(255, 255, 255), font=font)
                
                translations.append({
                    "original": text,
                    "translated": translated_text,
                    "confidence": prob
                })
        
        return translated_img, translations
    
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return image, []

# TTS
def text_to_speech(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(fp.name)
        return fp.name
    except Exception as e:
        return None

# Speech Recognition
def recognize_speech(language='en'):
    try:
        recognizer = sr.Recognizer()
        with sr.Microphone() as source:
            st.info("🎤 Listening... Speak now!")
            recognizer.adjust_for_ambient_noise(source, duration=0.5)
            audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
            
        text = recognizer.recognize_google(audio, language=language)
        return text
    except sr.WaitTimeoutError:
        return "⏱️ No speech detected"
    except sr.UnknownValueError:
        return "❌ Could not understand audio"
    except Exception as e:
        return f"❌ Error: {str(e)}"

# Main App
def main():
    # Header
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        if os.path.exists("logo.png"):
            logo_col1, logo_col2 = st.columns([1, 4])
            with logo_col1:
                st.image("logo.png", width=80)
            with logo_col2:
                st.markdown('<h1 class="app-title">SafeWander</h1>', unsafe_allow_html=True)
        else:
            st.markdown('<h1 class="app-title"><i class="fas fa-shield-alt"></i> SafeWander</h1>', unsafe_allow_html=True)
    
    st.markdown('<p class="subtitle">AI-Powered Travel Safety Companion</p>', unsafe_allow_html=True)
    
    # Initialize
    safety_data = load_safety_data()
    groq_client = init_groq()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### <i class='fas fa-map-marker-alt'></i> Location", unsafe_allow_html=True)
        
        country = st.selectbox(
            "Current Country",
            ["India", "Thailand", "Mexico", "USA", "Brazil"],
            index=0,
            label_visibility="collapsed"
        )
        st.session_state.current_country = country
        
        st.markdown("---")
        st.markdown("### <i class='fas fa-phone-alt'></i> Emergency", unsafe_allow_html=True)
        
        emergency_nums = safety_data.get("emergency_numbers", {}).get(country, {})
        for service, number in emergency_nums.items():
            st.markdown(f'<div class="emergency-box"><strong>{service.title()}</strong><br/><span style="font-size:1.2rem">{number}</span></div>', unsafe_allow_html=True)
    
    # Tabs
    tab1, tab2, tab3 = st.tabs([
        "🤖 AI Advisor", 
        "📸 Translator", 
        "🎤 Voice Chat"
    ])
    
    # TAB 1: AI Advisor
    with tab1:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.markdown("#### <i class='fas fa-robot'></i> AI Safety Advisor", unsafe_allow_html=True)
        st.markdown("Get instant, actionable safety advice")
        st.markdown('</div>', unsafe_allow_html=True)
        
        user_query = st.text_area(
            "Describe your situation:",
            placeholder="E.g., Driver wants ₹800 for 5km, is this fair?",
            height=100
        )
        
        col1, col2 = st.columns([1, 3])
        with col1:
            if st.button("Get Advice", use_container_width=True):
                if user_query:
                    with st.spinner("Analyzing..."):
                        response = get_ai_advice(user_query, country, groq_client, safety_data)
                        st.session_state.chat_history.append({
                            "query": user_query,
                            "response": response,
                            "country": country
                        })
        
        # Display responses
        if st.session_state.chat_history:
            st.markdown("---")
            for chat in reversed(st.session_state.chat_history[-2:]):
                st.markdown(f"**Your Question ({chat['country']}):** *{chat['query']}*")
                st.markdown(f'<div class="response-card">{chat["response"]}</div>', unsafe_allow_html=True)
                st.markdown("---")
    
    # TAB 2: Translator
    with tab2:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.markdown("#### <i class='fas fa-language'></i> Visual Translator", unsafe_allow_html=True)
        st.markdown("Translate signs, menus, notices")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            source_lang = st.selectbox(
                "From:",
                [("Hindi", "hi"), ("Thai", "th"), ("Spanish", "es"), ("Portuguese", "pt")],
                format_func=lambda x: x[0]
            )[1]
        
        with col2:
            target_lang = "en"
            st.selectbox("To:", ["English"], disabled=True)
        
        uploaded_file = st.file_uploader("Upload image", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            try:
                image = Image.open(uploaded_file).convert('RGB')
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Original**")
                    st.image(image, use_column_width=True)
                
                if st.button("🔤 Translate Now", use_container_width=True):
                    with st.spinner("Translating..."):
                        translated_img, translations = translate_image_text(image, source_lang, target_lang)
                        
                        with col2:
                            st.markdown("**Translated**")
                            st.image(translated_img, use_column_width=True)
                        
                        if translations:
                            st.success(f"✅ Translated {len(translations)} text sections")
                        else:
                            st.warning("No text detected. Try a clearer image.")
            except Exception as e:
                st.error(f"Error processing image: {str(e)}")
    
    # TAB 3: Voice Chat
    with tab3:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.markdown("#### <i class='fas fa-comments'></i> Voice Communication Bridge", unsafe_allow_html=True)
        st.markdown("Real-time voice translation between tourist and local")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Emergency phrases first
        st.markdown("### <i class='fas fa-exclamation-triangle'></i> Emergency Phrases", unsafe_allow_html=True)
        
        emergency_phrases = {
            "India": [
                ("Help!", "Madad karo!", "hi"),
                ("Call police!", "Police bulao!", "hi"),
                ("I need doctor", "Doctor chahiye", "hi"),
                ("Leave me alone!", "Chod do mujhe!", "hi")
            ],
            "Thailand": [
                ("Help!", "Chuay duay!", "th"),
                ("Call police!", "Riak tamruat!", "th")
            ],
            "Mexico": [
                ("Help!", "¡Ayuda!", "es"),
                ("Call police!", "¡Llama policía!", "es")
            ],
            "Brazil": [
                ("Help!", "Socorro!", "pt"),
                ("Call police!", "Chame polícia!", "pt")
            ],
            "USA": [
                ("Call 911", "Call 911", "en")
            ]
        }
        
        phrases = emergency_phrases.get(country, [])
        cols = st.columns(2)
        for i, (english, local, lang) in enumerate(phrases):
            with cols[i % 2]:
                if st.button(f"🔊 {english}", key=f"emg_{i}", use_container_width=True):
                    audio_file = text_to_speech(local, lang)
                    if audio_file:
                        st.audio(audio_file, autoplay=True)
                        st.success(f"**Says:** {local}")
        
        st.markdown("---")
        st.markdown("### <i class='fas fa-exchange-alt'></i> Two-Way Voice Translation", unsafe_allow_html=True)
        
        # Language mapping
        lang_map = {"India": "hi", "Thailand": "th", "Mexico": "es", "Brazil": "pt", "USA": "en"}
        local_lang = lang_map.get(country, "hi")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown('<div class="voice-side tourist">', unsafe_allow_html=True)
            st.markdown('<div class="voice-title"><i class="fas fa-user"></i> Tourist Side (English)</div>', unsafe_allow_html=True)
            
            if st.button("🎤 Speak English", key="tourist_speak", use_container_width=True):
                tourist_text = recognize_speech('en-US')
                st.session_state.tourist_text = tourist_text
                st.info(f"You said: **{tourist_text}**")
            
            if 'tourist_text' in st.session_state and st.session_state.tourist_text:
                if st.button(f"🔊 Translate to {country} Language", key="trans_to_local", use_container_width=True):
                    try:
                        translator = GoogleTranslator(source='en', target=local_lang)
                        translated = translator.translate(st.session_state.tourist_text)
                        st.success(f"**Translation:** {translated}")
                        
                        audio_file = text_to_speech(translated, local_lang)
                        if audio_file:
                            st.audio(audio_file, autoplay=True)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col2:
            st.markdown('<div class="voice-side local">', unsafe_allow_html=True)
            st.markdown(f'<div class="voice-title"><i class="fas fa-user-tie"></i> Local Side ({country})</div>', unsafe_allow_html=True)
            
            lang_codes = {"India": "hi-IN", "Thailand": "th-TH", "Mexico": "es-MX", "Brazil": "pt-BR", "USA": "en-US"}
            local_code = lang_codes.get(country, "hi-IN")
            
            if st.button(f"🎤 Speak {country} Language", key="local_speak", use_container_width=True):
                local_text = recognize_speech(local_code)
                st.session_state.local_text = local_text
                st.info(f"They said: **{local_text}**")
            
            if 'local_text' in st.session_state and st.session_state.local_text:
                if st.button("🔊 Translate to English", key="trans_to_eng", use_container_width=True):
                    try:
                        translator = GoogleTranslator(source=local_lang, target='en')
                        translated = translator.translate(st.session_state.local_text)
                        st.success(f"**Translation:** {translated}")
                        
                        audio_file = text_to_speech(translated, 'en')
                        if audio_file:
                            st.audio(audio_file, autoplay=True)
                    except Exception as e:
                        st.error(f"Error: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.info("💡 **How it works:** Tourist speaks English → Translates to local language. Local speaks their language → Translates to English. Both hear audio!")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #94a3b8; padding: 1.5rem;'>
        <p><strong>SafeWander</strong> - VisaVerse AI Hackathon 2024</p>
        <p>Stay safe. Travel fearlessly. 🌍</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
