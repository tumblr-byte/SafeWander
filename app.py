import streamlit as st
import json
import os
from groq import Groq
from datetime import datetime
import streamlit.components.v1 as components
import base64

# Page config
st.set_page_config(
    page_title="SafeWander - AI Travel Safety Guardian",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Load logo as base64
def get_logo_base64():
    try:
        if os.path.exists("logo.png"):
            with open("logo.png", "rb") as f:
                return base64.b64encode(f.read()).decode()
    except:
        pass
    return None

LOGO_BASE64 = get_logo_base64()

# Custom CSS - Redesigned with Font Awesome, smaller fonts, better UX
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');
    
    * { 
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
    }
    
    .main { padding: 0 !important; }
    
    /* Navigation Bar */
    .navbar {
        background: white;
        padding: 0.8rem 1.5rem;
        display: flex;
        align-items: center;
        justify-content: space-between;
        box-shadow: 0 2px 10px rgba(0,0,0,0.08);
        position: sticky;
        top: 0;
        z-index: 1000;
        border-radius: 0 0 15px 15px;
        margin-bottom: 1rem;
    }
    
    .nav-brand {
        display: flex;
        align-items: center;
        gap: 0.8rem;
    }
    
    .nav-logo {
        height: 40px;
        width: auto;
    }
    
    .nav-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #667eea;
    }
    
    .nav-home {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.6rem 1rem;
        cursor: pointer;
        font-size: 0.9rem;
        font-weight: 600;
        display: flex;
        align-items: center;
        gap: 0.5rem;
        transition: all 0.2s ease;
    }
    
    .nav-home:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
    }
    
    /* Hero Section - Smaller */
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 1.5rem 1.5rem;
        text-align: center;
        border-radius: 15px;
        margin: 0 1rem 1.5rem 1rem;
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .hero-logo {
        height: 50px;
        margin-bottom: 0.5rem;
    }
    
    .hero-title {
        font-size: 1.8rem;
        font-weight: 700;
        margin-bottom: 0.3rem;
    }
    
    .hero-subtitle {
        font-size: 0.95rem;
        opacity: 0.9;
        font-weight: 400;
    }
    
    /* Profile Section */
    .quick-profile {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 20px rgba(0,0,0,0.1);
        margin: 1rem;
        max-width: 700px;
        margin-left: auto;
        margin-right: auto;
    }
    
    .profile-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 1rem;
        text-align: center;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    /* Feature Cards */
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1rem;
    }
    
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 1.2rem;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        transition: all 0.2s ease;
        cursor: pointer;
        border-left: 4px solid #667eea;
        text-align: center;
    }
    
    .feature-card:hover {
        transform: translateY(-3px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.25);
    }
    
    .card-icon {
        font-size: 1.8rem;
        color: #667eea;
        margin-bottom: 0.8rem;
    }
    
    .card-title {
        font-size: 1rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.3rem;
    }
    
    .card-desc {
        color: #64748b;
        font-size: 0.8rem;
        line-height: 1.4;
    }
    
    /* SOS Button */
    .sos-button {
        position: fixed;
        bottom: 20px;
        right: 20px;
        z-index: 9999;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
        50% { transform: scale(1.05); box-shadow: 0 0 0 15px rgba(239, 68, 68, 0); }
    }
    
    .sos-btn {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 65px;
        height: 65px;
        font-size: 1.2rem;
        font-weight: 700;
        cursor: pointer;
        box-shadow: 0 6px 20px rgba(239, 68, 68, 0.5);
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .sos-btn:hover {
        transform: scale(1.1);
    }
    
    /* Map Container */
    .map-container {
        background: white;
        border-radius: 15px;
        padding: 1rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        margin: 1rem;
    }
    
    .section-header {
        font-size: 1.1rem;
        font-weight: 600;
        color: #667eea;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    #map {
        height: 400px;
        border-radius: 12px;
        border: 2px solid #667eea;
    }
    
    /* Emergency Modal */
    .emergency-modal {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 15px 40px rgba(0,0,0,0.2);
        max-width: 500px;
        margin: 1rem auto;
    }
    
    .emergency-title {
        font-size: 1.4rem;
        font-weight: 700;
        color: #ef4444;
        text-align: center;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 0.5rem;
    }
    
    /* Phrase Cards */
    .phrase-card {
        background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
        border-radius: 12px;
        padding: 1rem;
        margin: 0.8rem 0;
        border-left: 4px solid #7c3aed;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .phrase-local {
        font-size: 1.1rem;
        font-weight: 700;
        color: #5b21b6;
    }
    
    .phrase-meaning {
        font-size: 0.85rem;
        color: #6d28d9;
    }
    
    .phrase-audio {
        background: #7c3aed;
        color: white;
        border: none;
        border-radius: 50%;
        width: 40px;
        height: 40px;
        cursor: pointer;
        font-size: 1rem;
        transition: all 0.2s;
        display: flex;
        align-items: center;
        justify-content: center;
    }
    
    .phrase-audio:hover {
        background: #5b21b6;
        transform: scale(1.1);
    }
    
    .phrase-audio:active {
        transform: scale(0.95);
    }
    
    /* Scam Checker */
    .scam-checker {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-radius: 15px;
        padding: 1.5rem;
        border-left: 4px solid #f59e0b;
        margin: 1rem;
    }
    
    .scam-title {
        font-size: 1.1rem;
        font-weight: 600;
        color: #92400e;
        margin-bottom: 0.8rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .price-check {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin-top: 1rem;
    }
    
    /* Alerts */
    .alert-danger {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 4px solid #ef4444;
        padding: 1rem;
        border-radius: 12px;
        color: #991b1b;
        font-size: 0.9rem;
        margin: 0.8rem 0;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 4px solid #10b981;
        padding: 1rem;
        border-radius: 12px;
        color: #065f46;
        font-size: 0.9rem;
        margin: 0.8rem 0;
    }
    
    /* Officer Card */
    .officer-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        margin: 0.8rem 0;
        box-shadow: 0 3px 12px rgba(0,0,0,0.08);
        display: flex;
        gap: 1rem;
        align-items: center;
    }
    
    .officer-photo {
        width: 60px;
        height: 60px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 1.5rem;
        color: white;
    }
    
    .officer-name {
        font-size: 1rem;
        font-weight: 600;
        color: #1e293b;
    }
    
    .officer-badge {
        color: #64748b;
        font-size: 0.8rem;
    }
    
    .eta-badge {
        background: #10b981;
        color: white;
        padding: 0.4rem 0.8rem;
        border-radius: 15px;
        font-weight: 600;
        font-size: 0.85rem;
    }
    
    /* Cultural Grid */
    .cultural-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
        gap: 1rem;
        margin: 1rem 0;
    }
    
    .culture-card {
        background: white;
        border-radius: 12px;
        padding: 1rem;
        box-shadow: 0 3px 12px rgba(0,0,0,0.06);
        border-top: 3px solid #667eea;
    }
    
    .culture-icon {
        font-size: 1.5rem;
        color: #667eea;
        margin-bottom: 0.5rem;
    }
    
    .culture-title {
        font-size: 0.95rem;
        font-weight: 600;
        color: #1e293b;
        margin-bottom: 0.3rem;
    }
    
    .culture-text {
        color: #64748b;
        font-size: 0.8rem;
        line-height: 1.5;
    }
    
    /* Buttons */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.6rem 1.5rem;
        border-radius: 25px;
        font-weight: 600;
        font-size: 0.9rem;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 6px 20px rgba(102, 126, 234, 0.4);
    }
    
    .stButton>button:active {
        transform: translateY(0);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Input styling */
    .stTextInput>div>div>input {
        border-radius: 10px;
        border: 2px solid #e2e8f0;
        font-size: 0.9rem;
    }
    
    .stTextInput>div>div>input:focus {
        border-color: #667eea;
        box-shadow: 0 0 0 3px rgba(102, 126, 234, 0.1);
    }
    
    .stSelectbox>div>div {
        border-radius: 10px;
    }
</style>
""", unsafe_allow_html=True)


# Initialize session state
if 'profile_complete' not in st.session_state:
    st.session_state.profile_complete = False
if 'profile' not in st.session_state:
    st.session_state.profile = {}
if 'sos_active' not in st.session_state:
    st.session_state.sos_active = False
if 'sos_reason' not in st.session_state:
    st.session_state.sos_reason = None
if 'active_feature' not in st.session_state:
    st.session_state.active_feature = None

# Load safety data
@st.cache_data
def load_safety_data():
    if os.path.exists("dataset.json"):
        with open("dataset.json", "r") as f:
            return json.load(f)
    return {
        "countries": ["India", "Thailand", "Mexico", "USA", "Brazil"],
        "transport_scams": [],
        "emergency_numbers": {}
    }

# Initialize Groq
def init_groq():
    try:
        api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
        if api_key:
            return Groq(api_key=api_key)
    except:
        pass
    return None

# Language codes for TTS
LANGUAGE_CODES = {
    'India': 'hi-IN',
    'Thailand': 'th-TH',
    'Mexico': 'es-MX',
    'USA': 'en-US',
    'Brazil': 'pt-BR'
}

# Destinations
DESTINATIONS = {
    "India": {
        "cities": ["Delhi", "Mumbai", "Bangalore", "Goa", "Jaipur", "Agra", "Kolkata", "Chennai", "Hyderabad", "Pune"],
        "coords": {"Delhi": [28.6139, 77.2090], "Mumbai": [19.0760, 72.8777], "Bangalore": [12.9716, 77.5946], 
                   "Goa": [15.2993, 74.1240], "Jaipur": [26.9124, 75.7873]}
    },
    "Thailand": {
        "cities": ["Bangkok", "Phuket", "Chiang Mai", "Pattaya", "Krabi"],
        "coords": {"Bangkok": [13.7563, 100.5018], "Phuket": [7.8804, 98.3923], "Chiang Mai": [18.7883, 98.9853]}
    },
    "Mexico": {
        "cities": ["Mexico City", "Cancun", "Playa del Carmen", "Guadalajara", "Oaxaca"],
        "coords": {"Mexico City": [19.4326, -99.1332], "Cancun": [21.1619, -86.8515]}
    },
    "USA": {
        "cities": ["New York", "Los Angeles", "Las Vegas", "Miami", "San Francisco", "Chicago", "Boston"],
        "coords": {"New York": [40.7128, -74.0060], "Los Angeles": [34.0522, -118.2437]}
    },
    "Brazil": {
        "cities": ["Rio de Janeiro", "São Paulo", "Salvador", "Brasília"],
        "coords": {"Rio de Janeiro": [-22.9068, -43.1729], "São Paulo": [-23.5505, -46.6333]}
    }
}

# Essential phrases by country
ESSENTIAL_PHRASES = {
    "India": [
        ("Namaste", "नमस्ते", "Hello/Greetings"),
        ("Dhanyavaad", "धन्यवाद", "Thank you"),
        ("Madad karo", "मदद करो", "Help me"),
        ("Police bulao", "पुलिस बुलाओ", "Call police"),
        ("Kitna hai", "कितना है", "How much?"),
        ("Bahut mehenga", "बहुत महंगा", "Too expensive"),
        ("Ruko", "रुको", "Stop"),
        ("Maaf karna", "माफ़ करना", "Sorry/Excuse me"),
        ("Kaha hai", "कहाँ है", "Where is?"),
        ("Hospital kaha hai", "अस्पताल कहाँ है", "Where is hospital?"),
        ("Nahi chahiye", "नहीं चाहिए", "Don't want"),
        ("Mujhe samajh nahi aaya", "मुझे समझ नहीं आया", "I don't understand"),
        ("Theek hai", "ठीक है", "It's okay/Alright"),
        ("Paani", "पानी", "Water"),
        ("Bhuk lagi hai", "भूख लगी है", "I'm hungry")
    ],
    "Thailand": [
        ("Sawasdee", "สวัสดี", "Hello"),
        ("Khob khun", "ขอบคุณ", "Thank you"),
        ("Chuay duay", "ช่วยด้วย", "Help!"),
        ("Tao rai", "เท่าไหร่", "How much?"),
        ("Paeng maak", "แพงมาก", "Too expensive"),
        ("Mai ao", "ไม่เอา", "Don't want"),
        ("Yut", "หยุด", "Stop"),
        ("Khor thot", "ขอโทษ", "Sorry"),
        ("Yuu tii nai", "อยู่ที่ไหน", "Where is?"),
        ("Tamruat", "ตำรวจ", "Police"),
        ("Rong phayaban", "โรงพยาบาล", "Hospital"),
        ("Mai khao jai", "ไม่เข้าใจ", "Don't understand"),
        ("Naam", "น้ำ", "Water"),
        ("Hiu khao", "หิวข้าว", "Hungry"),
        ("Kin aahan", "กินอาหาร", "Eat food")
    ],
    "Mexico": [
        ("Hola", "Hola", "Hello"),
        ("Gracias", "Gracias", "Thank you"),
        ("Ayuda", "¡Ayuda!", "Help!"),
        ("Cuanto cuesta", "¿Cuánto cuesta?", "How much?"),
        ("Muy caro", "Muy caro", "Too expensive"),
        ("No quiero", "No quiero", "Don't want"),
        ("Alto", "¡Alto!", "Stop!"),
        ("Lo siento", "Lo siento", "Sorry"),
        ("Donde esta", "¿Dónde está?", "Where is?"),
        ("Policia", "Policía", "Police"),
        ("Hospital", "Hospital", "Hospital"),
        ("No entiendo", "No entiendo", "Don't understand"),
        ("Agua", "Agua", "Water"),
        ("Tengo hambre", "Tengo hambre", "I'm hungry"),
        ("Bano", "Baño", "Bathroom")
    ],
    "USA": [
        ("Hello", "Hello", "Greeting"),
        ("Thank you", "Thank you", "Thanks"),
        ("Help", "Help!", "Emergency"),
        ("How much", "How much?", "Price"),
        ("Too expensive", "Too expensive", "Costly"),
        ("No thanks", "No thanks", "Decline"),
        ("Stop", "Stop", "Halt"),
        ("Excuse me", "Excuse me", "Attention"),
        ("Where is", "Where is?", "Location"),
        ("Call police", "Call police", "Emergency"),
        ("Hospital", "Hospital", "Medical"),
        ("I dont understand", "I don't understand", "Confusion"),
        ("Water", "Water", "Drink"),
        ("Restroom", "Restroom", "Bathroom"),
        ("Emergency", "Emergency", "Urgent help")
    ],
    "Brazil": [
        ("Ola", "Olá", "Hello"),
        ("Obrigado", "Obrigado/a", "Thank you"),
        ("Socorro", "Socorro!", "Help!"),
        ("Quanto custa", "Quanto custa?", "How much?"),
        ("Muito caro", "Muito caro", "Too expensive"),
        ("Nao quero", "Não quero", "Don't want"),
        ("Pare", "Pare!", "Stop!"),
        ("Desculpe", "Desculpe", "Sorry"),
        ("Onde fica", "Onde fica?", "Where is?"),
        ("Policia", "Polícia", "Police"),
        ("Hospital", "Hospital", "Hospital"),
        ("Nao entendo", "Não entendo", "Don't understand"),
        ("Agua", "Água", "Water"),
        ("Estou com fome", "Estou com fome", "I'm hungry"),
        ("Banheiro", "Banheiro", "Bathroom")
    ]
}

# Mock police data
POLICE_STATIONS = {
    "Delhi": [
        {"name": "Connaught Place Police Station", "lat": 28.6315, "lng": 77.2167, "distance": "1.2 km"},
        {"name": "India Gate Police Post", "lat": 28.6129, "lng": 77.2295, "distance": "2.5 km"},
        {"name": "Chandni Chowk Police Station", "lat": 28.6506, "lng": 77.2303, "distance": "3.8 km"}
    ],
    "Mumbai": [
        {"name": "Colaba Police Station", "lat": 18.9067, "lng": 72.8147, "distance": "1.5 km"},
        {"name": "Marine Drive Police Station", "lat": 18.9432, "lng": 72.8236, "distance": "2.1 km"}
    ],
    "Bangkok": [
        {"name": "Lumpini Police Station", "lat": 13.7308, "lng": 100.5418, "distance": "1.8 km"},
        {"name": "Sukhumvit Police Station", "lat": 13.7367, "lng": 100.5609, "distance": "2.3 km"}
    ]
}

MOCK_OFFICERS = [
    {"name": "Officer Priya Sharma", "badge": "DL-2847", "eta": "7 mins", "gender": "Female"},
    {"name": "Officer Rajesh Kumar", "badge": "DL-3921", "eta": "5 mins", "gender": "Male"},
    {"name": "Officer Anjali Singh", "badge": "DL-4102", "eta": "9 mins", "gender": "Female"},
    {"name": "Officer Vikram Rao", "badge": "DL-5673", "eta": "6 mins", "gender": "Male"}
]


# Navigation Bar Component
def show_navbar():
    logo_html = ""
    if LOGO_BASE64:
        logo_html = f'<img src="data:image/png;base64,{LOGO_BASE64}" class="nav-logo" alt="SafeWander">'
    else:
        logo_html = '<i class="fa-solid fa-shield-halved" style="font-size:1.8rem;color:#667eea;"></i>'
    
    st.markdown(f'''
    <div class="navbar">
        <div class="nav-brand">
            {logo_html}
            <span class="nav-title">SafeWander</span>
        </div>
    </div>
    ''', unsafe_allow_html=True)

# Home button function
def go_home():
    st.session_state.active_feature = None
    st.session_state.sos_active = False
    st.session_state.sos_reason = None

# Quick Profile Form
def show_quick_profile():
    # Hero with logo
    logo_html = ""
    if LOGO_BASE64:
        logo_html = f'<img src="data:image/png;base64,{LOGO_BASE64}" class="hero-logo" alt="SafeWander">'
    else:
        logo_html = '<i class="fa-solid fa-shield-halved" style="font-size:2.5rem;margin-bottom:0.5rem;"></i>'
    
    st.markdown(f'''
    <div class="hero-section">
        {logo_html}
        <div class="hero-title">SafeWander</div>
        <div class="hero-subtitle">Your AI-Powered Travel Safety Guardian</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('<div class="quick-profile">', unsafe_allow_html=True)
    st.markdown('<div class="profile-title"><i class="fa-solid fa-bolt"></i> Quick Profile Setup</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("Your Name", placeholder="e.g., Sarah", label_visibility="visible")
        gender = st.selectbox("Gender", ["Female", "Male", "Non-binary", "Prefer not to say"])
        age = st.selectbox("Age Range", ["18-25", "26-35", "36-50", "50+"])
    
    with col2:
        destination_country = st.selectbox("Destination Country", list(DESTINATIONS.keys()))
        destination_city = st.selectbox("City", DESTINATIONS[destination_country]["cities"])
        interest = st.selectbox("Primary Interest", 
            ["Beach & Relaxation", "Culture & History", "Food & Cuisine", 
             "Nightlife", "Business", "Wellness", "Adventure"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("Start My Safe Journey", use_container_width=True):
        if name and destination_country and destination_city:
            st.session_state.profile = {
                "name": name,
                "gender": gender,
                "age_range": age,
                "destination_country": destination_country,
                "destination_city": destination_city,
                "interest": interest
            }
            st.session_state.profile_complete = True
            st.rerun()
        else:
            st.error("Please fill all required fields!")

# Interactive Map Component
def show_live_map():
    profile = st.session_state.profile
    city = profile.get('destination_city', 'Delhi')
    country = profile.get('destination_country', 'India')
    
    coords = DESTINATIONS.get(country, {}).get("coords", {}).get(city, [28.6139, 77.2090])
    police = POLICE_STATIONS.get(city, [])
    
    map_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css"/>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>
        <style>
            body {{ margin: 0; padding: 0; font-family: 'Poppins', sans-serif; }}
            #map {{ width: 100%; height: 400px; border-radius: 12px; }}
            .location-btn {{
                position: absolute;
                top: 10px;
                right: 10px;
                z-index: 1000;
                background: white;
                border: 2px solid #667eea;
                border-radius: 8px;
                padding: 8px 12px;
                cursor: pointer;
                font-weight: 600;
                color: #667eea;
                font-size: 0.85rem;
                display: flex;
                align-items: center;
                gap: 5px;
            }}
            .location-btn:hover {{ background: #667eea; color: white; }}
        </style>
    </head>
    <body>
        <button class="location-btn" onclick="getLocation()"><i class="fa-solid fa-location-crosshairs"></i> My Location</button>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([{coords[0]}, {coords[1]}], 13);
            
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '© OpenStreetMap',
                maxZoom: 19
            }}).addTo(map);
            
            L.marker([{coords[0]}, {coords[1]}]).addTo(map)
                .bindPopup('<b>{city}, {country}</b><br>Your destination').openPopup();
            
            var policeIcon = L.icon({{
                iconUrl: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSIjMzY0OGY4Ij48cGF0aCBkPSJNMTIgMkM4LjEzIDIgNSA1LjEzIDUgOWMwIDUuMjUgNyAxMyA3IDEzczctNy43NSA3LTEzYzAtMy44Ny0zLjEzLTctNy03em0wIDkuNWMtMS4zOCAwLTIuNS0xLjEyLTIuNS0yLjVzMS4xMi0yLjUgMi41LTIuNSAyLjUgMS4xMiAyLjUgMi41LTEuMTIgMi41LTIuNSAyLjV6Ii8+PC9zdmc+',
                iconSize: [30, 30], iconAnchor: [15, 30], popupAnchor: [0, -30]
            }});
            
            {chr(10).join([f"L.marker([{p['lat']}, {p['lng']}], {{icon: policeIcon}}).addTo(map).bindPopup('<b>{p['name']}</b><br>{p['distance']}');" for p in police])}
            
            L.circle([{coords[0] + 0.01}, {coords[1] + 0.01}], {{
                color: '#10b981', fillColor: '#10b981', fillOpacity: 0.2, radius: 500
            }}).addTo(map).bindPopup('<b>Safe Zone</b><br>Tourist area');
            
            var userMarker = null;
            function getLocation() {{
                if (navigator.geolocation) {{
                    navigator.geolocation.getCurrentPosition(function(pos) {{
                        if (userMarker) map.removeLayer(userMarker);
                        var redIcon = L.icon({{
                            iconUrl: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSIjZWY0NDQ0Ij48cGF0aCBkPSJNMTIgMkM4LjEzIDIgNSA1LjEzIDUgOWMwIDUuMjUgNyAxMyA3IDEzczctNy43NSA3LTEzYzAtMy44Ny0zLjEzLTctNy03em0wIDkuNWMtMS4zOCAwLTIuNS0xLjEyLTIuNS0yLjVzMS4xMi0yLjUgMi41LTIuNSAyLjUgMS4xMiAyLjUgMi41LTEuMTIgMi41LTIuNSAyLjV6Ii8+PC9zdmc+',
                            iconSize: [35, 35], iconAnchor: [17, 35]
                        }});
                        userMarker = L.marker([pos.coords.latitude, pos.coords.longitude], {{icon: redIcon}}).addTo(map).bindPopup('<b>You are here!</b>').openPopup();
                        map.setView([pos.coords.latitude, pos.coords.longitude], 15);
                    }}, function(err) {{ alert("Location error: " + err.message); }});
                }} else {{ alert("Geolocation not supported"); }}
            }}
        </script>
    </body>
    </html>
    """
    components.html(map_html, height=420)


# SOS Emergency Handler
def show_sos_modal():
    data = load_safety_data()
    profile = st.session_state.profile
    
    if not st.session_state.sos_reason:
        st.markdown('<div class="emergency-modal">', unsafe_allow_html=True)
        st.markdown('<div class="emergency-title"><i class="fa-solid fa-triangle-exclamation"></i> SOS ACTIVATED</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;color:#64748b;font-size:0.9rem;">Why do you need help?</p>', unsafe_allow_html=True)
        
        reasons = [
            ("Someone is following me", "stalking", "fa-person-walking"),
            ("Someone stole my belongings", "theft", "fa-sack-xmark"),
            ("I don't feel safe here", "unsafe", "fa-face-frown"),
            ("URGENT - Need immediate help!", "urgent", "fa-bolt")
        ]
        
        for label, reason, icon in reasons:
            if st.button(f"{label}", key=reason, use_container_width=True):
                st.session_state.sos_reason = reason
                st.rerun()
        
        if st.button("Cancel SOS", use_container_width=True):
            st.session_state.sos_active = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        st.markdown('<div class="emergency-modal">', unsafe_allow_html=True)
        st.markdown('<div class="emergency-title" style="color:#10b981;"><i class="fa-solid fa-check-circle"></i> HELP IS ON THE WAY!</div>', unsafe_allow_html=True)
        
        gender = profile.get('gender', 'Male')
        country = profile.get('destination_country', 'India')
        
        if gender == 'Female' and country == 'India':
            officer = [o for o in MOCK_OFFICERS if o['gender'] == 'Female'][0]
            st.markdown('<div class="alert-success"><i class="fa-solid fa-venus"></i> Female officer dispatched as per your request</div>', unsafe_allow_html=True)
        else:
            officer = MOCK_OFFICERS[1]
        
        st.markdown(f'''
        <div class="officer-card">
            <div class="officer-photo"><i class="fa-solid fa-user-shield"></i></div>
            <div style="flex:1;">
                <div class="officer-name">{officer['name']}</div>
                <div class="officer-badge">Badge: {officer['badge']}</div>
                <div style="margin-top:0.3rem;color:#64748b;font-size:0.8rem;">
                    <i class="fa-solid fa-location-dot"></i> Location tracked | 
                    <i class="fa-solid fa-building-shield"></i> Nearest station: 1.2 km
                </div>
            </div>
            <div class="eta-badge">ETA: {officer['eta']}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        st.markdown('<div class="alert-danger">', unsafe_allow_html=True)
        st.markdown('<strong><i class="fa-solid fa-exclamation-triangle"></i> WHILE YOU WAIT:</strong>', unsafe_allow_html=True)
        
        instructions = {
            "stalking": "1. Move to a crowded public place\n2. DO NOT go to isolated areas\n3. Make eye contact with security\n4. Stay on well-lit roads",
            "theft": "1. Do NOT chase the thief\n2. Note the direction they fled\n3. Memorize their appearance\n4. Stay in public area",
            "unsafe": "1. Go to nearest public place\n2. Enter a shop/restaurant\n3. Ask staff to stay with you\n4. Share live location with friend",
            "urgent": f"1. Stay calm and safe\n2. Call emergency: {data.get('emergency_numbers', {}).get(country, {}).get('police', '100')}\n3. Describe your surroundings\n4. Do NOT put yourself in danger"
        }
        st.markdown(instructions.get(st.session_state.sos_reason, "Stay calm and wait for help."))
        st.markdown('</div>', unsafe_allow_html=True)
        
        emergency = data.get("emergency_numbers", {}).get(country, {})
        if emergency:
            st.markdown('<p style="font-weight:600;margin-top:1rem;font-size:0.9rem;"><i class="fa-solid fa-phone"></i> Emergency Numbers:</p>', unsafe_allow_html=True)
            cols = st.columns(len(emergency))
            for i, (service, number) in enumerate(emergency.items()):
                with cols[i]:
                    st.markdown(f'<div style="text-align:center;padding:0.8rem;background:#fee2e2;border-radius:8px;"><strong style="font-size:0.8rem;">{service.title()}</strong><br/><span style="font-size:1.1rem;color:#ef4444;font-weight:700;">{number}</span></div>', unsafe_allow_html=True)
        
        if st.button("I'm Safe Now - Cancel SOS", use_container_width=True):
            st.session_state.sos_active = False
            st.session_state.sos_reason = None
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Scam Price Checker - SMART VERSION
def show_scam_checker():
    import re
    data = load_safety_data()
    profile = st.session_state.profile
    country = profile.get('destination_country', 'India')
    city = profile.get('destination_city', 'Delhi')
    
    # Price reference data by country
    PRICE_THRESHOLDS = {
        "India": {"currency": "₹", "auto_normal": 150, "auto_high": 300, "taxi_normal": 200, "taxi_high": 400},
        "Thailand": {"currency": "฿", "auto_normal": 100, "auto_high": 200, "taxi_normal": 150, "taxi_high": 300},
        "Mexico": {"currency": "$", "auto_normal": 10, "auto_high": 25, "taxi_normal": 15, "taxi_high": 40},
        "USA": {"currency": "$", "auto_normal": 15, "auto_high": 40, "taxi_normal": 25, "taxi_high": 60},
        "Brazil": {"currency": "R$", "auto_normal": 20, "auto_high": 50, "taxi_normal": 30, "taxi_high": 80}
    }
    
    thresholds = PRICE_THRESHOLDS.get(country, PRICE_THRESHOLDS["India"])
    currency = thresholds["currency"]
    
    scams = data.get("transport_scams", [])
    relevant = [s for s in scams if s.get("country") == country]
    
    st.markdown('<div class="scam-checker">', unsafe_allow_html=True)
    st.markdown('<div class="scam-title"><i class="fa-solid fa-magnifying-glass-dollar"></i> Real-Time Scam Price Checker</div>', unsafe_allow_html=True)
    st.markdown(f'<p style="color:#92400e;font-size:0.85rem;">Currently in: <strong>{city}, {country}</strong></p>', unsafe_allow_html=True)
    
    query = st.text_input("What are they charging you?", 
        placeholder=f"e.g., Auto wants {currency}500 or Taxi charging {currency}1000",
        label_visibility="collapsed")
    
    if query:
        # Extract any number from the query
        numbers = re.findall(r'\d+', query.replace(',', ''))
        
        if numbers:
            amount = int(numbers[0])
            query_lower = query.lower()
            
            # Determine service type
            is_taxi = any(word in query_lower for word in ['taxi', 'cab', 'uber', 'ola', 'grab', 'car'])
            normal_rate = thresholds["taxi_normal"] if is_taxi else thresholds["auto_normal"]
            high_rate = thresholds["taxi_high"] if is_taxi else thresholds["auto_high"]
            service_type = "Taxi/Cab" if is_taxi else "Auto/Rickshaw"
            
            st.markdown('<div class="price-check">', unsafe_allow_html=True)
            
            if amount > high_rate * 2:
                # Definite scam - more than 2x high rate
                overcharge_pct = int((amount / normal_rate - 1) * 100)
                st.markdown(f'''<div class="alert-danger">
                <h4 style="color:#991b1b;margin:0 0 0.5rem 0;font-size:1rem;"><i class="fa-solid fa-circle-exclamation"></i> SCAM ALERT!</h4>
                <p style="margin:0.3rem 0;font-size:0.85rem;"><strong>They're charging:</strong> {currency}{amount}</p>
                <p style="margin:0.3rem 0;font-size:0.85rem;"><strong>Normal {service_type} rate:</strong> {currency}{normal_rate}-{high_rate}</p>
                <p style="margin:0.3rem 0;font-size:0.85rem;"><strong>Overcharge:</strong> ~{overcharge_pct}%!</p>
                </div>''', unsafe_allow_html=True)
                
                st.markdown(f'''<p style="margin-top:0.8rem;font-size:0.85rem;"><strong><i class="fa-solid fa-check"></i> What to do:</strong></p>
                <ul style="font-size:0.8rem;color:#64748b;margin:0.5rem 0;">
                    <li>Show this screen to the driver</li>
                    <li>Refuse and use app-based rides instead</li>
                    <li>Insist on meter usage</li>
                    <li>Walk away and find another option</li>
                </ul>''', unsafe_allow_html=True)
                
            elif amount > high_rate:
                # Suspicious - above high rate
                st.markdown(f'''<div class="alert-danger" style="background:linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);border-color:#f59e0b;">
                <h4 style="color:#92400e;margin:0 0 0.5rem 0;font-size:1rem;"><i class="fa-solid fa-triangle-exclamation"></i> SUSPICIOUS PRICE</h4>
                <p style="margin:0.3rem 0;font-size:0.85rem;color:#92400e;"><strong>They're charging:</strong> {currency}{amount}</p>
                <p style="margin:0.3rem 0;font-size:0.85rem;color:#92400e;"><strong>Normal {service_type} rate:</strong> {currency}{normal_rate}-{high_rate}</p>
                <p style="margin:0.3rem 0;font-size:0.85rem;color:#92400e;">This seems high. Negotiate or check distance.</p>
                </div>''', unsafe_allow_html=True)
                
            else:
                # Fair price
                st.markdown(f'''<div class="alert-success">
                <h4 style="color:#065f46;margin:0 0 0.5rem 0;font-size:1rem;"><i class="fa-solid fa-check-circle"></i> FAIR PRICE</h4>
                <p style="margin:0.3rem 0;font-size:0.85rem;"><strong>They're charging:</strong> {currency}{amount}</p>
                <p style="margin:0.3rem 0;font-size:0.85rem;"><strong>Normal {service_type} rate:</strong> {currency}{normal_rate}-{high_rate}</p>
                <p style="margin:0.3rem 0;font-size:0.85rem;">This price looks reasonable!</p>
                </div>''', unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="price-check">', unsafe_allow_html=True)
            st.markdown(f'<p style="color:#64748b;font-size:0.85rem;">Please include an amount (e.g., "{currency}300" or "300 rupees")</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Show common scams
    if relevant:
        st.markdown(f'<p style="font-weight:600;margin-top:1rem;font-size:0.9rem;"><i class="fa-solid fa-triangle-exclamation"></i> Common Scams in {city}:</p>', unsafe_allow_html=True)
        for scam in relevant[:3]:
            st.markdown(f'''
            <div style="background:white;padding:0.8rem;border-radius:8px;margin:0.5rem 0;font-size:0.85rem;">
                <strong>{scam.get("scam_type", "Scam")}</strong><br/>
                <small style="color:#64748b;">{scam.get("description", "")[:80]}...</small><br/>
                <span style="color:#10b981;">Normal: {scam.get("normal_rate", "N/A")}</span> | 
                <span style="color:#ef4444;">Scam: {scam.get("scam_rate", "N/A")}</span>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)


# Essential Phrases with WORKING Text-to-Speech
def show_phrases():
    profile = st.session_state.profile
    country = profile.get('destination_country', 'India')
    phrases = ESSENTIAL_PHRASES.get(country, [])
    lang_code = LANGUAGE_CODES.get(country, 'en-US')
    
    st.markdown(f'<div class="section-header"><i class="fa-solid fa-language"></i> 15 Essential Phrases for {country}</div>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;font-size:0.8rem;margin-bottom:1rem;">Click the speaker button to hear pronunciation</p>', unsafe_allow_html=True)
    
    # Build all phrase cards HTML
    phrases_html = ""
    for idx, (local, script, meaning) in enumerate(phrases):
        # Escape single quotes for JavaScript
        local_escaped = local.replace("'", "\\'")
        phrases_html += f'''
        <div class="phrase-card">
            <div>
                <div class="phrase-local">{local}</div>
                <div class="phrase-meaning">{script} = {meaning}</div>
            </div>
            <button class="phrase-audio" onclick="speakPhrase('{local_escaped}', '{lang_code}')" title="Click to hear pronunciation">
                <i class="fa-solid fa-volume-high"></i>
            </button>
        </div>
        '''
    
    # Everything in ONE components.html so JS and buttons are in same context
    components.html(f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
        <link href="https://fonts.googleapis.com/css2?family=Poppins:wght@400;600;700&display=swap" rel="stylesheet">
        <style>
            * {{ font-family: 'Poppins', sans-serif; margin: 0; padding: 0; box-sizing: border-box; }}
            body {{ background: transparent; }}
            .phrase-card {{
                background: linear-gradient(135deg, #ede9fe 0%, #ddd6fe 100%);
                border-radius: 12px;
                padding: 1rem;
                margin: 0.6rem 0;
                border-left: 4px solid #7c3aed;
                display: flex;
                justify-content: space-between;
                align-items: center;
            }}
            .phrase-local {{
                font-size: 1.1rem;
                font-weight: 700;
                color: #5b21b6;
            }}
            .phrase-meaning {{
                font-size: 0.85rem;
                color: #6d28d9;
            }}
            .phrase-audio {{
                background: #7c3aed;
                color: white;
                border: none;
                border-radius: 50%;
                width: 45px;
                height: 45px;
                cursor: pointer;
                font-size: 1.1rem;
                transition: all 0.2s;
                display: flex;
                align-items: center;
                justify-content: center;
                flex-shrink: 0;
            }}
            .phrase-audio:hover {{
                background: #5b21b6;
                transform: scale(1.1);
            }}
            .phrase-audio:active {{
                transform: scale(0.95);
            }}
            .phrase-audio.speaking {{
                background: #5b21b6;
                animation: pulse 0.5s infinite;
            }}
            @keyframes pulse {{
                0%, 100% {{ opacity: 1; transform: scale(1); }}
                50% {{ opacity: 0.7; transform: scale(1.05); }}
            }}
        </style>
    </head>
    <body>
        {phrases_html}
        <script>
        function speakPhrase(text, langCode) {{
            if ('speechSynthesis' in window) {{
                // Cancel any ongoing speech
                window.speechSynthesis.cancel();
                
                const utterance = new SpeechSynthesisUtterance(text);
                utterance.lang = langCode;
                utterance.rate = 0.7;
                utterance.pitch = 1.0;
                utterance.volume = 1.0;
                
                // Find the button that was clicked
                const buttons = document.querySelectorAll('.phrase-audio');
                buttons.forEach(btn => btn.classList.remove('speaking'));
                event.currentTarget.classList.add('speaking');
                
                utterance.onend = function() {{
                    event.currentTarget.classList.remove('speaking');
                }};
                
                utterance.onerror = function(e) {{
                    console.error('Speech error:', e);
                    event.currentTarget.classList.remove('speaking');
                }};
                
                // Speak immediately
                window.speechSynthesis.speak(utterance);
            }} else {{
                alert('Text-to-speech not supported. Try Chrome or Edge browser.');
            }}
        }}
        </script>
    </body>
    </html>
    """, height=len(phrases) * 75 + 20)

# Cultural Guide
def show_cultural_guide():
    data = load_safety_data()
    profile = st.session_state.profile
    country = profile.get('destination_country', 'India')
    
    cultural = next((c for c in data.get("cultural_guidelines", []) if c.get("country") == country), {})
    
    st.markdown(f'<div class="section-header"><i class="fa-solid fa-earth-americas"></i> Cultural Respect Guide: {country}</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="cultural-grid">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown(f'''
        <div class="culture-card">
            <div class="culture-icon"><i class="fa-solid fa-shirt"></i></div>
            <div class="culture-title">Dress Code</div>
            <div class="culture-text">{cultural.get("dress", "Dress modestly in religious places")}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown(f'''
        <div class="culture-card">
            <div class="culture-icon"><i class="fa-solid fa-handshake"></i></div>
            <div class="culture-title">Gestures</div>
            <div class="culture-text">{cultural.get("gestures", "Be respectful with gestures")}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    with col3:
        st.markdown(f'''
        <div class="culture-card">
            <div class="culture-icon"><i class="fa-solid fa-hands-praying"></i></div>
            <div class="culture-title">Etiquette</div>
            <div class="culture-text">{cultural.get("etiquette", "Follow local customs")}</div>
        </div>
        ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
        <div style="background:linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);padding:1rem;border-radius:12px;border-left:4px solid #10b981;">
            <h4 style="color:#065f46;font-size:0.95rem;margin:0 0 0.5rem 0;"><i class="fa-solid fa-check"></i> DO's</h4>
            <ul style="color:#047857;font-size:0.8rem;line-height:1.8;margin:0;padding-left:1.2rem;">
                <li>Remove shoes at temples/homes</li>
                <li>Use right hand for giving</li>
                <li>Ask before photographing</li>
                <li>Respect religious customs</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div style="background:linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);padding:1rem;border-radius:12px;border-left:4px solid #ef4444;">
            <h4 style="color:#991b1b;font-size:0.95rem;margin:0 0 0.5rem 0;"><i class="fa-solid fa-xmark"></i> DON'Ts</h4>
            <ul style="color:#991b1b;font-size:0.8rem;line-height:1.8;margin:0;padding-left:1.2rem;">
                <li>Don't point feet at people</li>
                <li>Don't touch heads</li>
                <li>Don't wear shoes in temples</li>
                <li>Don't show excessive PDA</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)


# Main Dashboard
def show_dashboard():
    profile = st.session_state.profile
    data = load_safety_data()
    
    # Navigation bar with home button
    show_navbar()
    
    # Home button in sidebar area
    col1, col2, col3 = st.columns([1, 6, 1])
    with col3:
        if st.button("🏠", key="home_btn", help="Go to Home"):
            go_home()
            st.rerun()
    
    # Show SOS modal if active
    if st.session_state.sos_active:
        show_sos_modal()
        return
    
    # If a feature is active, show it with back button
    if st.session_state.active_feature:
        col1, col2 = st.columns([1, 8])
        with col1:
            if st.button("← Back", key="back_btn"):
                st.session_state.active_feature = None
                st.rerun()
        
        if st.session_state.active_feature == 'map':
            st.markdown('<div class="map-container">', unsafe_allow_html=True)
            st.markdown('<div class="section-header"><i class="fa-solid fa-map-location-dot"></i> Live Safety Map</div>', unsafe_allow_html=True)
            show_live_map()
            st.markdown('</div>', unsafe_allow_html=True)
        elif st.session_state.active_feature == 'scam':
            show_scam_checker()
        elif st.session_state.active_feature == 'phrases':
            show_phrases()
        elif st.session_state.active_feature == 'culture':
            show_cultural_guide()
        return
    
    # Welcome banner - smaller
    st.markdown(f'''
    <div class="hero-section">
        <div class="hero-title">Welcome, {profile.get("name")}!</div>
        <div class="hero-subtitle">
            <i class="fa-solid fa-location-dot"></i> {profile.get("destination_city")}, {profile.get("destination_country")} | 
            <i class="fa-solid fa-heart"></i> {profile.get("interest", "Exploring")}
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Feature cards - instant switching
    st.markdown('<div class="dashboard-grid">', unsafe_allow_html=True)
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.markdown('''
        <div class="feature-card">
            <div class="card-icon"><i class="fa-solid fa-map-location-dot"></i></div>
            <div class="card-title">Live Safety Map</div>
            <div class="card-desc">Police stations & safe zones</div>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("Open Map", key="map_btn", use_container_width=True):
            st.session_state.active_feature = 'map'
            st.rerun()
    
    with col2:
        st.markdown('''
        <div class="feature-card">
            <div class="card-icon"><i class="fa-solid fa-magnifying-glass-dollar"></i></div>
            <div class="card-title">Scam Checker</div>
            <div class="card-desc">Check if you're being scammed</div>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("Check Prices", key="scam_btn", use_container_width=True):
            st.session_state.active_feature = 'scam'
            st.rerun()
    
    with col3:
        st.markdown('''
        <div class="feature-card">
            <div class="card-icon"><i class="fa-solid fa-language"></i></div>
            <div class="card-title">Essential Phrases</div>
            <div class="card-desc">15 life-saving words</div>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("Learn Phrases", key="phrase_btn", use_container_width=True):
            st.session_state.active_feature = 'phrases'
            st.rerun()
    
    with col4:
        st.markdown('''
        <div class="feature-card">
            <div class="card-icon"><i class="fa-solid fa-earth-americas"></i></div>
            <div class="card-title">Cultural Guide</div>
            <div class="card-desc">Do's and Don'ts</div>
        </div>
        ''', unsafe_allow_html=True)
        if st.button("View Guide", key="culture_btn", use_container_width=True):
            st.session_state.active_feature = 'culture'
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # SOS Button (fixed position via HTML)
    st.markdown('''
    <div class="sos-button">
        <button class="sos-btn" onclick="document.querySelector('[data-testid=stButton] button').click()" title="Emergency SOS">
            <i class="fa-solid fa-triangle-exclamation"></i>
        </button>
    </div>
    ''', unsafe_allow_html=True)
    
    # Hidden SOS button for Streamlit
    if st.button("SOS", key="sos_main", help="Emergency Help"):
        st.session_state.sos_active = True
        st.rerun()
    
    # AI Assistant section
    st.markdown("---")
    st.markdown('<div class="section-header"><i class="fa-solid fa-robot"></i> AI Safety Assistant</div>', unsafe_allow_html=True)
    
    question = st.text_area(
        "Ask anything about safety...",
        placeholder=f"e.g., Is it safe to visit street food markets at night as a {profile.get('gender')} in {profile.get('destination_city')}?",
        height=80,
        label_visibility="collapsed"
    )
    
    if st.button("Get Personalized Advice", use_container_width=True):
        if question:
            groq_client = init_groq()
            with st.spinner("Analyzing..."):
                if groq_client:
                    try:
                        response = groq_client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": f"You are a travel safety expert. User is {profile.get('name')}, {profile.get('gender')}, {profile.get('age_range')}, visiting {profile.get('destination_city')}, {profile.get('destination_country')}. Provide specific, concise safety advice."},
                                {"role": "user", "content": question}
                            ],
                            model="llama-3.3-70b-versatile",
                            temperature=0.6,
                            max_tokens=300
                        )
                        advice = response.choices[0].message.content
                        st.markdown(f'<div class="alert-success">{advice}</div>', unsafe_allow_html=True)
                    except:
                        st.error("AI temporarily unavailable. Please try the other features!")
                else:
                    st.warning("Add GROQ_API_KEY to Streamlit secrets for AI features")

# Main App
def main():
    if not st.session_state.profile_complete:
        show_quick_profile()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()


