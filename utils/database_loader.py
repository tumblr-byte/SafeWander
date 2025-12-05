"""Database loader utility for SafeWonder knowledge base."""
import json
import streamlit as st
from typing import Optional, Dict, Any


@st.cache_data
def load_database(db_path: str = "database.json") -> Dict[str, Any]:
    """
    Load and parse the database.json file.
    
    Args:
        db_path: Path to the database JSON file
        
    Returns:
        Parsed database dictionary
        
    Raises:
        FileNotFoundError: If database file doesn't exist
        json.JSONDecodeError: If JSON is malformed
    """
    try:
        with open(db_path, 'r', encoding='utf-8') as f:
            data = json.load(f)
        return data
    except FileNotFoundError:
        st.error(f"❌ Database file not found at: {db_path}")
        return {"countries": []}
    except json.JSONDecodeError as e:
        st.error(f"❌ Invalid JSON in database file: {str(e)}")
        return {"countries": []}


def get_country_data(database: Dict[str, Any], country_id: str) -> Optional[Dict[str, Any]]:
    """
    Filter and retrieve specific country data by country ID.
    
    Args:
        database: The loaded database dictionary
        country_id: Country ID to filter (e.g., 'IND', 'JPN', 'USA')
        
    Returns:
        Country data dictionary or None if not found
    """
    countries = database.get("countries", [])
    for country in countries:
        if country.get("id") == country_id:
            return country
    return None


def get_all_countries(database: Dict[str, Any]) -> list:
    """
    Get list of all available countries.
    
    Args:
        database: The loaded database dictionary
        
    Returns:
        List of country dictionaries with id and name
    """
    countries = database.get("countries", [])
    return [{"id": c.get("id"), "name": c.get("name")} for c in countries]


def get_emergency_numbers(country_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract emergency numbers from country data.
    
    Args:
        country_data: Country-specific data dictionary
        
    Returns:
        Dictionary of emergency contact numbers
    """
    return country_data.get("emergency_numbers", {})


def get_scams(country_data: Dict[str, Any]) -> list:
    """
    Extract common scams from country data.
    
    Args:
        country_data: Country-specific data dictionary
        
    Returns:
        List of scam dictionaries
    """
    return country_data.get("common_scams", [])


def get_harassment_patterns(country_data: Dict[str, Any]) -> list:
    """
    Extract harassment patterns from country data.
    
    Args:
        country_data: Country-specific data dictionary
        
    Returns:
        List of harassment pattern dictionaries
    """
    harassment = country_data.get("harassment_patterns", {})
    return harassment.get("examples", [])


def get_cultural_info(country_data: Dict[str, Any]) -> Dict[str, Any]:
    """
    Extract cultural information from country data.
    
    Args:
        country_data: Country-specific data dictionary
        
    Returns:
        Dictionary with cultural dos, donts, greetings, etc.
    """
    return country_data.get("culture", {})


def get_local_phrases(country_data: Dict[str, Any]) -> Dict[str, str]:
    """
    Extract local phrases from country data.
    
    Args:
        country_data: Country-specific data dictionary
        
    Returns:
        Dictionary of common phrases in local language
    """
    return country_data.get("local_phrases", {})
