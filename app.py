"""
SafeWonder - Travel Safety Assistant
Main application entry point
"""

import streamlit as st
import os
from pathlib import Path

# Import utilities
from utils.session_manager import initialize_session_state, get_session_value, set_session_value
from utils.database_loader import load_database, get_country_data
from utils.groq_client import validate_api_key

# Import components
from components.profile_manager import show_onboarding_screen, show_profile_settings
from components.situation_analyzer_ui import show_situation_analyzer
from components.culture_translator_ui import show_culture_translator
from components.ocr_translator_ui import show_ocr_translator


def load_custom_css():
    """Load custom CSS styling"""
    css = """
    <style>
    /* Import Inter font and Font Awesome */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');
    @import url('https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css');
    
    :root {
        --primary: #6366F1;
        --secondary: #EC4899;
        --success: #10B981;
        --warning: #F59E0B;
        --danger: #EF4444;
        --background: #0F172A;
        --surface: #1E293B;
        --text-primary: #F1F5F9;
        --text-secondary: #94A3B8;
    }
    
    /* Global styles */
    .stApp {
        font-family: 'Inter', sans-serif;
    }
    
    /* Hide Streamlit branding */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    
    /* Custom card styling */
    .custom-card {
        background: rgba(30, 41, 59, 0.6);
        backdrop-filter: blur(10px);
        border-radius: 12px;
        padding: 24px;
        margin: 16px 0;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        border: 1px solid rgba(99, 102, 241, 0.2);
        transition: all 0.3s ease;
    }
    
    .custom-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 12px rgba(99, 102, 241, 0.2);
    }
    
    /* Risk score styling */
    .risk-low {
        color: #10B981;
        font-size: 48px;
        font-weight: 700;
    }
    
    .risk-medium {
        color: #F59E0B;
        font-size: 48px;
        font-weight: 700;
    }
    
    .risk-high {
        color: #EF4444;
        font-size: 48px;
        font-weight: 700;
    }
    
    /* Emergency button */
    .emergency-button {
        position: fixed;
        bottom: 24px;
        right: 24px;
        z-index: 1000;
        animation: pulse 2s infinite;
    }
    
    @keyframes pulse {
        0%, 100% {
            box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7);
        }
        50% {
            box-shadow: 0 0 0 20px rgba(239, 68, 68, 0);
        }
    }
    
    /* Button styling */
    .stButton>button {
        border-radius: 8px;
        font-weight: 600;
        transition: all 0.2s ease;
    }
    
    .stButton>button:hover {
        transform: scale(0.98);
    }
    
    /* Input field styling */
    .stTextInput>div>div>input,
    .stTextArea>div>div>textarea {
        border-radius: 8px;
        border: 2px solid rgba(99, 102, 241, 0.3);
        transition: all 0.3s ease;
    }
    
    .stTextInput>div>div>input:focus,
    .stTextArea>div>div>textarea:focus {
        border-color: #6366F1;
        box-shadow: 0 0 0 3px rgba(99, 102, 241, 0.1);
    }
    
    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1E293B 0%, #0F172A 100%);
    }
    
    /* Logo styling */
    .logo-container {
        text-align: center;
        padding: 20px 0;
        margin-bottom: 20px;
    }
    
    /* Success animation */
    @keyframes checkmark {
        0% {
            transform: scale(0);
        }
        50% {
            transform: scale(1.2);
        }
        100% {
            transform: scale(1);
        }
    }
    
    .success-checkmark {
        animation: checkmark 0.5s ease;
    }
    
    /* Warning banner */
    .warning-banner {
        background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(239, 68, 68, 0.2) 100%);
        border-left: 4px solid #F59E0B;
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
    }
    
    /* Info callout */
    .info-callout {
        background: rgba(99, 102, 241, 0.1);
        border-left: 4px solid #6366F1;
        padding: 16px;
        border-radius: 8px;
        margin: 16px 0;
    }
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)


def show_logo():
    """Display app logo"""
    logo_path = Path("logo.png")
    if logo_path.exists():
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.image(str(logo_path), use_container_width=True)
    else:
        st.markdown("<h1 style='text-align: center; color: #6366F1;'><i class='fas fa-shield-alt'></i> SafeWonder</h1>", unsafe_allow_html=True)


def show_emergency_modal():
    """Display emergency contacts modal"""
    country_data = get_session_value('country_data')
    
    if not country_data:
        st.error("⚠️ Country data not loaded. Please complete onboarding.")
        return
    
    st.markdown("### <i class='fas fa-ambulance'></i> Emergency Contacts", unsafe_allow_html=True)
    
    emergency_numbers = country_data.get('emergency_numbers', {})
    
    if emergency_numbers:
        cols = st.columns(2)
        idx = 0
        for service, number in emergency_numbers.items():
            with cols[idx % 2]:
                st.markdown(f"""
                <div class="custom-card">
                    <h4 style="color: #EF4444; margin: 0;">{service.replace('_', ' ').title()}</h4>
                    <h2 style="margin: 8px 0;">{number}</h2>
                    <a href="tel:{number}" style="text-decoration: none;">
                        <button style="background: #EF4444; color: white; border: none; padding: 8px 16px; border-radius: 6px; cursor: pointer;">
                            📞 Call Now
                        </button>
                    </a>
                </div>
                """, unsafe_allow_html=True)
            idx += 1
    
    # Important locations
    st.markdown("### <i class='fas fa-map-marker-alt'></i> Important Locations", unsafe_allow_html=True)
    
    locations = country_data.get('important_locations', {})
    
    if 'hospitals' in locations and locations['hospitals']:
        st.markdown("**<i class='fas fa-hospital'></i> Hospitals**", unsafe_allow_html=True)
        for hospital in locations['hospitals']:
            st.markdown(f"- **{hospital['name']}**: {hospital.get('contact', 'N/A')}")
    
    if 'police_stations' in locations and locations['police_stations']:
        st.markdown("**<i class='fas fa-shield-alt'></i> Police Stations**", unsafe_allow_html=True)
        for station in locations['police_stations']:
            st.markdown(f"- **{station['name']}**: {station.get('contact', 'N/A')}")
    
    if 'embassy' in locations and locations['embassy']:
        st.markdown("**<i class='fas fa-landmark'></i> Embassy Contacts**", unsafe_allow_html=True)
        for country, info in locations['embassy'].items():
            st.markdown(f"- **{country.upper()}**: {info.get('contact', 'N/A')}")
            if 'address' in info:
                st.markdown(f"  *{info['address']}*")


def show_navigation():
    """Display sidebar navigation"""
    with st.sidebar:
        show_logo()
        
        st.markdown("---")
        
        # Navigation menu
        current_page = get_session_value('current_page', 'home')
        
        # Navigation items
        nav_items = [
            ("home", "fa-home", "Home"),
            ("analyzer", "fa-exclamation-triangle", "Situation Analyzer"),
            ("translator", "fa-language", "Polite Translator"),
            ("ocr", "fa-camera", "OCR Translator"),
            ("settings", "fa-cog", "Profile Settings"),
            ("emergency", "fa-ambulance", "Emergency")
        ]
        
        # Create navigation buttons
        for page_id, icon, label in nav_items:
            is_active = current_page == page_id
            
            # Display icon and label as markdown above button
            st.markdown(f"""
                <div style="margin-bottom: -45px; pointer-events: none;">
                    <div style="
                        background: {'#6366F1' if is_active else 'rgba(30, 41, 59, 0.5)'};
                        border: {'2px solid #6366F1' if is_active else '1px solid rgba(99, 102, 241, 0.3)'};
                        border-radius: 8px;
                        padding: 12px 16px;
                        margin: 4px 0;
                        backdrop-filter: blur(10px);
                        transition: all 0.3s ease;
                    ">
                        <i class="fas {icon}" style="margin-right: 10px; width: 18px;"></i>
                        <span style="font-weight: {'600' if is_active else '400'};">{label}</span>
                    </div>
                </div>
            """, unsafe_allow_html=True)
            
            # Invisible button for click handling
            if st.button(label, key=f"nav_{page_id}", use_container_width=True, 
                        type="primary" if is_active else "secondary"):
                set_session_value('current_page', page_id)
                st.rerun()
        
        # Hide button text with CSS
        st.markdown("""
            <style>
            [data-testid="stSidebar"] .stButton button {
                opacity: 0.01;
                height: 48px;
                margin-top: -4px;
            }
            [data-testid="stSidebar"] .stButton button:hover {
                opacity: 0.05;
            }
            </style>
        """, unsafe_allow_html=True)
        
        st.markdown("---")
        
        # User info
        user_profile = get_session_value('user_profile')
        if user_profile:
            st.markdown(f"**<i class='fas fa-user'></i> {user_profile.get('name', 'User')}**", unsafe_allow_html=True)
            st.markdown(f"<i class='fas fa-map-marker-alt'></i> {user_profile.get('traveling_to_city', 'Unknown')}, {user_profile.get('traveling_to_country', 'Unknown')}", unsafe_allow_html=True)


def show_home_page():
    """Display home page"""
    st.markdown("# <i class='fas fa-shield-alt'></i> Welcome to SafeWonder!", unsafe_allow_html=True)
    
    user_profile = get_session_value('user_profile')
    if user_profile:
        st.markdown(f"### <i class='fas fa-hand-wave'></i> Hello, {user_profile.get('name')}!", unsafe_allow_html=True)
        st.markdown(f"<i class='fas fa-plane-departure'></i> You're traveling to **{user_profile.get('traveling_to_city')}**, **{user_profile.get('traveling_to_country')}**", unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Feature cards
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        <div class="custom-card">
            <h3><i class="fas fa-exclamation-triangle"></i> Situation Analyzer</h3>
            <p>Describe any situation and get instant risk assessment with safety recommendations.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card">
            <h3><i class="fas fa-language"></i> Polite Translator</h3>
            <p>Translate phrases with cultural context and pronunciation guidance.</p>
        </div>
        """, unsafe_allow_html=True)
    
    with col2:
        st.markdown("""
        <div class="custom-card">
            <h3><i class="fas fa-camera"></i> OCR Translator</h3>
            <p>Photograph signs, menus, or documents for instant translation and scam detection.</p>
        </div>
        """, unsafe_allow_html=True)
        
        st.markdown("""
        <div class="custom-card">
            <h3><i class="fas fa-ambulance"></i> Emergency</h3>
            <p>Quick access to emergency contacts, hospitals, and police stations.</p>
        </div>
        """, unsafe_allow_html=True)
    
    # Safety tips
    st.markdown("---")
    st.markdown("### <i class='fas fa-lightbulb'></i> Quick Safety Tips", unsafe_allow_html=True)
    
    country_data = get_session_value('country_data')
    if country_data and 'culture' in country_data:
        culture = country_data['culture']
        
        col1, col2 = st.columns(2)
        
        with col1:
            if 'dos' in culture:
                st.markdown("**<i class='fas fa-check-circle' style='color: #10B981;'></i> Do's**", unsafe_allow_html=True)
                for do in culture['dos']:
                    st.markdown(f"- {do}")
        
        with col2:
            if 'donts' in culture:
                st.markdown("**<i class='fas fa-times-circle' style='color: #EF4444;'></i> Don'ts**", unsafe_allow_html=True)
                for dont in culture['donts']:
                    st.markdown(f"- {dont}")


