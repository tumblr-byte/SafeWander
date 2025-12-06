import streamlit as st
import json
import os
from groq import Groq
from PIL import Image, ImageDraw, ImageFont
import easyocr
from googletrans import Translator
from gtts import gTTS
import speech_recognition as sr
import tempfile
import io

# Page config
st.set_page_config(
    page_title="SafeWander - AI Travel Safety Companion",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        font-weight: bold;
        text-align: center;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 0.5rem;
    }
    .sub-header {
        text-align: center;
        color: #666;
        font-size: 1.2rem;
        margin-bottom: 2rem;
    }
    .feature-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 15px;
        color: white;
        margin: 1rem 0;
        box-shadow: 0 10px 30px rgba(0,0,0,0.2);
    }
    .warning-box {
        background-color: #fff3cd;
        border-left: 5px solid #ffc107;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .danger-box {
        background-color: #f8d7da;
        border-left: 5px solid #dc3545;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .safe-box {
        background-color: #d4edda;
        border-left: 5px solid #28a745;
        padding: 1rem;
        border-radius: 5px;
        margin: 1rem 0;
    }
    .stButton>button {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: bold;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-size: 1rem;
    }
    .emergency-button {
        background: linear-gradient(90deg, #ff416c 0%, #ff4b2b 100%) !important;
        animation: pulse 2s infinite;
    }
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.05); }
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
    # In production, load from dataset.json file
    # For demo, we'll use the embedded data
    return {
        "countries": ["India", "Thailand", "Mexico", "USA", "Brazil"],
        # ... (full dataset from above)
    }

# Initialize Groq client
def init_groq():
    api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
    if api_key:
        return Groq(api_key=api_key)
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
                results.append({
                    "type": "transport_scam",
                    "data": scam
                })
    
    # Search harassment safety
    for safety in data.get("harassment_safety", []):
        if any(word in query_lower for word in ["follow", "harass", "touch", "stalk", "danger", "help", "emergency"]):
            results.append({
                "type": "harassment",
                "data": safety
            })
    
    # Search accommodation
    for accom in data.get("accommodation_scams", []):
        if accom.get("country") == country:
            if any(word in query_lower for word in ["hotel", "accommodation", "stay", "room", "booking"]):
                results.append({
                    "type": "accommodation",
                    "data": accom
                })
    
    # Search shopping
    for shop in data.get("shopping_scams", []):
        if shop.get("country") == country:
            if any(word in query_lower for word in ["buy", "shop", "price", "gem", "jewelry", "market"]):
                results.append({
                    "type": "shopping",
                    "data": shop
                })
    
    # Add emergency numbers
    emergency = data.get("emergency_numbers", {}).get(country, {})
    if any(word in query_lower for word in ["emergency", "police", "ambulance", "help", "call"]):
        results.append({
            "type": "emergency",
            "data": emergency
        })
    
    # Add price reference
    prices = data.get("price_reference", {}).get(country, {})
    if any(word in query_lower for word in ["price", "cost", "how much", "fare", "normal"]):
        results.append({
            "type": "price_reference",
            "data": prices
        })
    
    return results

