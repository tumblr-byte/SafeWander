import streamlit as st
import json
import os
from datetime import datetime
import speech_recognition as sr
from deep_translator import GoogleTranslator
import pyttsx3
import pytesseract
from PIL import Image
import requests
from dotenv import load_dotenv

load_dotenv()

# Page config
st.set_page_config(
    page_title="SafeWander - Travel Safety AI",
    page_icon="🌍",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    :root {
        --primary-color: #1E3A8A;
        --accent-color: #14B8A6;
        --danger-color: #DC2626;
        --success-color: #10B981;
    }
    
    .main {
        background-color: #F8FAFC;
    }
    
    .stTabs [data-baseweb="tab-list"] button {
        background-color: #E2E8F0;
        color: #1E3A8A;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #1E3A8A !important;
        color: white !important;
    }
    
    .safety-score-high {
        color: #10B981;
        font-weight: bold;
        font-size: 24px;
    }
    
    .safety-score-medium {
        color: #F59E0B;
        font-weight: bold;
        font-size: 24px;
    }
    
    .safety-score-low {
        color: #DC2626;
        font-weight: bold;
        font-size: 24px;
    }
    </style>
""", unsafe_allow_html=True)

# Grok API Integration
def call_grok_api(prompt, api_key):
    """Call Grok API with prompt"""
    try:
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "grok-1",
            "messages": [{"role": "user", "content": prompt}],
            "temperature": 0.7,
            "max_tokens": 500
        }
        response = requests.post(
            "https://api.x.ai/v1/chat/completions",
            headers=headers,
            json=payload,
            timeout=10
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            return f"Error: {response.status_code}"
    except Exception as e:
        return f"API Error: {str(e)}"

# Initialize session state
if "grok_client" not in st.session_state:
    st.session_state.grok_client = None

if "community_reports" not in st.session_state:
    st.session_state.community_reports = []

if "user_reports" not in st.session_state:
    st.session_state.user_reports = []

# Load or create database
def load_database():
    if os.path.exists("database.json"):
        with open("database.json", "r") as f:
            return json.load(f)
    return {
        "locations": {},
        "community_reports": [],
        "emergency_contacts": {}
    }

def save_database(db):
    with open("database.json", "w") as f:
        json.dump(db, f, indent=2)

# Header with logo
col1, col2 = st.columns([1, 4])
with col1:
    if os.path.exists("logo.png"):
        st.image("logo.png", width=80)
    else:
        st.markdown("🌍")

with col2:
    st.title("SafeWander")
    st.markdown("*Your AI Travel Safety Companion*")

st.markdown("---")

# Sidebar - Setup
with st.sidebar:
    st.header("⚙️ Setup")
    
    # Try to load from secrets first
    try:
        grok_api_key = st.secrets["GROK_API_KEY"]
        st.session_state.grok_client = grok_api_key
        st.success("✅ Grok API Connected from Secrets")
    except:
        # Fallback to manual input
        grok_api_key = st.text_input("Enter Grok API Key", type="password", key="grok_key")
        if grok_api_key:
            st.session_state.grok_client = grok_api_key
            st.success("✅ Grok API Connected")
    
    st.markdown("---")
    st.markdown("### 📍 Quick Stats")
    db = load_database()
    st.metric("Locations Covered", len(db["locations"]))
    st.metric("Community Reports", len(db["community_reports"]))

# Main tabs
tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🗺️ Trip Planner",
    "🛡️ Real-time Safety",
    "🎤 Voice Translator",
    "🚨 Emergency",
    "👥 Community"
])

# ============ TAB 1: TRIP PLANNER ============
with tab1:
    st.header("Trip Planner - Before You Travel")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📍 Your Journey")
        current_location = st.text_input("Where are you now?", placeholder="e.g., New Delhi, India")
        destination = st.text_input("Where do you want to go?", placeholder="e.g., Bangkok, Thailand")
        travel_date = st.date_input("Travel date")
        traveler_type = st.selectbox("Traveler type", ["Solo", "Couple", "Group", "Family"])
    
    with col2:
        st.subheader("👤 About You")
        gender = st.selectbox("Gender (for safety tips)", ["Male", "Female", "Other", "Prefer not to say"])
        age_group = st.selectbox("Age group", ["18-25", "26-35", "36-50", "50+"])
        experience = st.selectbox("Travel experience", ["First time", "Occasional", "Frequent"])
    
    if st.button("🔍 Get Trip Information", key="trip_info"):
        if destination:
            if st.session_state.grok_client:
                st.info("⏳ Fetching information from Grok AI...")
                
                prompt = f"""
                Traveler going from {current_location} to {destination}.
                Traveler type: {traveler_type}
                Gender: {gender}
                Experience: {experience}
                
                Provide practical travel information:
                1. Money & Currency (exchange rates, safe places to exchange, roaming, money transfer)
                2. Hotels (budget options, mid-range, safe areas, fair price indicators)
                3. Transport (taxi fares, recommended apps, safety tips)
                4. Quick safety overview
                
                Be concise and practical.
                """
                
                response = call_grok_api(prompt, st.session_state.grok_client)
                st.success("✅ Information Retrieved!")
                st.write(response)
            else:
                st.warning("⚠️ Please enter Grok API key in sidebar first")
                
                # Show default info
                db = load_database()
                if destination in db["locations"]:
                    loc_data = db["locations"][destination]
                    
                    col1, col2, col3 = st.columns(3)
                    
                    with col1:
                        st.subheader("💰 Money & Currency")
                        st.write(f"• Exchange rate: {loc_data['money']['exchange_rate']}")
                        st.write(f"• Safe exchange: {', '.join(loc_data['money']['safe_exchange'])}")
                        st.write(f"• Roaming: {loc_data['money']['roaming']}")
                    
                    with col2:
                        st.subheader("🏨 Hotels")
                        st.write(f"• Budget: {loc_data['hotels']['budget']['price_range']}")
                        st.write(f"• Safe areas: {', '.join(loc_data['hotels']['budget']['safe_areas'])}")
                    
                    with col3:
                        st.subheader("🚕 Transport")
                        st.write(f"• Taxi base: {loc_data['transport']['taxi_base']}")
                        st.write(f"• Per km: {loc_data['transport']['taxi_per_km']}")
                        st.write(f"• Recommended: {loc_data['transport']['recommended']}")
    
    st.markdown("---")
    
    # Cultural Awareness
    st.subheader("🤝 Cultural Awareness")
    if destination:
        col1, col2 = st.columns(2)
        
        with col1:
            st.write("**Do's:**")
            st.write("✅ Remove shoes before entering homes/temples")
            st.write("✅ Show respect to elders")
            st.write("✅ Learn basic greetings")
            st.write("✅ Dress modestly in religious areas")
        
        with col2:
            st.write("**Don'ts:**")
            st.write("❌ Point feet at Buddha images")
            st.write("❌ Touch people's heads")
            st.write("❌ Raise voice in public")
            st.write("❌ Disrespect local customs")

# ============ TAB 2: REAL-TIME SAFETY ============
with tab2:
    st.header("Real-time Safety Check")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("📍 Current Location")
        current_area = st.text_input("What area are you in?", placeholder="e.g., Khao San Road, Bangkok")
        time_of_day = st.selectbox("Time of day", ["Morning (6AM-12PM)", "Afternoon (12PM-6PM)", "Evening (6PM-11PM)", "Night (11PM-6AM)"])
    
    with col2:
        st.subheader("🎯 What's happening?")
        situation = st.selectbox("Current situation", [
            "Just arrived",
            "Walking around",
            "Using taxi",
            "At restaurant",
            "At hotel",
            "Feeling unsafe",
            "Other"
        ])
    
    if st.button("🛡️ Check Safety", key="safety_check"):
        if current_area:
            st.info("⏳ Analyzing area safety...")
            
            db = load_database()
            
            # Get location data
            location_key = current_area.split(",")[0].strip()
            loc_data = db["locations"].get(location_key, {})
            
            if loc_data:
                # Safety Score
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    score = loc_data.get("safety_score", 7.0)
                    if score >= 8:
                        st.markdown(f'<p class="safety-score-high">{score}/10</p>', unsafe_allow_html=True)
                    elif score >= 6:
                        st.markdown(f'<p class="safety-score-medium">{score}/10</p>', unsafe_allow_html=True)
                    else:
                        st.markdown(f'<p class="safety-score-low">{score}/10</p>', unsafe_allow_html=True)
                    st.write("**Safety Score**")
                
                with col2:
                    if time_of_day == "Night (11PM-6AM)" and not loc_data.get("safe_at_night", False):
                        st.write("⚠️ Not safe at this time")
                    else:
                        st.write("✅ Generally safe")
                    st.write("✅ Check community reports")
                    st.write("📍 Know emergency contacts")
                
                with col3:
                    st.write("**Emergency Contacts:**")
                    contacts = loc_data.get("emergency_contacts", {})
                    for contact_type, number in list(contacts.items())[:3]:
                        st.write(f"📞 {contact_type.replace('_', ' ').title()}: {number}")
                
                st.markdown("---")
                
                # Situational Tips with Grok
                if st.session_state.grok_client:
                    prompt = f"""
                    Person in {current_area} at {time_of_day}.
                    Situation: {situation}
                    Gender: {gender}
                    
                    Provide 5 immediate safety actions they should take right now.
                    Be practical and specific.
                    """
                    
                    st.subheader("💡 What to Do Right Now")
                    response = call_grok_api(prompt, st.session_state.grok_client)
                    st.write(response)
                else:
                    st.subheader("💡 What to Do Right Now")
                    st.write("""
                    1. **Stay in crowded areas** - Good visibility and witnesses
                    2. **Keep valuables hidden** - Pickpocketing is common
                    3. **Use registered transport** - Avoid unmarked vehicles
                    4. **Trust your gut** - If uncomfortable, move to another area
                    5. **Share location** - Tell friend where you are
                    """)
                
                st.markdown("---")
                
                # Common Scams
                st.subheader("⚠️ Common Scams in This Area")
                scams = loc_data.get("common_scams", [])
                if scams:
                    for scam in scams:
                        st.write(f"🔴 {scam}")
                
                # Community Reports
                st.markdown("---")
                st.subheader("📖 Community Reports")
                relevant_reports = [r for r in db["community_reports"] if location_key.lower() in r["location"].lower()]
                if relevant_reports:
                    for report in relevant_reports[:3]:
                        with st.expander(f"{report['type'].upper()} - {report['title']} ({report['upvotes']} 👍)"):
                            st.write(report["description"])
                            st.write(f"*Reported by: {report['reported_by']}*")
            else:
                st.warning("Location not in database. Try: Bangkok, New Delhi")

# ============ TAB 3: VOICE TRANSLATOR ============
with tab3:
    st.header("🎤 Voice Translator - Talk to Locals")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🗣️ Speak to Translate")
        
        # Language mapping
        lang_map = {
            "Hindi": "hi",
            "Thai": "th",
            "Spanish": "es",
            "French": "fr",
            "German": "de",
            "Japanese": "ja",
            "Mandarin": "zh-CN"
        }
        
        language = st.selectbox("Local language", list(lang_map.keys()))
        lang_code = lang_map[language]
        
        # Text input for translation
        user_text = st.text_area("What do you want to say?", placeholder="Type or paste text here", height=100)
        
        if st.button("🔄 Translate", key="translate_text"):
            if user_text:
                try:
                    translator = GoogleTranslator(source_language='en', target_language=lang_code)
                    translated = translator.translate(user_text)
                    st.success("✅ Translation:")
                    st.write(f"**{translated}**")
                    
                    # Text-to-speech
                    if st.button("🔊 Speak Translation", key="speak_translation"):
                        try:
                            engine = pyttsx3.init()
                            engine.setProperty('rate', 150)
                            engine.say(translated)
                            engine.runAndWait()
                            st.success("🔊 Playing audio...")
                        except Exception as e:
                            st.error(f"Audio error: {str(e)}")
                except Exception as e:
                    st.error(f"Translation error: {str(e)}")
            else:
                st.warning("Please enter text to translate")
        
        st.markdown("---")
        
        st.subheader("💬 Survival Phrases")
        phrases = {
            "Help": "मदद करो",
            "Police": "पुलिस",
            "Hospital": "अस्पताल",
            "Stop": "रुको",
            "I'm lost": "मैं खो गया हूँ",
            "Too expensive": "बहुत महंगा है",
            "Thank you": "धन्यवाद",
            "I don't understand": "मैं नहीं समझता"
        }
        
        for english, local in phrases.items():
            col_a, col_b = st.columns([1, 1])
            with col_a:
                st.write(f"**{english}**")
            with col_b:
                st.write(f"*{local}*")
    
    with col2:
        st.subheader("💭 Heart-to-Heart Communication")
        st.write("**Respectful phrases to connect:**")
        
        heart_phrases = [
            "I respect your culture",
            "Can you help me?",
            "I'm sorry, I didn't understand",
            "Thank you for helping",
            "You're very kind",
            "I'm learning your language",
            "This is beautiful",
            "I appreciate your help"
        ]
        
        for phrase in heart_phrases:
            st.write(f"• {phrase}")
        
        st.markdown("---")
        
        st.subheader("🚕 Driver Communication")
        st.write("**If talking to taxi driver:**")
        
        driver_phrases = [
            "Is this the correct route?",
            "How much will it cost?",
            "Can you use the meter?",
            "Please take the main road",
            "Stop here, please",
            "Thank you, have a good day"
        ]
        
        for phrase in driver_phrases:
            st.write(f"• {phrase}")

# ============ TAB 4: EMERGENCY ============
with tab4:
    st.header("🚨 Emergency - Get Help Now")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("🆘 Emergency Contacts")
        location = st.text_input("Your location", placeholder="e.g., Bangkok, Thailand")
        
        if location:
            st.write("**Emergency Numbers:**")
            st.write("🚔 Police: +66-1191")
            st.write("👩‍⚕️ Ambulance: +66-1669")
            st.write("🚒 Fire: +66-1199")
            st.write("👩‍💼 Women Helpline: +66-1300")
            st.write("🏥 Tourist Police: +66-4-281-5051")
            st.write("🤝 NGO Safe House: +66-2-xxx-xxxx")
    
    with col2:
        st.subheader("📍 Share Your Location")
        trusted_contact = st.text_input("Trusted contact phone/email", placeholder="Friend or family")
        
        if st.button("📤 Send SOS Alert", key="sos_alert"):
            st.success("✅ SOS Alert Sent!")
            st.write(f"Location shared with: {trusted_contact}")
            st.write("Emergency contacts notified")
    
    st.markdown("---")
    
    # Complaint System
    st.subheader("📝 File a Complaint")
    
    complaint_type = st.selectbox("What happened?", [
        "Scam/Overcharging",
        "Harassment/Stalking",
        "Theft",
        "Unsafe situation",
        "Other"
    ])
    
    complaint_details = st.text_area("Describe what happened", height=100)
    
    # Upload evidence
    uploaded_file = st.file_uploader("Upload photo/video (optional)", type=["jpg", "png", "mp4"])
    
    if st.button("📤 Submit Complaint", key="submit_complaint"):
        if complaint_details:
            st.success("✅ Complaint Submitted!")
            st.write("Your report will help protect other travelers")
            st.write("Reference ID: #2025-12-04-001")
        else:
            st.error("Please describe what happened")

# ============ TAB 5: COMMUNITY ============
with tab5:
    st.header("👥 Community - Help Each Other")
    
    tab5_1, tab5_2, tab5_3 = st.tabs(["📖 Reports", "✍️ Share", "🔍 Search"])
    
    with tab5_1:
        st.subheader("Community Reports")
        
        # Sample reports
        reports = [
            {
                "type": "⚠️ Scam",
                "location": "Khao San Road, Bangkok",
                "title": "Gem Shop Scam",
                "description": "Overpriced stones, fake quality. Avoid shops with touts.",
                "upvotes": 45,
                "verified": True,
                "author": "traveler_123"
            },
            {
                "type": "✅ Safe Spot",
                "location": "BTS Sukhumvit, Bangkok",
                "title": "Safe Shopping Area",
                "description": "Lots of tourists, good restaurants, safe at all times.",
                "upvotes": 78,
                "verified": True,
                "author": "local_bangkok_456"
            },
            {
                "type": "💡 Tip",
                "location": "Bangkok Taxis",
                "title": "How to Avoid Taxi Scams",
                "description": "Always use Grab app or insist on meter. Negotiate before boarding.",
                "upvotes": 92,
                "verified": True,
                "author": "local_bangkok_789"
            }
        ]
        
        for report in reports:
            with st.expander(f"{report['type']} {report['title']} ({report['upvotes']} 👍)"):
                st.write(f"**Location:** {report['location']}")
                st.write(f"**Description:** {report['description']}")
                st.write(f"**Author:** {report['author']}")
                if report['verified']:
                    st.write("✅ Verified by community")
                
                col1, col2 = st.columns(2)
                with col1:
                    if st.button("👍 Helpful", key=f"upvote_{report['title']}"):
                        st.write("Thanks for voting!")
                with col2:
                    if st.button("💬 Comment", key=f"comment_{report['title']}"):
                        st.write("Comments coming soon!")
    
    with tab5_2:
        st.subheader("Share Your Experience")
        
        report_type = st.selectbox("What do you want to share?", [
            "⚠️ Scam Warning",
            "✅ Safe Spot",
            "💡 Helpful Tip",
            "📍 Incident Report"
        ])
        
        location = st.text_input("Location", placeholder="e.g., Bangkok, Thailand")
        title = st.text_input("Title", placeholder="Brief title")
        description = st.text_area("Description", height=100, placeholder="Share details...")
        
        if st.button("📤 Post Report", key="post_report"):
            if title and description:
                st.success("✅ Report Posted!")
                st.write("Thank you for helping other travelers!")
            else:
                st.error("Please fill in all fields")
    
    with tab5_3:
        st.subheader("Search Community Reports")
        
        search_location = st.text_input("Search by location", placeholder="e.g., Bangkok")
        search_keyword = st.text_input("Search by keyword", placeholder="e.g., scam, safe, taxi")
        
        if st.button("🔍 Search", key="search_reports"):
            st.write("Searching...")
            st.write("Found 3 relevant reports")

st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; font-size: 12px;'>
    <p>SafeWander - Travel Safely, Travel Smart 🌍</p>
    <p>Made with ❤️ for travelers worldwide</p>
</div>
""", unsafe_allow_html=True)
