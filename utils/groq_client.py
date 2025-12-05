"""Groq API client wrapper with retry logic and error handling."""
import time
import streamlit as st
from groq import Groq
from typing import Optional, Dict, Any


class GroqClient:
    """Wrapper for Groq API with retry logic and error handling."""
    
    def __init__(self, api_key: str):
        """
        Initialize Groq client.
        
        Args:
            api_key: Groq API key
            
        Raises:
            ValueError: If API key is empty or invalid
        """
        if not api_key or api_key.strip() == "":
            raise ValueError("Groq API key is required")
        
        self.client = Groq(api_key=api_key)
        self.model = "llama-3.1-70b-versatile"
    
    def call_api(
        self,
        prompt: str,
        max_retries: int = 3,
        temperature: float = 0.7,
        max_tokens: int = 2000
    ) -> Optional[str]:
        """
        Call Groq API with retry logic and exponential backoff.
        
        Args:
            prompt: The prompt to send to the API
            max_retries: Maximum number of retry attempts
            temperature: Sampling temperature (0-2)
            max_tokens: Maximum tokens in response
            
        Returns:
            API response text or None if all retries fail
        """
        for attempt in range(max_retries):
            try:
                response = self.client.chat.completions.create(
                    model=self.model,
                    messages=[
                        {
                            "role": "system",
                            "content": "You are a helpful travel safety assistant. Provide accurate, actionable advice."
                        },
                        {
                            "role": "user",
                            "content": prompt
                        }
                    ],
                    temperature=temperature,
                    max_tokens=max_tokens
                )
                
                return response.choices[0].message.content
                
            except Exception as e:
                error_msg = str(e)
                
                # Handle rate limit errors
                if "rate_limit" in error_msg.lower():
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt) * 2  # Exponential backoff
                        st.warning(f"⏳ Rate limit reached. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        st.error("❌ Rate limit exceeded. Please try again later.")
                        return None
                
                # Handle timeout errors
                elif "timeout" in error_msg.lower():
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt)
                        st.warning(f"⏳ Request timeout. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        st.error("❌ Request timeout. Please check your connection.")
                        return None
                
                # Handle authentication errors
                elif "authentication" in error_msg.lower() or "api key" in error_msg.lower():
                    st.error("❌ Invalid API key. Please check your Groq API key in Streamlit secrets.")
                    return None
                
                # Handle other errors
                else:
                    if attempt < max_retries - 1:
                        wait_time = (2 ** attempt)
                        st.warning(f"⚠️ Error occurred. Retrying in {wait_time} seconds...")
                        time.sleep(wait_time)
                        continue
                    else:
                        st.error(f"❌ API Error: {error_msg}")
                        return None
        
        return None


def get_groq_client() -> Optional[GroqClient]:
    """
    Get or create Groq client from Streamlit secrets or environment.
    
    Returns:
        GroqClient instance or None if API key not found
    """
    api_key = None
    
    # Try to get from Streamlit secrets first
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except:
        pass
    
    # Fallback to environment variable
    if not api_key:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key:
        st.error("❌ Groq API key not found. Please add GROQ_API_KEY to Streamlit secrets or .env file.")
        return None
    
    try:
        return GroqClient(api_key)
    except ValueError as e:
        st.error(f"❌ {str(e)}")
        return None


def validate_api_key() -> bool:
    """
    Validate that Groq API key is available and valid.
    
    Returns:
        True if API key is valid, False otherwise
    """
    api_key = None
    
    # Try to get from Streamlit secrets first
    try:
        api_key = st.secrets.get("GROQ_API_KEY")
    except:
        pass
    
    # Fallback to environment variable
    if not api_key:
        import os
        from dotenv import load_dotenv
        load_dotenv()
        api_key = os.getenv("GROQ_API_KEY")
    
    if not api_key or api_key.strip() == "":
        return False
    
    return True