# AI Safety Advisor
def get_ai_advice(query, country, groq_client, safety_data):
    """Get AI-powered safety advice using RAG"""
    
    # Search relevant data
    relevant_info = search_safety_data(query, country, safety_data)
    
    # Build context for AI
    context = f"User is in {country}. Query: {query}\n\nRelevant Safety Information:\n"
    
    for item in relevant_info[:5]:  # Limit to top 5 results
        if item["type"] == "transport_scam":
            data = item["data"]
            context += f"\nTransport Scam Alert: {data.get('scam_type')}\n"
            context += f"Normal Rate: {data.get('normal_rate')}\n"
            context += f"Scam Rate: {data.get('scam_rate')}\n"
            context += f"Safety Advice: {data.get('safety_advice')}\n"
            context += f"Threat Level: {data.get('threat_level')}\n"
        
        elif item["type"] == "harassment":
            data = item["data"]
            context += f"\nHarassment/Safety Protocol:\n"
            context += f"Situation: {data.get('situation')}\n"
            context += f"Threat Level: {data.get('threat_level')}\n"
            actions = data.get('immediate_actions', [])
            context += f"Actions: {', '.join(actions[:3])}\n"
        
        elif item["type"] == "emergency":
            context += f"\nEmergency Numbers for {country}:\n"
            for key, value in item["data"].items():
                context += f"{key}: {value}\n"
        
        elif item["type"] == "price_reference":
            context += f"\nTypical Prices in {country}:\n{item['data']}\n"
    
    # Create prompt for Groq
    system_prompt = """You are SafeWander AI, a travel safety expert. 
    Provide clear, actionable safety advice to travelers.
    - Be direct and specific
    - Highlight scams and dangers clearly
    - Give step-by-step actions
    - Include relevant emergency numbers
    - Use threat levels: LOW, MEDIUM, HIGH
    - Be empathetic but firm about safety"""
    
    user_prompt = f"{context}\n\nBased on this information, provide comprehensive safety advice for the user's query."
    
    try:
        if groq_client:
            chat_completion = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.7,
                max_tokens=1000
            )
            return chat_completion.choices[0].message.content
        else:
            # Fallback response without API
            return f"⚠️ **Safety Alert for {country}**\n\nBased on available data:\n{context}\n\nPlease set up GROQ_API_KEY for full AI-powered responses."
    except Exception as e:
        return f"Error getting AI response: {str(e)}\n\nRelevant info:\n{context}"

# Visual Translation Feature
def translate_image_text(image, source_lang='hi', target_lang='en'):
    """Extract text from image and overlay translation"""
    try:
        # Initialize OCR and translator
        reader = easyocr.Reader([source_lang, 'en'])
        translator = Translator()
        
        # Convert PIL image to format easyocr expects
        img_array = np.array(image)
        
        # Extract text with coordinates
        results = reader.readtext(img_array)
        
        # Create a copy of image for drawing
        translated_img = image.copy()
        draw = ImageDraw.Draw(translated_img)
        
        # Try to load a font, fallback to default
        try:
            font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans-Bold.ttf", 20)
        except:
            font = ImageFont.load_default()
        
        translations = []
        
        for (bbox, text, prob) in results:
            if prob > 0.5:  # Only use confident detections
                # Translate text
                try:
                    translated = translator.translate(text, src=source_lang, dest=target_lang)
                    translated_text = translated.text
                except:
                    translated_text = text
                
                # Get bounding box coordinates
                top_left = tuple(map(int, bbox[0]))
                bottom_right = tuple(map(int, bbox[2]))
                
                # Draw semi-transparent rectangle
                draw.rectangle([top_left, bottom_right], fill=(0, 0, 0, 180), outline=(255, 255, 0, 255), width=2)
                
                # Draw translated text
                draw.text((top_left[0] + 5, top_left[1] + 5), translated_text, fill=(255, 255, 255, 255), font=font)
                
                translations.append({
                    "original": text,
                    "translated": translated_text,
                    "confidence": prob
                })
        
        return translated_img, translations
    
    except Exception as e:
        st.error(f"Translation error: {str(e)}")
        return image, []

# Voice Communication Feature
def text_to_speech(text, lang='en'):
    """Convert text to speech"""
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(fp.name)
        return fp.name
    except Exception as e:
        st.error(f"Text-to-speech error: {str(e)}")
        return None