def main():
    """Main application entry point"""
    
    # Page configuration
    st.set_page_config(
        page_title="SafeWonder - Travel Safety Assistant",
        page_icon="🛡️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Load custom CSS
    load_custom_css()
    
    # Initialize session state
    initialize_session_state()
    
    # Get API key from Streamlit secrets or environment
    try:
        api_key = st.secrets.get("GROQ_API_KEY") or os.getenv("GROQ_API_KEY")
    except:
        api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.error("⚠️ GROQ_API_KEY not found. Please add it to Streamlit secrets or .env file.")
        st.stop()
    
    set_session_value('groq_api_key', api_key)
    
    # Load database
    try:
        database = load_database()
        set_session_value('database', database)
    except Exception as e:
        st.error(f"❌ Failed to load database: {str(e)}")
        st.stop()
    
    # Check if user has completed onboarding
    user_profile = get_session_value('user_profile')
    
    if not user_profile:
        # Show onboarding
        show_onboarding_screen()
    else:
        # Show navigation and main app
        show_navigation()
        
        # Route to appropriate page
        current_page = get_session_value('current_page', 'home')
        
        if current_page == 'home':
            show_home_page()
        elif current_page == 'analyzer':
            show_situation_analyzer()
        elif current_page == 'translator':
            show_culture_translator()
        elif current_page == 'ocr':
            show_ocr_translator()
        elif current_page == 'settings':
            show_profile_settings()
        elif current_page == 'emergency':
            show_emergency_modal()
        
        # Emergency button (floating)
        st.markdown("""
        <div class="emergency-button">
            <a href="?emergency=true" style="text-decoration: none;">
                <button style="background: #EF4444; color: white; border: none; padding: 16px; border-radius: 50%; font-size: 24px; cursor: pointer; box-shadow: 0 4px 12px rgba(239, 68, 68, 0.4);">
                    <i class="fas fa-ambulance"></i>
                </button>
            </a>
        </div>
        """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
