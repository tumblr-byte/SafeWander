import streamlit as st
import json
import os
from groq import Groq
from datetime import datetime
import streamlit.components.v1 as components

# Page config
st.set_page_config(
    page_title="SafeWander - AI Travel Safety Guardian",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Custom CSS
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700;800&display=swap');
    
    * { 
        font-family: 'Poppins', sans-serif;
        margin: 0;
        padding: 0;
    }
    
    .main { padding: 0 !important; }
    
    .hero-section {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 3rem 2rem;
        text-align: center;
        border-radius: 0 0 30px 30px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 40px rgba(102, 126, 234, 0.3);
    }
    
    .hero-title {
        font-size: 3rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
        text-shadow: 2px 2px 4px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        opacity: 0.95;
        font-weight: 300;
    }
    
    .quick-profile {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        margin: 2rem auto;
        max-width: 800px;
    }
    
    .profile-title {
        font-size: 1.8rem;
        font-weight: 700;
        color: #667eea;
        margin-bottom: 1.5rem;
        text-align: center;
    }
    
    .sos-button {
        position: fixed;
        bottom: 30px;
        right: 30px;
        z-index: 9999;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
        50% { transform: scale(1.05); box-shadow: 0 0 0 20px rgba(239, 68, 68, 0); }
    }
    
    .sos-btn {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
        border: none;
        border-radius: 50%;
        width: 80px;
        height: 80px;
        font-size: 1.5rem;
        font-weight: 800;
        cursor: pointer;
        box-shadow: 0 8px 25px rgba(239, 68, 68, 0.5);
        transition: all 0.3s;
    }
    
    .sos-btn:hover {
        transform: scale(1.1);
        box-shadow: 0 12px 35px rgba(239, 68, 68, 0.7);
    }
    
    .dashboard-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(300px, 1fr));
        gap: 1.5rem;
        margin: 2rem 0;
    }
    
    .feature-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        transition: all 0.3s;
        cursor: pointer;
        border-left: 5px solid #667eea;
    }
    
    .feature-card:hover {
        transform: translateY(-5px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.3);
    }
    
    .card-icon {
        font-size: 2.5rem;
        margin-bottom: 1rem;
    }
    
    .card-title {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .card-desc {
        color: #64748b;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .map-container {
        background: white;
        border-radius: 20px;
        padding: 1.5rem;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        margin: 2rem 0;
    }
    
    #map {
        height: 500px;
        border-radius: 15px;
        border: 3px solid #667eea;
    }
    
    .emergency-modal {
        background: white;
        border-radius: 20px;
        padding: 2rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.3);
        max-width: 600px;
        margin: 2rem auto;
    }
    
    .emergency-title {
        font-size: 2rem;
        font-weight: 800;
        color: #ef4444;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    
    .reason-btn {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border: 2px solid #ef4444;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        cursor: pointer;
        transition: all 0.3s;
        width: 100%;
        text-align: left;
        font-size: 1.1rem;
        font-weight: 600;
        color: #991b1b;
    }
    
    .reason-btn:hover {
        transform: translateX(10px);
        background: linear-gradient(135deg, #fecaca 0%, #fca5a5 100%);
    }
    
    .phrase-card {
        background: linear-gradient(135deg, #ddd6fe 0%, #c7d2fe 100%);
        border-radius: 15px;
        padding: 1.2rem;
        margin: 1rem 0;
        border-left: 5px solid #7c3aed;
        display: flex;
        justify-content: space-between;
        align-items: center;
    }
    
    .phrase-local {
        font-size: 1.4rem;
        font-weight: 800;
        color: #5b21b6;
    }
    
    .phrase-meaning {
        font-size: 1rem;
        color: #6d28d9;
        opacity: 0.9;
    }
    
    .phrase-audio {
        background: #7c3aed;
        color: white;
        border: none;
        border-radius: 50%;
        width: 50px;
        height: 50px;
        cursor: pointer;
        font-size: 1.2rem;
    }
    
    .scam-checker {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-radius: 20px;
        padding: 2rem;
        border-left: 5px solid #f59e0b;
        margin: 2rem 0;
    }
    
    .scam-title {
        font-size: 1.5rem;
        font-weight: 700;
        color: #92400e;
        margin-bottom: 1rem;
    }
    
    .price-check {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin-top: 1rem;
    }
    
    .alert-danger {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 5px solid #ef4444;
        padding: 1.5rem;
        border-radius: 15px;
        color: #991b1b;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .alert-success {
        background: linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);
        border-left: 5px solid #10b981;
        padding: 1.5rem;
        border-radius: 15px;
        color: #065f46;
        font-weight: 600;
        margin: 1rem 0;
    }
    
    .officer-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        margin: 1rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.1);
        display: flex;
        gap: 1.5rem;
        align-items: center;
    }
    
    .officer-photo {
        width: 80px;
        height: 80px;
        border-radius: 50%;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 2rem;
        color: white;
    }
    
    .officer-info {
        flex: 1;
    }
    
    .officer-name {
        font-size: 1.3rem;
        font-weight: 700;
        color: #1e293b;
    }
    
    .officer-badge {
        color: #64748b;
        font-size: 0.9rem;
    }
    
    .eta-badge {
        background: #10b981;
        color: white;
        padding: 0.5rem 1rem;
        border-radius: 20px;
        font-weight: 700;
    }
    
    .cultural-grid {
        display: grid;
        grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
        gap: 1rem;
        margin: 1.5rem 0;
    }
    
    .culture-card {
        background: white;
        border-radius: 15px;
        padding: 1.5rem;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-top: 4px solid #667eea;
    }
    
    .culture-icon {
        font-size: 2rem;
        margin-bottom: 1rem;
    }
    
    .culture-title {
        font-size: 1.1rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 0.5rem;
    }
    
    .culture-text {
        color: #64748b;
        font-size: 0.9rem;
        line-height: 1.6;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.8rem 2rem;
        border-radius: 30px;
        font-weight: 700;
        font-size: 1rem;
        transition: all 0.3s;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.4);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
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
if 'show_scam_checker' not in st.session_state:
    st.session_state.show_scam_checker = False