# Main App
def main():
    # Header with logo
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        # Display logo if exists
        if os.path.exists("logo.png"):
            st.image("logo.png", width=200)
    
    st.markdown('<p class="main-header">🛡️ SafeWander</p>', unsafe_allow_html=True)
    st.markdown('<p class="sub-header">Your AI Travel Safety Companion - Stay Safe Anywhere</p>', unsafe_allow_html=True)
    
    # Initialize
    safety_data = load_safety_data()
    groq_client = init_groq()
    
    # Sidebar
    with st.sidebar:
        st.header("⚙️ Settings")
        
        country = st.selectbox(
            "📍 Select Country",
            ["India", "Thailand", "Mexico", "USA", "Brazil"],
            index=0
        )
        st.session_state.current_country = country
        
        st.markdown("---")
        st.markdown("### 🚨 Emergency Numbers")
        emergency_nums = safety_data.get("emergency_numbers", {}).get(country, {})
        for service, number in emergency_nums.items():
            st.markdown(f"**{service.title()}:** `{number}`")
        
        st.markdown("---")
        st.markdown("### 💡 Quick Safety Tips")
        st.info("✓ Save emergency numbers\n✓ Share location with trusted contact\n✓ Trust your instincts\n✓ Stay in well-lit areas at night")
    
    # Main content tabs
    tab1, tab2, tab3 = st.tabs(["🤖 AI Safety Advisor", "📸 Visual Translator", "🎤 Voice Bridge"])
    
    # TAB 1: AI Safety Advisor
    with tab1:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🤖 AI Safety Advisor")
        st.markdown("Get instant, context-aware safety advice for any situation")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Example scenarios
        with st.expander("💡 Example Scenarios to Try"):
            st.markdown("""
            - "Driver asking ₹800 from airport to hotel, is this fair?"
            - "Someone has been following me for 10 minutes, what should I do?"
            - "Restaurant bill seems too high, is this normal?"
            - "How safe is it to walk around at night here?"
            - "What are common scams I should watch out for?"
            """)
        
        # Chat interface
        user_query = st.text_area(
            "Describe your situation or ask a safety question:",
            placeholder="Example: A taxi driver quoted ₹500 for a 5km trip. Is this fair?",
            height=100
        )
        
        col1, col2 = st.columns([1, 4])
        with col1:
            if st.button("🔍 Get Advice", use_container_width=True):
                if user_query:
                    with st.spinner("Analyzing situation and searching safety database..."):
                        response = get_ai_advice(user_query, country, groq_client, safety_data)
                        
                        # Add to chat history
                        st.session_state.chat_history.append({
                            "query": user_query,
                            "response": response,
                            "country": country
                        })
                else:
                    st.warning("Please enter a question or describe your situation")
        
        with col2:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.chat_history = []
                st.rerun()
        
        # Display chat history
        if st.session_state.chat_history:
            st.markdown("---")
            st.markdown("### 💬 Conversation History")
            for i, chat in enumerate(reversed(st.session_state.chat_history[-5:])):
                with st.container():
                    st.markdown(f"**You asked ({chat['country']}):** {chat['query']}")
                    
                    # Determine threat level for styling
                    if "HIGH" in chat['response'].upper() or "DANGER" in chat['response'].upper():
                        st.markdown(f'<div class="danger-box">{chat["response"]}</div>', unsafe_allow_html=True)
                    elif "MEDIUM" in chat['response'].upper() or "WARNING" in chat['response'].upper():
                        st.markdown(f'<div class="warning-box">{chat["response"]}</div>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<div class="safe-box">{chat["response"]}</div>', unsafe_allow_html=True)
                    
                    st.markdown("---")
    
    # TAB 2: Visual Translator
    with tab2:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 📸 Visual Translator")
        st.markdown("Translate signs, menus, and notices in real-time")
        st.markdown('</div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns([1, 1])
        
        with col1:
            source_lang = st.selectbox(
                "Source Language",
                [("Hindi", "hi"), ("Thai", "th"), ("Spanish", "es"), ("Portuguese", "pt")],
                format_func=lambda x: x[0]
            )[1]
        
        with col2:
            target_lang = st.selectbox(
                "Target Language",
                [("English", "en"), ("Spanish", "es"), ("French", "fr")],
                format_func=lambda x: x[0]
            )[1]
        
        uploaded_file = st.file_uploader(
            "Upload an image of text (sign, menu, notice)",
            type=['png', 'jpg', 'jpeg']
        )
        
        if uploaded_file:
            image = Image.open(uploaded_file)
            
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("#### Original Image")
                st.image(image, use_container_width=True)
            
            if st.button("🔤 Translate Image", use_container_width=True):
                with st.spinner("Extracting and translating text..."):
                    # Note: This requires numpy, add: import numpy as np
                    try:
                        import numpy as np
                        translated_img, translations = translate_image_text(image, source_lang, target_lang)
                        
                        with col2:
                            st.markdown("#### Translated Image")
                            st.image(translated_img, use_container_width=True)
                        
                        if translations:
                            st.success(f"✅ Found and translated {len(translations)} text blocks")
                            with st.expander("📝 View Translation Details"):
                                for i, trans in enumerate(translations, 1):
                                    st.markdown(f"**{i}.** {trans['original']} → **{trans['translated']}** (confidence: {trans['confidence']:.2%})")
                        else:
                            st.warning("No text detected in image. Try a clearer photo.")
                    except ImportError:
                        st.error("Please install required packages: `pip install numpy easyocr googletrans==4.0.0rc1 Pillow`")
                    except Exception as e:
                        st.error(f"Translation error: {str(e)}")
    
    # TAB 3: Voice Bridge
    with tab3:
        st.markdown('<div class="feature-card">', unsafe_allow_html=True)
        st.markdown("### 🎤 Voice Communication Bridge")
        st.markdown("Speak and translate in real-time for emergency communication")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Emergency phrases
        st.markdown("### 🚨 Quick Emergency Phrases")
        
        emergency_phrases = {
            "India": [
                ("Help!", "Madad karo!", "hi"),
                ("Call police!", "Police bulao!", "hi"),
                ("I need a doctor", "Mujhe doctor chahiye", "hi"),
                ("Leave me alone!", "Mujhe akela chhod do!", "hi"),
                ("Where is hospital?", "Hospital kahan hai?", "hi")
            ],
            "Thailand": [
                ("Help!", "Chuay duay!", "th"),
                ("Call police!", "Riak tamruat!", "th"),
                ("I need a doctor", "Chan tong kan mor", "th"),
                ("Where is hospital?", "Rong phayaban yoo thi nai?", "th")
            ],
            "Mexico": [
                ("Help!", "¡Ayuda!", "es"),
                ("Call police!", "¡Llama a la policía!", "es"),
                ("I need a doctor", "Necesito un médico", "es"),
                ("Where is hospital?", "¿Dónde está el hospital?", "es")
            ],
            "Brazil": [
                ("Help!", "Socorro!", "pt"),
                ("Call police!", "Chame a polícia!", "pt"),
                ("I need a doctor", "Preciso de um médico", "pt"),
                ("Where is hospital?", "Onde fica o hospital?", "pt")
            ],
            "USA": [
                ("I need help", "I need help", "en"),
                ("Call 911", "Call 911", "en"),
                ("Where is hospital?", "Where is the nearest hospital?", "en")
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
                        st.success(f"**{english}**\n\n*{local}*")
        
        st.markdown("---")
        st.markdown("### 🎙️ Real-time Voice Translation")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("#### Speak in English")
            english_text = st.text_area("Or type your message:", placeholder="I need directions to my hotel")
            
            if st.button("🔊 Translate to Local Language"):
                if english_text:
                    # Map country to language code
                    lang_map = {
                        "India": "hi",
                        "Thailand": "th",
                        "Mexico": "es",
                        "Brazil": "pt",
                        "USA": "en"
                    }
                    
                    target = lang_map.get(country, "en")
                    
                    with st.spinner("Translating..."):
                        try:
                            translator = Translator()
                            translated = translator.translate(english_text, src='en', dest=target)
                            
                            st.success(f"**Translation:** {translated.text}")
                            
                            audio_file = text_to_speech(translated.text, target)
                            if audio_file:
                                st.audio(audio_file)
                        except Exception as e:
                            st.error(f"Translation error: {str(e)}")
        
        with col2:
            st.markdown("#### Local Person Speaks")
            st.info("🎤 Record audio feature coming soon!\n\nFor now, you can type the local language text below:")
            
            local_text = st.text_area("Type local language:", placeholder="स्टेशन कहाँ है?")
            
            if st.button("🔊 Translate to English"):
                if local_text:
                    lang_map = {
                        "India": "hi",
                        "Thailand": "th",
                        "Mexico": "es",
                        "Brazil": "pt",
                        "USA": "en"
                    }
                    
                    source = lang_map.get(country, "en")
                    
                    with st.spinner("Translating..."):
                        try:
                            translator = Translator()
                            translated = translator.translate(local_text, src=source, dest='en')
                            
                            st.success(f"**Translation:** {translated.text}")
                            
                            audio_file = text_to_speech(translated.text, 'en')
                            if audio_file:
                                st.audio(audio_file)
                        except Exception as e:
                            st.error(f"Translation error: {str(e)}")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666; padding: 2rem;'>
        <p><strong>SafeWander</strong> - Built for VisaVerse AI Hackathon</p>
        <p>Stay safe, travel fearlessly 🌍</p>
        <p style='font-size: 0.9rem;'>⚠️ This is an AI-powered tool. Always use official emergency services when in danger.</p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()

