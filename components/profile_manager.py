"""User profile management and onboarding for SafeWonder."""
import streamlit as st
from dataclasses import dataclass
from datetime import date
from typing import Tuple, Optional
from utils.database_loader import load_database, get_country_data, get_all_countries
from utils.session_manager import save_user_profile, save_country_data


@dataclass
class UserProfile:
    """User profile data structure."""
    name: str
    native_language: str
    traveling_to_country: str
    traveling_to_city: str
    arrival_date: str
    gender: str
    safety_preference: str


def validate_profile(profile: dict) -> Tuple[bool, str]:
    """
    Validate profile data completeness and format.
    
    Args:
        profile: Profile dictionary to validate
        
    Returns:
        Tuple of (is_valid, error_message)
    """
    required_fields = [
        'name', 'native_language', 'traveling_to_country',
        'traveling_to_city', 'arrival_date', 'gender', 'safety_preference'
    ]
    
    for field in required_fields:
        if field not in profile or not profile[field]:
            return False, f"Please fill in your {field.replace('_', ' ')}"
    
    if len(profile['name']) < 2:
        return False, "Name must be at least 2 characters"
    
    return True, ""


def show_onboarding_screen():
    """Display onboarding form and collect user profile data."""
    
    # Load database for country selection
    database = load_database()
    countries = get_all_countries(database)
    
    st.markdown("""
        <style>
        .onboarding-container {
            max-width: 800px;
            margin: 0 auto;
            padding: 2rem;
        }
        .welcome-text {
            text-align: center;
            font-size: 2.5rem;
            font-weight: bold;
            margin-bottom: 1rem;
            background: linear-gradient(135deg, #6366F1 0%, #EC4899 100%);
            -webkit-background-clip: text;
            -webkit-text-fill-color: transparent;
            animation: fadeIn 1s ease-in;
        }
        .subtitle {
            text-align: center;
            font-size: 1.2rem;
            color: #94A3B8;
            margin-bottom: 2rem;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(-20px); }
            to { opacity: 1; transform: translateY(0); }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Welcome header
    st.markdown('<div class="welcome-text">✈️ Welcome to SafeWonder</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your AI-powered travel safety companion</div>', unsafe_allow_html=True)
    
    st.markdown("---")
    
    # Create form
    with st.form("onboarding_form"):
        st.subheader("📋 Tell us about your trip")
        
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input(
                "👤 Your Name",
                placeholder="Enter your name",
                help="We'll use this to personalize your experience"
            )
            
            native_language = st.selectbox(
                "🗣️ Native Language",
                options=[
                    "English", "Spanish", "French", "German", "Italian",
                    "Portuguese", "Hindi", "Japanese", "Korean", "Chinese",
                    "Arabic", "Russian", "Other"
                ],
                help="Your primary language for translations"
            )
            
            gender = st.selectbox(
                "⚧ Gender",
                options=["Female", "Male", "Non-binary", "Prefer not to say"],
                help="Helps us provide relevant safety guidance"
            )
        
        with col2:
            country_options = {c['name']: c['id'] for c in countries if c['name']}
            traveling_to_country_name = st.selectbox(
                "🌍 Destination Country",
                options=list(country_options.keys()),
                help="Where are you traveling to?"
            )
            
            traveling_to_city = st.text_input(
                "🏙️ Destination City",
                placeholder="e.g., Delhi, Tokyo, New York",
                help="Main city you'll be visiting"
            )
            
            arrival_date = st.date_input(
                "📅 Arrival Date",
                value=date.today(),
                help="When do you arrive?"
            )
        
        safety_preference = st.radio(
            "🛡️ Safety Alert Preference",
            options=["Cautious (All warnings)", "Balanced (Important warnings)", "Minimal (Critical only)"],
            help="How much safety information do you want to see?",
            horizontal=True
        )
        
        st.markdown("---")
        
        submitted = st.form_submit_button(
            "🚀 Start My Safe Journey",
            use_container_width=True,
            type="primary"
        )
        
        if submitted:
            # Get country ID from selection
            traveling_to_country = country_options.get(traveling_to_country_name, "")
            
            # Create profile dictionary
            profile = {
                'name': name,
                'native_language': native_language,
                'traveling_to_country': traveling_to_country,
                'traveling_to_city': traveling_to_city,
                'arrival_date': str(arrival_date),
                'gender': gender,
                'safety_preference': safety_preference
            }
            
            # Validate profile
            is_valid, error_msg = validate_profile(profile)
            
            if is_valid:
                # Load country data
                country_data = get_country_data(database, traveling_to_country)
                
                if country_data:
                    # Save to session
                    save_user_profile(profile)
                    save_country_data(country_data)
                    
                    st.success(f"✅ Welcome aboard, {name}! Your profile is ready.")
                    st.balloons()
                    st.rerun()
                else:
                    st.error(f"❌ Sorry, we don't have safety data for {traveling_to_country_name} yet.")
            else:
                st.error(f"❌ {error_msg}")


def show_profile_settings():
    """Display and allow editing of user profile."""
    from utils.session_manager import get_user_profile
    
    profile = get_user_profile()
    
    if not profile:
        st.warning("⚠️ No profile found. Please complete onboarding first.")
        return
    
    st.subheader("⚙️ Profile Settings")
    
    database = load_database()
    countries = get_all_countries(database)
    
    with st.form("profile_edit_form"):
        col1, col2 = st.columns(2)
        
        with col1:
            name = st.text_input("👤 Name", value=profile.get('name', ''))
            native_language = st.selectbox(
                "🗣️ Native Language",
                options=[
                    "English", "Spanish", "French", "German", "Italian",
                    "Portuguese", "Hindi", "Japanese", "Korean", "Chinese",
                    "Arabic", "Russian", "Other"
                ],
                index=0 if not profile.get('native_language') else 
                      ["English", "Spanish", "French", "German", "Italian",
                       "Portuguese", "Hindi", "Japanese", "Korean", "Chinese",
                       "Arabic", "Russian", "Other"].index(profile.get('native_language', 'English'))
            )
            gender = st.selectbox(
                "⚧ Gender",
                options=["Female", "Male", "Non-binary", "Prefer not to say"],
                index=["Female", "Male", "Non-binary", "Prefer not to say"].index(
                    profile.get('gender', 'Prefer not to say')
                )
            )
        
        with col2:
            country_options = {c['name']: c['id'] for c in countries if c['name']}
            current_country_name = next(
                (c['name'] for c in countries if c['id'] == profile.get('traveling_to_country')),
                list(country_options.keys())[0]
            )
            
            traveling_to_country_name = st.selectbox(
                "🌍 Destination Country",
                options=list(country_options.keys()),
                index=list(country_options.keys()).index(current_country_name)
            )
            
            traveling_to_city = st.text_input(
                "🏙️ Destination City",
                value=profile.get('traveling_to_city', '')
            )
            
            arrival_date = st.date_input(
                "📅 Arrival Date",
                value=date.today()
            )
        
        safety_preference = st.radio(
            "🛡️ Safety Alert Preference",
            options=["Cautious (All warnings)", "Balanced (Important warnings)", "Minimal (Critical only)"],
            index=["Cautious (All warnings)", "Balanced (Important warnings)", "Minimal (Critical only)"].index(
                profile.get('safety_preference', 'Balanced (Important warnings)')
            ),
            horizontal=True
        )
        
        if st.form_submit_button("💾 Save Changes", use_container_width=True, type="primary"):
            traveling_to_country = country_options.get(traveling_to_country_name, "")
            
            updated_profile = {
                'name': name,
                'native_language': native_language,
                'traveling_to_country': traveling_to_country,
                'traveling_to_city': traveling_to_city,
                'arrival_date': str(arrival_date),
                'gender': gender,
                'safety_preference': safety_preference
            }
            
            is_valid, error_msg = validate_profile(updated_profile)
            
            if is_valid:
                country_data = get_country_data(database, traveling_to_country)
                if country_data:
                    save_user_profile(updated_profile)
                    save_country_data(country_data)
                    st.success("✅ Profile updated successfully!")
                    st.rerun()
                else:
                    st.error(f"❌ No data available for {traveling_to_country_name}")
            else:
                st.error(f"❌ {error_msg}")