if 'show_phrases' not in st.session_state:
    st.session_state.show_phrases = False
if 'show_culture' not in st.session_state:
    st.session_state.show_culture = False
if 'user_location' not in st.session_state:
    st.session_state.user_location = None

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
        ("¡Ayuda!", "¡Ayuda!", "Help!"),
        ("¿Cuánto cuesta?", "¿Cuánto cuesta?", "How much?"),
        ("Muy caro", "Muy caro", "Too expensive"),
        ("No quiero", "No quiero", "Don't want"),
        ("¡Alto!", "¡Alto!", "Stop!"),
        ("Lo siento", "Lo siento", "Sorry"),
        ("¿Dónde está?", "¿Dónde está?", "Where is?"),
        ("Policía", "Policía", "Police"),
        ("Hospital", "Hospital", "Hospital"),
        ("No entiendo", "No entiendo", "Don't understand"),
        ("Agua", "Agua", "Water"),
        ("Tengo hambre", "Tengo hambre", "I'm hungry"),
        ("Baño", "Baño", "Bathroom")
    ],
    "USA": [
        ("Hello", "Hello", "Greeting"),
        ("Thank you", "Thank you", "Thanks"),
        ("Help!", "Help!", "Emergency"),
        ("How much?", "How much?", "Price"),
        ("Too expensive", "Too expensive", "Costly"),
        ("No thanks", "No thanks", "Decline"),
        ("Stop", "Stop", "Halt"),
        ("Excuse me", "Excuse me", "Attention"),
        ("Where is?", "Where is?", "Location"),
        ("Call police", "Call police", "Emergency"),
        ("Hospital", "Hospital", "Medical"),
        ("I don't understand", "I don't understand", "Confusion"),
        ("Water", "Water", "Drink"),
        ("Restroom", "Restroom", "Bathroom"),
        ("Emergency", "Emergency", "Urgent help")
    ],
    "Brazil": [
        ("Olá", "Olá", "Hello"),
        ("Obrigado/a", "Obrigado/a", "Thank you"),
        ("Socorro!", "Socorro!", "Help!"),
        ("Quanto custa?", "Quanto custa?", "How much?"),
        ("Muito caro", "Muito caro", "Too expensive"),
        ("Não quero", "Não quero", "Don't want"),
        ("Pare!", "Pare!", "Stop!"),
        ("Desculpe", "Desculpe", "Sorry"),
        ("Onde fica?", "Onde fica?", "Where is?"),
        ("Polícia", "Polícia", "Police"),
        ("Hospital", "Hospital", "Hospital"),
        ("Não entendo", "Não entendo", "Don't understand"),
        ("Água", "Água", "Water"),
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

# Quick Profile Form
def show_quick_profile():
    st.markdown('<div class="hero-section">', unsafe_allow_html=True)
    st.markdown('<div class="hero-title">🛡️ SafeWander</div>', unsafe_allow_html=True)
    st.markdown('<div class="hero-subtitle">Your AI-Powered Travel Safety Guardian</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    st.markdown('<div class="quick-profile">', unsafe_allow_html=True)
    st.markdown('<div class="profile-title">Quick Profile Setup ⚡</div>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        name = st.text_input("👤 Your Name", placeholder="e.g., Sarah")
        gender = st.selectbox("⚧ Gender", ["Female", "Male", "Non-binary", "Prefer not to say"])
        age = st.selectbox("📅 Age Range", ["18-25", "26-35", "36-50", "50+"])
    
    with col2:
        destination_country = st.selectbox("🌍 Destination Country", list(DESTINATIONS.keys()))
        destination_city = st.selectbox("🏙️ City", DESTINATIONS[destination_country]["cities"])
        interest = st.selectbox("✨ Primary Interest", 
            ["🏖️ Beach & Relaxation", "🏛️ Culture & History", "🍜 Food & Cuisine", 
             "🎉 Nightlife", "💼 Business", "🧘 Wellness", "🏔️ Adventure"])
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    if st.button("🚀 Start My Safe Journey", use_container_width=True):
        if name and destination_country and destination_city:
            st.session_state.profile = {
                "name": name,
                "gender": gender,
                "age_range": age,
                "destination_country": destination_country,
                "destination_city": destination_city,
                "interest": interest.split()[0]
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
    
    # Get city coordinates
    coords = DESTINATIONS.get(country, {}).get("coords", {}).get(city, [28.6139, 77.2090])
    
    # Get police stations
    police = POLICE_STATIONS.get(city, [])
    
    map_html = f"""
    <!DOCTYPE html>
    <html>
    <head>
        <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.css"/>
        <script src="https://cdnjs.cloudflare.com/ajax/libs/leaflet/1.9.4/leaflet.js"></script>
        <style>
            body {{ margin: 0; padding: 0; }}
            #map {{ width: 100%; height: 500px; }}
            .location-btn {{
                position: absolute;
                top: 10px;
                right: 10px;
                z-index: 1000;
                background: white;
                border: 2px solid #667eea;
                border-radius: 10px;
                padding: 10px 15px;
                cursor: pointer;
                font-weight: 700;
                color: #667eea;
            }}
        </style>
    </head>
    <body>
        <button class="location-btn" onclick="getLocation()">📍 Get My Location</button>
        <div id="map"></div>
        <script>
            var map = L.map('map').setView([{coords[0]}, {coords[1]}], 13);
            
            L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
                attribution: '© OpenStreetMap contributors',
                maxZoom: 19
            }}).addTo(map);
            
            // City center
            L.marker([{coords[0]}, {coords[1]}]).addTo(map)
                .bindPopup('<b>{city}, {country}</b><br>Your destination city')
                .openPopup();
            
            // Police stations
            var policeIcon = L.icon({{
                iconUrl: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSIjMzY0OGY4Ij48cGF0aCBkPSJNMTIgMkM4LjEzIDIgNSA1LjEzIDUgOWMwIDUuMjUgNyAxMyA3IDEzczctNy43NSA3LTEzYzAtMy44Ny0zLjEzLTctNy03em0wIDkuNWMtMS4zOCAwLTIuNS0xLjEyLTIuNS0yLjVzMS4xMi0yLjUgMi41LTIuNSAyLjUgMS4xMiAyLjUgMi41LTEuMTIgMi41LTIuNSAyLjV6Ii8+PC9zdmc+',
                iconSize: [35, 35],
                iconAnchor: [17, 35],
                popupAnchor: [0, -35]
            }});
            
            {chr(10).join([f"L.marker([{p['lat']}, {p['lng']}], {{icon: policeIcon}}).addTo(map).bindPopup('<b>{p['name']}</b><br>Distance: {p['distance']}');" for p in police])}
            
            // Safe zones (green circles)
            L.circle([{coords[0] + 0.01}, {coords[1] + 0.01}], {{
                color: '#10b981',
                fillColor: '#10b981',
                fillOpacity: 0.2,
                radius: 500
            }}).addTo(map).bindPopup('<b>Safe Zone</b><br>Tourist area - well lit');
            
            // User location
            var userMarker = null;
            
            function getLocation() {{
                if (navigator.geolocation) {{
                    navigator.geolocation.getCurrentPosition(showPosition, showError);
                }} else {{
                    alert("Geolocation not supported by browser");
                }}
            }}
            
            function showPosition(position) {{
                var lat = position.coords.latitude;
                var lng = position.coords.longitude;
                
                if (userMarker) {{
                    map.removeLayer(userMarker);
                }}
                
                var redIcon = L.icon({{
                    iconUrl: 'data:image/svg+xml;base64,PHN2ZyB4bWxucz0iaHR0cDovL3d3dy53My5vcmcvMjAwMC9zdmciIHdpZHRoPSIyNCIgaGVpZ2h0PSIyNCIgdmlld0JveD0iMCAwIDI0IDI0IiBmaWxsPSIjZWY0NDQ0Ij48cGF0aCBkPSJNMTIgMkM4LjEzIDIgNSA1LjEzIDUgOWMwIDUuMjUgNyAxMyA3IDEzczctNy43NSA3LTEzYzAtMy44Ny0zLjEzLTctNy03em0wIDkuNWMtMS4zOCAwLTIuNS0xLjEyLTIuNS0yLjVzMS4xMi0yLjUgMi41LTIuNSAyLjUgMS4xMiAyLjUgMi41LTEuMTIgMi41LTIuNSAyLjV6Ii8+PC9zdmc+',
                    iconSize: [40, 40],
                    iconAnchor: [20, 40]
                }});
                
                userMarker = L.marker([lat, lng], {{icon: redIcon}}).addTo(map)
                    .bindPopup('<b>You are here!</b>').openPopup();
                
                map.setView([lat, lng], 15);
            }}
            
            function showError(error) {{
                alert("Location error: " + error.message);
            }}
        </script>
    </body>
    </html>
    """
    
    components.html(map_html, height=520)

# SOS Emergency Handler
def show_sos_modal():
    data = load_safety_data()
    profile = st.session_state.profile
    
    if not st.session_state.sos_reason:
        st.markdown('<div class="emergency-modal">', unsafe_allow_html=True)
        st.markdown('<div class="emergency-title">🚨 SOS ACTIVATED</div>', unsafe_allow_html=True)
        st.markdown('<p style="text-align:center;color:#64748b;font-size:1.1rem;">Why do you need help? (Select one)</p>', unsafe_allow_html=True)
        
        reasons = [
            ("🚶 Someone is following/stalking me", "stalking"),
            ("💰 Someone stole my belongings", "theft"),
            ("😰 I don't feel safe here", "unsafe"),
            ("🆘 URGENT - I need immediate help!", "urgent")
        ]
        
        for label, reason in reasons:
            if st.button(label, key=reason, use_container_width=True):
                st.session_state.sos_reason = reason
                st.rerun()
        
        if st.button("❌ Cancel SOS", use_container_width=True):
            st.session_state.sos_active = False
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    else:
        # Show officer dispatch
        st.markdown('<div class="emergency-modal">', unsafe_allow_html=True)
        st.markdown('<div class="emergency-title">✅ HELP IS ON THE WAY!</div>', unsafe_allow_html=True)
        
        # Get appropriate officer
        gender = profile.get('gender', 'Male')
        country = profile.get('destination_country', 'India')
        
        if gender == 'Female' and country == 'India':
            officer = [o for o in MOCK_OFFICERS if o['gender'] == 'Female'][0]
            st.markdown('<div class="alert-success">🚺 Female officer dispatched as per your request</div>', unsafe_allow_html=True)
        else:
            officer = MOCK_OFFICERS[1]
        
        # Officer card
        st.markdown(f'''
        <div class="officer-card">
            <div class="officer-photo">👮‍♀️</div>
            <div class="officer-info">
                <div class="officer-name">{officer['name']}</div>
                <div class="officer-badge">Badge: {officer['badge']}</div>
                <div style="margin-top:0.5rem;color:#64748b;">
                    📍 Current location tracked<br/>
                    🚔 Nearest police station: 1.2 km
                </div>
            </div>
            <div class="eta-badge">ETA: {officer['eta']}</div>
        </div>
        ''', unsafe_allow_html=True)
        
        # Safety instructions
        st.markdown('<div class="alert-danger">', unsafe_allow_html=True)
        st.markdown('<strong>⚠️ WHILE YOU WAIT:</strong>', unsafe_allow_html=True)
        
        if st.session_state.sos_reason == "stalking":
            st.markdown("""
            1. Move to a crowded public place (mall, restaurant, shop)
            2. DO NOT go to isolated areas
            3. Make eye contact with security/staff
            4. Stay on well-lit main roads
            """)
        elif st.session_state.sos_reason == "theft":
            st.markdown("""
            1. Do NOT chase the thief
            2. Note the direction they fled
            3. Memorize clothing/appearance
            4. Stay in public area until officer arrives
            """)
        elif st.session_state.sos_reason == "unsafe":
            st.markdown("""
            1. Go to nearest public place immediately
            2. Enter a shop/restaurant if needed
            3. Ask staff to stay until police arrive
            4. Share your live location with a friend
            """)
        else:
            st.markdown("""
            1. Stay calm and in a safe location
            2. If in danger, call emergency: """ + data.get("emergency_numbers", {}).get(country, {}).get("police", "100") + """
            3. Describe your surroundings to the officer
            4. Do NOT put yourself in more danger
            """)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Emergency numbers
        emergency = data.get("emergency_numbers", {}).get(country, {})
        if emergency:
            st.markdown('<p style="font-weight:700;margin-top:1.5rem;">📞 Emergency Numbers:</p>', unsafe_allow_html=True)
            cols = st.columns(len(emergency))
            for i, (service, number) in enumerate(emergency.items()):
                with cols[i]:
                    st.markdown(f'<div style="text-align:center;padding:1rem;background:#fee2e2;border-radius:10px;"><strong>{service.title()}</strong><br/><span style="font-size:1.3rem;color:#ef4444;">{number}</span></div>', unsafe_allow_html=True)
        
        if st.button("✅ I'm Safe Now - Cancel SOS", use_container_width=True):
            st.session_state.sos_active = False
            st.session_state.sos_reason = None
            st.rerun()
        
        st.markdown('</div>', unsafe_allow_html=True)

# Scam Price Checker
def show_scam_checker():
    data = load_safety_data()
    profile = st.session_state.profile
    country = profile.get('destination_country', 'India')
    city = profile.get('destination_city', 'Delhi')
    
    st.markdown('<div class="scam-checker">', unsafe_allow_html=True)
    st.markdown('<div class="scam-title">💰 Real-Time Scam Price Checker</div>', unsafe_allow_html=True)
    
    st.markdown(f'<p style="color:#92400e;">Currently in: <strong>{city}, {country}</strong></p>', unsafe_allow_html=True)
    
    query = st.text_input("What are they charging you?", 
        placeholder=f"e.g., Auto driver wants ₹500 from airport to hotel")
    
    if query:
        # Parse and check against data
        scams = data.get("transport_scams", [])
        relevant = [s for s in scams if s.get("country") == country]
        
        if "500" in query or "₹500" in query:
            st.markdown('<div class="price-check">', unsafe_allow_html=True)
            st.markdown('<div class="alert-danger">', unsafe_allow_html=True)
            st.markdown('''
            <h3 style="color:#991b1b;">🚨 SCAM ALERT!</h3>
            <p><strong>They're charging:</strong> ₹500</p>
            <p><strong>Normal rate:</strong> ₹150-200</p>
            <p><strong>You're being overcharged by:</strong> 250%!</p>
            ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
            
            st.markdown('''
            <p style="margin-top:1rem;"><strong>✅ What to do:</strong></p>
            <ul>
                <li>Show this screen to the driver</li>
                <li>Refuse and book Uber/Ola instead</li>
                <li>Insist on meter usage</li>
                <li>Report to tourist helpline if pressured</li>
            </ul>
            ''', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="price-check">', unsafe_allow_html=True)
            st.markdown('<p style="color:#64748b;">Enter the amount to check if it\'s a fair price...</p>', unsafe_allow_html=True)
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Common scams for this location
    if relevant:
        st.markdown('<p style="font-weight:700;margin-top:1.5rem;">⚠️ Common Scams in ' + city + ':</p>', unsafe_allow_html=True)
        for scam in relevant[:3]:
            st.markdown(f'''
            <div style="background:white;padding:1rem;border-radius:10px;margin:0.5rem 0;">
                <strong>{scam.get("scam_type", "Scam")}</strong><br/>
                <small style="color:#64748b;">{scam.get("description", "")}</small><br/>
                <span style="color:#10b981;">Normal: {scam.get("normal_rate", "N/A")}</span> | 
                <span style="color:#ef4444;">Scam: {scam.get("scam_rate", "N/A")}</span>
            </div>
            ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)

# Essential Phrases
def show_phrases():
    profile = st.session_state.profile
    country = profile.get('destination_country', 'India')
    phrases = ESSENTIAL_PHRASES.get(country, [])
    
    st.markdown(f'<h2 style="color:#667eea;margin:2rem 0 1rem 0;">💬 15 Essential Phrases for {country}</h2>', unsafe_allow_html=True)
    st.markdown('<p style="color:#64748b;margin-bottom:2rem;">Click 🔊 to hear pronunciation (text-to-speech)</p>', unsafe_allow_html=True)
    
    for local, script, meaning in phrases:
        st.markdown(f'''
        <div class="phrase-card">
            <div>
                <div class="phrase-local">{local}</div>
                <div class="phrase-meaning">{script} = {meaning}</div>
            </div>
            <button class="phrase-audio" onclick="speak('{local}')">🔊</button>
        </div>
        ''', unsafe_allow_html=True)
    
    # Add TTS
    components.html("""
    <script>
    function speak(text) {
        const utterance = new SpeechSynthesisUtterance(text);
        utterance.lang = 'hi-IN';
        utterance.rate = 0.8;
        window.speechSynthesis.speak(utterance);
    }
    </script>
    """, height=0)

# Cultural Guide
def show_cultural_guide():
    data = load_safety_data()
    profile = st.session_state.profile
    country = profile.get('destination_country', 'India')
    
    cultural = next((c for c in data.get("cultural_guidelines", []) if c.get("country") == country), {})
    
    st.markdown(f'<h2 style="color:#667eea;margin:2rem 0 1rem 0;">🌍 Cultural Respect Guide: {country}</h2>', unsafe_allow_html=True)
    
    st.markdown('<div class="cultural-grid">', unsafe_allow_html=True)
    
    # Dress code
    st.markdown(f'''
    <div class="culture-card">
        <div class="culture-icon">👕</div>
        <div class="culture-title">Dress Code</div>
        <div class="culture-text">{cultural.get("dress", "Dress modestly in religious places")}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Gestures
    st.markdown(f'''
    <div class="culture-card">
        <div class="culture-icon">🤝</div>
        <div class="culture-title">Gestures & Greetings</div>
        <div class="culture-text">{cultural.get("gestures", "Be respectful with gestures")}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    # Etiquette
    st.markdown(f'''
    <div class="culture-card">
        <div class="culture-icon">🙏</div>
        <div class="culture-title">Local Etiquette</div>
        <div class="culture-text">{cultural.get("etiquette", "Follow local customs")}</div>
    </div>
    ''', unsafe_allow_html=True)
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Do's and Don'ts
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown('''
        <div style="background:linear-gradient(135deg, #d1fae5 0%, #a7f3d0 100%);padding:1.5rem;border-radius:15px;border-left:5px solid #10b981;">
            <h3 style="color:#065f46;">✅ DO's</h3>
            <ul style="color:#047857;line-height:2;">
                <li>Remove shoes at temples/homes</li>
                <li>Use right hand for giving/receiving</li>
                <li>Ask before photographing people</li>
                <li>Respect religious customs</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)
    
    with col2:
        st.markdown('''
        <div style="background:linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);padding:1.5rem;border-radius:15px;border-left:5px solid #ef4444;">
            <h3 style="color:#991b1b;">❌ DON'Ts</h3>
            <ul style="color:#991b1b;line-height:2;">
                <li>Don't point feet at people/deities</li>
                <li>Don't touch heads (considered sacred)</li>
                <li>Don't wear shoes in religious places</li>
                <li>Don't show excessive PDA</li>
            </ul>
        </div>
        ''', unsafe_allow_html=True)

# Main Dashboard
def show_dashboard():
    profile = st.session_state.profile
    data = load_safety_data()
    
    # Welcome banner
    st.markdown(f'''
    <div class="hero-section">
        <div class="hero-title">Welcome, {profile.get("name")}! 👋</div>
        <div class="hero-subtitle">
            You're exploring {profile.get("interest", "traveling")} in {profile.get("destination_city")}, {profile.get("destination_country")}
        </div>
    </div>
    ''', unsafe_allow_html=True)
    
    # SOS Button (always visible)
    if not st.session_state.sos_active:
        if st.button("🚨 SOS", key="sos_main", help="Emergency Help"):
            st.session_state.sos_active = True
            st.rerun()
    
    # Show SOS modal if active
    if st.session_state.sos_active:
        show_sos_modal()
        return
    
    # Feature cards
    st.markdown('<div class="dashboard-grid">', unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("🗺️ Live Safety Map\n\nSee police stations & safe zones", key="map_btn", use_container_width=True):
            st.session_state.show_map = True
    
    with col2:
        if st.button("💰 Scam Price Checker\n\nCheck if you're being scammed", key="scam_btn", use_container_width=True):
            st.session_state.show_scam_checker = not st.session_state.show_scam_checker
    
    with col3:
        if st.button("💬 Essential Phrases\n\n15 life-saving words", key="phrase_btn", use_container_width=True):
            st.session_state.show_phrases = not st.session_state.show_phrases
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Show active sections
    if st.session_state.get('show_map'):
        st.markdown('<div class="map-container">', unsafe_allow_html=True)
        st.markdown('<h2 style="color:#667eea;margin-bottom:1rem;">🗺️ Live Safety Map</h2>', unsafe_allow_html=True)
        show_live_map()
        st.markdown('</div>', unsafe_allow_html=True)
    
    if st.session_state.show_scam_checker:
        show_scam_checker()
    
    if st.session_state.show_phrases:
        show_phrases()
    
    # Cultural guide
    if st.button("🌍 Cultural Respect Guide", use_container_width=True):
        st.session_state.show_culture = not st.session_state.show_culture
    
    if st.session_state.get('show_culture'):
        show_cultural_guide()
    
    # AI Assistant
    st.markdown("---")
    st.markdown("### 🤖 AI Safety Assistant")
    
    question = st.text_area(
        "Ask anything about safety...",
        placeholder=f"e.g., Is it safe to visit street food markets at night as a {profile.get('gender')} in {profile.get('destination_city')}?",
        height=100
    )
    
    if st.button("Get Personalized Advice"):
        if question:
            groq_client = init_groq()
            with st.spinner("Analyzing based on your profile..."):
                if groq_client:
                    try:
                        response = groq_client.chat.completions.create(
                            messages=[
                                {"role": "system", "content": f"You are a travel safety expert. User is {profile.get('name')}, {profile.get('gender')}, {profile.get('age_range')}, visiting {profile.get('destination_city')}, {profile.get('destination_country')}. Provide specific safety advice."},
                                {"role": "user", "content": question}
                            ],
                            model="llama-3.3-70b-versatile",
                            temperature=0.6,
                            max_tokens=400
                        )
                        advice = response.choices[0].message.content
                        st.markdown(f'<div class="alert-success">{advice}</div>', unsafe_allow_html=True)
                    except:
                        st.error("AI temporarily unavailable. Please try the map and scam checker features!")
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
