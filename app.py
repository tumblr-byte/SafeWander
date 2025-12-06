import streamlit as st
import json
import os
from groq import Groq
from PIL import Image, ImageDraw, ImageFont
import easyocr
from deep_translator import GoogleTranslator
from gtts import gTTS
import tempfile
import io
import numpy as np
from audiorecorder import audiorecorder
from datetime import datetime

# Page config
st.set_page_config(
    page_title="SafeWander - AI Travel Safety",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    .app-title {
        font-size: 2.5rem;
        font-weight: 700;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0;
        text-align: center;
    }
    
    .subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 3rem;
        font-weight: 500;
    }
    
    /* Chat Container */
    .chat-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 20px;
        padding: 2rem;
        max-height: 500px;
        overflow-y: auto;
        margin: 2rem 0;
        box-shadow: 0 8px 24px rgba(0,0,0,0.12);
    }
    
    /* Chat Messages */
    .chat-message {
        display: flex;
        margin: 1.5rem 0;
        animation: slideIn 0.3s ease-out;
    }
    
    @keyframes slideIn {
        from {
            opacity: 0;
            transform: translateY(10px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .chat-message.tourist {
        justify-content: flex-end;
    }
    
    .chat-message.local {
        justify-content: flex-start;
    }
    
    .message-bubble {
        max-width: 70%;
        padding: 1.2rem 1.5rem;
        border-radius: 20px;
        position: relative;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .message-bubble.tourist {
        background: linear-gradient(135deg, #3b82f6 0%, #2563eb 100%);
        color: white;
        border-bottom-right-radius: 5px;
    }
    
    .message-bubble.local {
        background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%);
        color: white;
        border-bottom-left-radius: 5px;
    }
    
    .message-header {
        display: flex;
        align-items: center;
        gap: 0.5rem;
        margin-bottom: 0.5rem;
        font-weight: 700;
        font-size: 0.9rem;
        opacity: 0.9;
    }
    
    .message-original {
        font-size: 1.1rem;
        font-weight: 600;
        margin-bottom: 0.8rem;
        line-height: 1.5;
    }
    
    .message-translation {
        font-size: 0.95rem;
        padding-top: 0.8rem;
        border-top: 1px solid rgba(255,255,255,0.3);
        font-style: italic;
        opacity: 0.95;
    }
    
    .message-time {
        font-size: 0.75rem;
        margin-top: 0.5rem;
        opacity: 0.7;
    }
    
    /* Input sections */
    .input-section {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1rem 0;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
        border: 2px solid #e2e8f0;
    }
    
    .input-section.tourist {
        border-left: 6px solid #3b82f6;
    }
    
    .input-section.local {
        border-left: 6px solid #8b5cf6;
    }
    
    /* Other styles */
    .threat-high {
        background: linear-gradient(135deg, #dc2626 0%, #991b1b 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        display: inline-block;
        margin: 1rem 0;
    }
    
    .threat-medium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        display: inline-block;
        margin: 1rem 0;
    }
    
    .threat-low {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
        padding: 0.5rem 1.5rem;
        border-radius: 25px;
        font-weight: 700;
        display: inline-block;
        margin: 1rem 0;
    }
    
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
    
    .feature-box {
        background: white;
        padding: 2rem;
        border-radius: 16px;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.1);
        border: 1px solid #e2e8f0;
        margin-bottom: 2rem;
    }
    
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
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'chat_history' not in st.session_state:
    st.session_state.chat_history = []
if 'current_country' not in st.session_state:
    st.session_state.current_country = "India"
if 'voice_messages' not in st.session_state:
    st.session_state.voice_messages = []
if 'tourist_mode' not in st.session_state:
    st.session_state.tourist_mode = "voice"
if 'local_mode' not in st.session_state:
    st.session_state.local_mode = "voice"

@st.cache_data
def load_safety_data():
    if os.path.exists("dataset.json"):
        with open("dataset.json", "r") as f:
            return json.load(f)
    return {"countries": ["India", "Thailand", "Mexico", "USA", "Brazil"]}

def init_groq():
    try:
        api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
        if api_key:
            return Groq(api_key=api_key)
    except Exception as e:
        st.warning(f"⚠️ Groq unavailable: {str(e)}")
    return None

def search_safety_data(query, country, data):
    query_lower = query.lower()
    results = []
    
    for scam in data.get("transport_scams", []):
        if scam.get("country") == country:
            if any(word in query_lower for word in ["taxi", "driver", "uber", "transport", "price", "fare", "scam"]):
                results.append({"type": "transport_scam", "data": scam})
    
    emergency = data.get("emergency_numbers", {}).get(country, {})
    if emergency:
        results.append({"type": "emergency", "data": emergency})
    
    return results

def get_ai_advice(query, country, groq_client, safety_data):
    relevant_info = search_safety_data(query, country, safety_data)
    
    context = f"User in {country} asks: {query}\n\n"
    for item in relevant_info[:3]:
        if item["type"] == "transport_scam":
            data = item["data"]
            context += f"Normal: {data.get('normal_rate')}, Scam: {data.get('scam_rate')}\n"
    
    system_prompt = """Respond in HTML format:
<div class="threat-[high/medium/low]">🚨 THREAT: [LEVEL]</div>
<div class="quick-answer"><strong>💡 Answer:</strong><br/>[2 sentences]</div>
<div class="action-steps"><strong>✅ Actions:</strong><ol><li>[Action 1]</li><li>[Action 2]</li></ol></div>
<div class="emergency-alert"><strong>🆘 Emergency:</strong> [Numbers]</div>"""
    
    try:
        if groq_client:
            chat = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": context}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.5,
                max_tokens=400
            )
            return chat.choices[0].message.content
        else:
            return f'<div class="threat-medium">🚨 THREAT: MEDIUM</div><div class="quick-answer">Verify prices in {country}.</div>'
    except Exception as e:
        return f"<div class='quick-answer'>Error: {str(e)}</div>"

def translate_image_text(image, source_lang='hi', target_lang='en'):
    try:
        reader = easyocr.Reader([source_lang, 'en'], gpu=False)
        translator = GoogleTranslator(source=source_lang, target=target_lang)
        
        img_array = np.array(image) if isinstance(image, Image.Image) else image
        results = reader.readtext(img_array)
        
        if not results:
            return image, []
        
        translated_img = image.copy() if isinstance(image, Image.Image) else Image.fromarray(img_array)
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
                
                translations.append({"original": text, "translated": translated_text})
        
        return translated_img, translations
    except Exception as e:
        st.error(f"Error: {str(e)}")
        return image, []

def text_to_speech(text, lang='en'):
    try:
        tts = gTTS(text=text, lang=lang, slow=False)
        fp = tempfile.NamedTemporaryFile(delete=False, suffix='.mp3')
        tts.save(fp.name)
        return fp.name
    except:
        return None

def transcribe_audio(audio_bytes, language='en'):
    try:
        groq_client = init_groq()
        if not groq_client:
            return "⚠️ Voice unavailable"
        
        with tempfile.NamedTemporaryFile(delete=False, suffix='.wav') as fp:
            fp.write(audio_bytes)
            temp_path = fp.name
        
        with open(temp_path, 'rb') as audio_file:
            transcription = groq_client.audio.transcriptions.create(
                file=audio_file,
                model="whisper-large-v3",
                language=language
            )
        
        os.unlink(temp_path)
        return transcription.text
    except Exception as e:
        return f"❌ Error: {str(e)}"

def add_message(speaker, original_text, translated_text, original_lang, translated_lang):
    message = {
        "speaker": speaker,
        "original": original_text,
        "translated": translated_text,
        "original_lang": original_lang,
        "translated_lang": translated_lang,
        "time": datetime.now().strftime("%I:%M %p"),
        "audio_file": text_to_speech(translated_text, translated_lang)
    }
    st.session_state.voice_messages.append(message)

def main():
    st.markdown('<h1 class="app-title"><i class="fas fa-shield-alt"></i> SafeWander</h1>', unsafe_allow_html=True)
    st.markdown('<p class="subtitle">AI-Powered Travel Safety Companion</p>', unsafe_allow_html=True)
    
    safety_data = load_safety_data()
    groq_client = init_groq()
    
    lang_map = {"India": "hi", "Thailand": "th", "Mexico": "es", "Brazil": "pt", "USA": "en"}
    
    with st.sidebar:
        st.markdown("### <i class='fas fa-map-marker-alt'></i> Location", unsafe_allow_html=True)
        country = st.selectbox("Country", ["India", "Thailand", "Mexico", "USA", "Brazil"], label_visibility="collapsed")
        st.session_state.current_country = country
        local_lang = lang_map.get(country, "hi")
        
        st.markdown("---")
        st.markdown("### <i class='fas fa-phone-alt'></i> Emergency", unsafe_allow_html=True)
        emergency_nums = safety_data.get("emergency_numbers", {}).get(country, {})
        for service, number in emergency_nums.items():
            st.markdown(f'<div class="emergency-box"><strong>{service.title()}</strong><br/>{number}</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        if st.button("🗑️ Clear Chat", use_container_width=True):
            st.session_state.voice_messages = []
            st.rerun()
    
    tab1, tab2, tab3 = st.tabs(["🤖 AI Advisor", "📸 Translator", "💬 Voice Chat"])
    
    # TAB 1: AI Advisor
    with tab1:
        st.markdown('<div class="feature-box"><h4><i class="fas fa-robot"></i> AI Safety Advisor</h4></div>', unsafe_allow_html=True)
        
        user_query = st.text_area("Describe your situation:", placeholder="E.g., Driver wants ₹800 for 5km", height=100)
        
        if st.button("Get Advice", use_container_width=True):
            if user_query:
                with st.spinner("Analyzing..."):
                    response = get_ai_advice(user_query, country, groq_client, safety_data)
                    st.session_state.chat_history.append({"query": user_query, "response": response, "country": country})
        
        if st.session_state.chat_history:
            st.markdown("---")
            for chat in reversed(st.session_state.chat_history[-2:]):
                st.markdown(f"**Question ({chat['country']}):** *{chat['query']}*")
                st.markdown(f'<div class="response-card">{chat["response"]}</div>', unsafe_allow_html=True)
    
    # TAB 2: Translator
    with tab2:
        st.markdown('<div class="feature-box"><h4><i class="fas fa-language"></i> Visual Translator</h4></div>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        with col1:
            source_lang = st.selectbox("From:", [("Hindi", "hi"), ("Thai", "th"), ("Spanish", "es")], format_func=lambda x: x[0])[1]
        with col2:
            st.selectbox("To:", ["English"], disabled=True)
        
        uploaded_file = st.file_uploader("Upload image", type=['png', 'jpg', 'jpeg'])
        
        if uploaded_file:
            image = Image.open(uploaded_file).convert('RGB')
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Original**")
                st.image(image, use_column_width=True)
            
            if st.button("🔤 Translate", use_container_width=True):
                with st.spinner("Translating..."):
                    translated_img, translations = translate_image_text(image, source_lang, 'en')
                    with col2:
                        st.markdown("**Translated**")
                        st.image(translated_img, use_column_width=True)
                    if translations:
                        st.success(f"✅ Translated {len(translations)} sections")
    
    # TAB 3: Voice Chat
    with tab3:
        st.markdown('<div class="feature-box"><h4><i class="fas fa-comments"></i> Voice Chat</h4>', unsafe_allow_html=True)
        st.markdown(f"**English** ↔ **{country}**</div>", unsafe_allow_html=True)
        
        # Display chat
        if st.session_state.voice_messages:
            st.markdown('<div class="chat-container">', unsafe_allow_html=True)
            for msg in st.session_state.voice_messages:
                speaker_class = "tourist" if msg["speaker"] == "Tourist" else "local"
                icon = "fa-user" if msg["speaker"] == "Tourist" else "fa-user-tie"
                
                st.markdown(f"""
                <div class="chat-message {speaker_class}">
                    <div class="message-bubble {speaker_class}">
                        <div class="message-header"><i class="fas {icon}"></i> {msg["speaker"]}</div>
                        <div class="message-original">{msg["original"]}</div>
                        <div class="message-translation">📝 {msg["translated"]}</div>
                        <div class="message-time">⏰ {msg["time"]}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                if msg == st.session_state.voice_messages[-1] and msg["audio_file"]:
                    st.audio(msg["audio_file"])
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.info("💬 No messages yet. Start chatting!")
        
        st.markdown("---")
        
        col1, col2 = st.columns(2)
        
        # TOURIST SIDE
        with col1:
            st.markdown('<div class="input-section tourist">', unsafe_allow_html=True)
            st.markdown("### <i class='fas fa-user'></i> Tourist (English)")
            
            t_col1, t_col2 = st.columns(2)
            with t_col1:
                if st.button("🎤 Voice", key="t_v", use_container_width=True):
                    st.session_state.tourist_mode = "voice"
            with t_col2:
                if st.button("⌨️ Text", key="t_t", use_container_width=True):
                    st.session_state.tourist_mode = "text"
            
            mode = st.session_state.tourist_mode
            st.info(f"**Mode:** {'🎤 Voice' if mode == 'voice' else '⌨️ Text'}")
            
            if mode == "voice":
                st.write("**Record:**")
                t_audio = audiorecorder("🔴 Start", "⏹️ Stop", key="t_rec")
                
                if len(t_audio) > 0:
                    st.audio(t_audio.export().read())
                    
                    if st.button("📤 Send", key="send_t", use_container_width=True, type="primary"):
                        with st.spinner("Processing..."):
                            audio_bytes = t_audio.export().read()
                            original = transcribe_audio(audio_bytes, 'en')
                            
                            if original and not original.startswith(("❌", "⚠️")):
                                try:
                                    translator = GoogleTranslator(source='en', target=local_lang)
                                    translated = translator.translate(original)
                                    add_message("Tourist", original, translated, 'en', local_lang)
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Translation failed: {str(e)}")
                            else:
                                st.error("Transcription failed!")
            else:
                t_text = st.text_area("Type:", key="t_txt", height=100)
                if st.button("📤 Send", key="send_t_txt", use_container_width=True, type="primary"):
                    if t_text.strip():
                        with st.spinner("Translating..."):
                            try:
                                translator = GoogleTranslator(source='en', target=local_lang)
                                translated = translator.translate(t_text)
                                add_message("Tourist", t_text, translated, 'en', local_lang)
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # LOCAL SIDE
        with col2:
            st.markdown('<div class="input-section local">', unsafe_allow_html=True)
            st.markdown(f"### <i class='fas fa-user-tie'></i> Local ({country})")
            
            l_col1, l_col2 = st.columns(2)
            with l_col1:
                if st.button("🎤 Voice", key="l_v", use_container_width=True):
                    st.session_state.local_mode = "voice"
            with l_col2:
                if st.button("⌨️ Text", key="l_t", use_container_width=True):
                    st.session_state.local_mode = "text"
            
            mode = st.session_state.local_mode
            st.info(f"**Mode:** {'🎤 Voice' if mode == 'voice' else '⌨️ Text'}")
            
            if mode == "voice":
                st.write("**Record:**")
                l_audio = audiorecorder("🔴 Start", "⏹️ Stop", key="l_rec")
                
                if len(l_audio) > 0:
                    st.audio(l_audio.export().read())
                    
                    if st.button("📤 Send", key="send_l", use_container_width=True, type="primary"):
                        with st.spinner("Processing..."):
                            audio_bytes = l_audio.export().read()
                            original = transcribe_audio(audio_bytes, local_lang)
                            
                            if original and not original.startswith(("❌", "⚠️")):
                                try:
                                    translator = GoogleTranslator(source=local_lang, target='en')
                                    translated = translator.translate(original)
                                    add_message("Local", original, translated, local_lang, 'en')
                                    st.rerun()
                                except Exception as e:
                                    st.error(f"Translation failed: {str(e)}")
                            else:
                                st.error("Transcription failed!")
            else:
                l_text = st.text_area(f"Type in {country}:", key="l_txt", height=100)
                if st.button("📤 Send", key="send_l_txt", use_container_width=True, type="primary"):
                    if l_text.strip():
                        with st.spinner("Translating..."):
                            try:
                                translator = GoogleTranslator(source=local_lang, target='en')
                                translated = translator.translate(l_text)
                                add_message("Local", l_text, translated, local_lang, 'en')
                                st.rerun()
                            except Exception as e:
                                st.error(f"Failed: {str(e)}")
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        st.info("💡 **Tip:** Choose Voice or Text mode, then send your message!")
    
    st.markdown("---")
    st.markdown("<div style='text-align:center;color:#94a3b8;'><strong>SafeWander</strong> - Stay Safe 🌍</div>", unsafe_allow_html=True)

if __name__ == "__main__":
    main()
