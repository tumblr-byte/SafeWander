"""Session state manager for SafeWonder application."""
import streamlit as st
from typing import Optional, Dict, Any


def initialize_session_state():
    """Initialize all session state variables on first load."""
    
    # User profile
    if 'profile_completed' not in st.session_state:
        st.session_state.profile_completed = False
    
    if 'user_profile' not in st.session_state:
        st.session_state.user_profile = {}
    
    if 'country_data' not in st.session_state:
        st.session_state.country_data = None
    
    # Navigation
    if 'current_page' not in st.session_state:
        st.session_state.current_page = 'home'
    
    # Feature states
    if 'situation_history' not in st.session_state:
        st.session_state.situation_history = []
    
    if 'translation_cache' not in st.session_state:
        st.session_state.translation_cache = {}
    
    if 'ocr_results' not in st.session_state:
        st.session_state.ocr_results = []


def save_user_profile(profile: Dict[str, Any]):
    """
    Save user profile to session state.
    
    Args:
        profile: User profile dictionary
    """
    st.session_state.user_profile = profile
    st.session_state.profile_completed = True


def get_user_profile() -> Optional[Dict[str, Any]]:
    """
    Retrieve user profile from session state.
    
    Returns:
        User profile dictionary or None if not set
    """
    if st.session_state.profile_completed:
        return st.session_state.user_profile
    return None


def save_country_data(country_data: Dict[str, Any]):
    """
    Save country data to session state.
    
    Args:
        country_data: Country-specific data from database
    """
    st.session_state.country_data = country_data


def get_country_data() -> Optional[Dict[str, Any]]:
    """
    Retrieve country data from session state.
    
    Returns:
        Country data dictionary or None if not set
    """
    return st.session_state.country_data


def set_current_page(page: str):
    """
    Set the current active page.
    
    Args:
        page: Page identifier
    """
    st.session_state.current_page = page


def get_current_page() -> str:
    """
    Get the current active page.
    
    Returns:
        Current page identifier
    """
    return st.session_state.current_page


def add_situation_to_history(situation: Dict[str, Any]):
    """
    Add analyzed situation to history.
    
    Args:
        situation: Situation analysis result
    """
    st.session_state.situation_history.append(situation)


def cache_translation(key: str, translation: Dict[str, Any]):
    """
    Cache translation result to avoid redundant API calls.
    
    Args:
        key: Cache key (typically the source text)
        translation: Translation result dictionary
    """
    st.session_state.translation_cache[key] = translation


def get_cached_translation(key: str) -> Optional[Dict[str, Any]]:
    """
    Retrieve cached translation if available.
    
    Args:
        key: Cache key
        
    Returns:
        Cached translation or None
    """
    return st.session_state.translation_cache.get(key)


def is_profile_completed() -> bool:
    """
    Check if user has completed onboarding.
    
    Returns:
        True if profile is completed, False otherwise
    """
    return st.session_state.profile_completed
