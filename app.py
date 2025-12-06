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

# Custom CSS - STUNNING UI
st.markdown("""
<style>
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
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
    
    /* Card Styles */
    .info-card {
        background: linear-gradient(135deg, #f5f7fa 0%, #c3cfe2 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        margin: 1rem 0;
        color: #1e293b;
    }
    
    .warning-card {
        background: linear-gradient(135deg, #fff7ed 0%, #fed7aa 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #f59e0b;
        margin: 1rem 0;
        color: #78350f;
    }
    
    .danger-card {
        background: linear-gradient(135deg, #fef2f2 0%, #fecaca 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #ef4444;
        margin: 1rem 0;
        color: #7f1d1d;
    }
    
    .success-card {
        background: linear-gradient(135deg, #f0fdf4 0%, #bbf7d0 100%);
        padding: 1.5rem;
        border-radius: 12px;
        border-left: 4px solid #22c55e;
        margin: 1rem 0;
        color: #14532d;
    }
    
    /* Feature Cards */
    .feature-box {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .feature-box:hover {
        transform: translateY(-4px);
        box-shadow: 0 12px 24px -4px rgba(0,0,0,0.15);
    }
    
    /* Response formatting */
    .ai-response {
        background: white;
        padding: 1.5rem;
        border-radius: 12px;
        border: 1px solid #e2e8f0;
        margin: 1rem 0;
        color: #1e293b;
        line-height: 1.8;
    }
    
    .ai-response h4 {
        color: #1e293b;
        margin-bottom: 1rem;
        font-size: 1.2rem;
    }
    
    .ai-response ul {
        color: #334155;
        line-height: 1.8;
    }
    
    .ai-response strong {
        color: #0f172a;
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
    
    /* Emergency number styling */
    .emergency-box {
        background: rgba(255,255,255,0.1);
        padding: 0.5rem 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        backdrop-filter: blur(10px);
    }
    
    /* Hide streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Tab styling */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2rem;
    }
    
    .stTabs [data-baseweb="tab"] {
        padding: 1rem 2rem;
        font-size: 1.1rem;
        font-weight: 600;
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
    # Load from dataset.json if exists
    if os.path.exists("dataset.json"):
        with open("dataset.json", "r") as f:
            return json.load(f)
    # Fallback minimal data
    return {"countries": ["India", "Thailand", "Mexico", "USA", "Brazil"]}

# Initialize Groq client
def init_groq():
    try:
        api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
        if api_key:
            return Groq(api_key=api_key)
    except Exception as e:
        st.warning(f"⚠️ Groq API unavailable: {str(e)}")
    return None

# RAG Search Function
def search_safety_data(query, country, data):
    """Search through safety data for relevant information"""
    query_lower = query.lower()
    results = []
    
    # Search transport scams
    for scam in data.get("transport_scams", []):
        if scam.get("country") == country:
            if any(word in query_lower for word in ["taxi", "driver", "uber", "transport", "price", "fare", "scam"]):
                results.append({"type": "transport_scam", "data": scam})
    
    # Search harassment safety
    for safety in data.get("harassment_safety", []):
        if any(word in query_lower for word in ["follow", "harass", "touch", "stalk", "danger", "help", "emergency"]):
            results.append({"type": "harassment", "data": safety})
    
    # Emergency numbers
    emergency = data.get("emergency_numbers", {}).get(country, {})
    if any(word in query_lower for word in ["emergency", "police", "ambulance", "help", "call"]):
        results.append({"type": "emergency", "data": emergency})
    
    # Price reference
    prices = data.get("price_reference", {}).get(country, {})
    if any(word in query_lower for word in ["price", "cost", "how much", "fare", "normal"]):
        results.append({"type": "price_reference", "data": prices})
    
    return results

# AI Safety Advisor - CONCISE RESPONSES
def get_ai_advice(query, country, groq_client, safety_data):
    """Get concise AI-powered safety advice"""
    
    relevant_info = search_safety_data(query, country, safety_data)
    
    context = f"User in {country} asks: {query}\n\nRelevant data:\n"
    
    for item in relevant_info[:3]:
        if item["type"] == "transport_scam":
            data = item["data"]
            context += f"Normal: {data.get('normal_rate')}, Scam: {data.get('scam_rate')}, Advice: {data.get('safety_advice')}\n"
        elif item["type"] == "emergency":
            context += f"Emergency numbers: {item['data']}\n"
        elif item["type"] == "price_reference":
            context += f"Typical prices: {item['data']}\n"
    
    system_prompt = """You are SafeWander AI. Give SHORT, actionable safety advice.

Format your response EXACTLY like this:

**🚨 Threat: [HIGH/MEDIUM/LOW]**

**Quick Answer:**
[2-3 sentences max explaining if it's safe/scam]

**What To Do:**
1. [Action 1]
2. [Action 2]  
3. [Action 3]

**Emergency:** [Relevant number if needed]

Keep it BRIEF. No long explanations. Be direct."""
    
    try:
        if groq_client:
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=300
            )
            return chat_completion.choices[0].message.content
        else:
            # Fallback concise response
            return f"""**🚨 Threat: MEDIUM**

**Quick Answer:**
Based on typical {country} rates, this might be overpriced. Check the distance and compare with standard rates.

**What To Do:**
1. Ask driver for meter/use ride app
2. Check typical rates: {relevant_info[0]['data'].get('normal_rate') if relevant_info else 'varies'}
3. If uncomfortable, find alternative transport

**Need Help?** Call local emergency services."""
    except Exception as e:
        return f"Error: {str(e)}"

# Visual Translation
def translate_image_text(image, source_lang='hi', target_lang='en'):
    """Extract and translate text from image"""
    try:
        reader = easyocr.Reader([source_lang, 'en'], gpu=False)
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        
        # Convert to numpy array properly
        if isinstance(image, Image.Image):
            img_array = np.array(image)
        else:
            img_array = image
        
        # Extract text
        results = reader.readtext(img_array)
        
        # Create copy for drawing
        translated_img = Image.fromarray(img_array) if not isinstance(image, Image.Image) else image.copy()
        draw = ImageDraw.Draw(translated_img)
        
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 16)
        except:
            font = ImageFont.load_default()
        
        translations = []
        
        for (bbox, text, prob) in results:
            if prob > 0.5:
                try:
                    translated_text = translator.translate(text)
                except:
                    translated_text = text
                
                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))
                
                # Draw background rectangle
                draw.rectangle([top_left, bottom_right], fill=(0, 0, 0, 180), outline=(255, 215, 0), width=2)
                
                # Draw text
                draw.text((top_left[0] + 5, top_left[1] + 5), translated_text, fill=(255, 255, 255), font=font)
                
                translations.append({
                    "original": text,
                    "translated": translated_text,
                    "confidence": prob
                })
        
        return translated_img, translations
    
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return image, []

# TTS Function
def text_to_speech(text, lang='en'):
    """Convert text to speech"""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(fp.name)
        return fp.name
    except Exception as e:
        st.error(f"TTS error: {str(e)}")
        return None

# Main App
def main():
    # Header with logo
    col1, col2, col3 = st.columns([1, 3, 1])
    with col2:
        st.markdown('<div class="main-header">', unsafe_allow_html=True)
        if os.path.exists("logo.png"):
            logo_col1, logo_col2 = st.columns([1, 4])
            with logo_col1:
                st.image("logo.png", width=80)
            with logo_col2:
                st.markdown('<h1 class="app-title">SafeWander</h1>', unsafe_allow_html=True)
        else:
            st.markdown('<h1 class="app-title"><i class="fas fa-shield-alt"></i> SafeWander</h1>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<p class="subtitle">Your AI-Powered Travel Safety Companion</p>', unsafe_allow_html=True)
    
    # Initialize
    safety_data = load_safety_data()
    groq_client = init_groq()
    
    # Sidebar
    with st.sidebar:
        st.markdown("### <i class='fas fa-cog'></i> Settings", unsafe_allow_html=True)
        
        country = st.selectbox(
            "📍 Current Location",
            ["India", "Thailand", "Mexico", "USA", "Brazil"],
            index=0
        )
        st.session_state.current_country = country
        
        st.markdown("---")
        st.markdown("### <i class='fas fa-phone-alt'></i> Emergency Numbers", unsafe_allow_html=True)
        
        emergency_nums = safety_data.get("emergency_numbers", {}).get(country, {})
        for service, number in emergency_nums.items():
            st.markdown(f'<div class="emergency-box"><strong>{service.title()}</strong><br/>{number}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.markdown("### <i class='fas fa-lightbulb'></i> Quick Tips", unsafe_allow_html=True)
        st.markdown("""
        <div style='font-size: 0.9rem; line-height: 1.6;'>
        • Save emergency numbers<br/>
        • Share live location<br/>
        • Trust your instincts<br/>
        • Stay in lit areas at night
        </div>
        """, unsafe_allow_html=True)
    
    # Main tabs
    tab1, tab2, tab3 = st.tabs([
        "🤖 AI Safety Advisor", 
        "📸 Visual Translator", 
        "🎤 Voice Bridge"
    ])
    
    # TAB 1: AI Safety Advisor
    with tab1:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.markdown("#### <i class='fas fa-robot'></i> AI Safety Advisor", unsafe_allow_html=True)
        st.markdown("Get instant, actionable safety advice for any situation")
        st.markdown('</div>', unsafe_allow_html=True)
        
        with st.expander("💡 Try asking..."):
            st.markdown("""
            • "Driver wants ₹800 for 5km, fair?"
            • "Someone following me, what do I do?"
            • "Is this restaurant bill normal?"
            • "Safe to walk here at night?"
            """)
        
        user_query = st.text_area(
            "Describe your situation:",
            placeholder="E.g., Taxi quoted ₹500 for airport to hotel",
            height=80
        )
        
        col1, col2 = st.columns([1, 4])
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
                else:
                    st.warning("Please describe your situation")
        
        with col2:
            if st.button("Clear History", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        # Display responses
        if st.session_state.chat_history:
            st.markdown("---")
            for chat in reversed(st.session_state.chat_history[-3:]):  # Only show last 3
                st.markdown(f"**Your Question ({chat['country']}):**")
                st.markdown(f"*{chat['query']}*")
                
                # Style based on threat level
                response_text = chat['response']
                if "HIGH" in response_text.upper():
                    st.markdown(f'<div class="danger-card">{response_text}</div>', unsafe_allow_html=True)
                elif "MEDIUM" in response_text.upper():
                    st.markdown(f'<div class="warning-card">{response_text}</div>', unsafe_allow_html=True)
                else:
                    st.markdown(f'<div class="success-card">{response_text}</div>', unsafe_allow_html=True)
                
                st.markdown("---")
    
    # TAB 2: Visual Translator
    with tab2:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.markdown("#### <i class='fas fa-language'></i> Visual Translator", unsafe_allow_html=True)
        st.markdown("Translate signs, menus, and notices instantly")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            source_lang = st.selectbox(
                "From:",
                [("Hindi", "hi"), ("Thai", "th"), ("Spanish", "es"), ("Portuguese", "pt")],
                format_func=lambda x: x[0]
            )[1]
        
        with col2:
            target_lang = st.selectbox(
                "To:",
                [("English", "en"), ("Spanish", "es")],
                format_func=lambda x: x[0]
            )[1]
        
        uploaded_file = st.file_uploader("Upload image", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            try:
                image = Image.open(uploaded_file)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    st.markdown("**Original**")
                    st.image(image, use_column_width=True)
                
                if st.button("🔤 Translate", use_container_width=True):
                    with st.spinner("Translating..."):
                        translated_img, translations = translate_image_text(image, source_lang, target_lang)
                        
                        with col2:
                            st.markdown("**Translated**")
                            st.image(translated_img, use_column_width=True)
                        
                        if translations:
                            st.success(f"✅ Translated {len(translations)} text blocks")
                            with st.expander("View details"):
                                for i, trans in enumerate(translations, 1):
                                    st.markdown(f"**{i}.** {trans['original']} → **{trans['translated']}**")
                        else:
                            st.warning("No text detected")
            except Exception as e:
                st.error(f"Error: {str(e)}")
    
    # TAB 3: Voice Bridge
    with tab3:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.markdown("#### <i class='fas fa-microphone'></i> Voice Communication", unsafe_allow_html=True)
        st.markdown("Quick emergency phrases in local language")
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("### <i class='fas fa-exclamation-triangle'></i> Emergency Phrases")
        
        emergency_phrases = {
            "India": [
                ("Help!", "Madad karo!", "hi"),
                ("Call police!", "Police bulao!", "hi"),
                ("I need doctor", "Doctor chahiye", "hi"),
                ("Leave me alone!", "Mujhe akela chhod do!", "hi")
            ],
            "Thailand": [
                ("Help!", "Chuay duay!", "th"),
                ("Call police!", "Riak tamruat!", "th"),
                ("I need doctor", "Chan tong kan mor", "th")
            ],
            "Mexico": [
                ("Help!", "¡Ayuda!", "es"),
                ("Call police!", "¡Llama policía!", "es"),
                ("I need doctor", "Necesito médico", "es")
            ],
            "Brazil": [
                ("Help!", "Socorro!", "pt"),
                ("Call police!", "Chame polícia!", "pt"),
                ("I need doctor", "Preciso médico", "pt")
            ],
            "USA": [
                ("Call 911", "Call 911", "en"),
                ("I need help", "I need help", "en")
            ]
        }
        
        phrases = emergency_phrases.get(country, [])
        
        cols = st.columns(2)
        for i, (english, local, lang) in enumerate(phrases):
            with cols[i % 2]:
                if st.button(f"🔊 {english}", key=f"phrase_{i}", use_container_width=True):
                    audio_file = text_to_speech(local, lang)
                    if audio_file:
                        st.audio(audio_file)
                        st.success(f"**{local}**")
        
        st.markdown("---")
        st.markdown("### <i class='fas fa-exchange-alt'></i> Custom Translation")
        
        english_text = st.text_input("Your message (English):", placeholder="Where is the hospital?")
        
        if st.button("🔊 Translate & Speak"):
            if english_text:
                lang_map = {"India": "hi", "Thailand": "th", "Mexico": "es", "Brazil": "pt", "USA": "en"}
                target = lang_map.get(country, "en")
                
                try:
                    translator = GoogleTranslator(source='en', target=target)
                    translated_text = translator.translate(english_text)
                    
                    st.success(f"**Translation:** {translated_text}")
                    
                    audio_file = text_to_speech(translated_text, target)
                    if audio_file:
                        st.audio(audio_file)
                except Exception as e:
                    st.error(f"Error: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #94a3b8; padding: 1.5rem;'>
        <p><strong>SafeWander</strong> - VisaVerse AI Hackathon 2024</p>
        <p style='font-size: 0.9rem;'>Stay safe. Travel fearlessly. 🌍</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
