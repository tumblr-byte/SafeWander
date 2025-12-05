"""Situation analyzer for SafeWonder - AI-powered safety assessment."""
import json
import streamlit as st
from dataclasses import dataclass
from typing import List, Dict, Any, Optional
from utils.groq_client import GroqClient
from utils.database_loader import get_scams, get_harassment_patterns, get_cultural_info, get_local_phrases, get_emergency_numbers


@dataclass
class SituationAnalysis:
    """Situation analysis result data structure."""
    risk_score: int
    pattern_matched: str
    risk_explanation: str
    what_to_do: List[str]
    what_not_to_do: List[str]
    emergency_numbers: Dict[str, str]
    local_phrases: Dict[str, str]
    cultural_notes: str


def match_keywords(description: str, scams: list, harassment: list) -> List[Dict[str, Any]]:
    """
    Match situation keywords against scams and harassment patterns.
    
    Args:
        description: User's situation description
        scams: List of scam patterns from database
        harassment: List of harassment patterns from database
        
    Returns:
        List of matched patterns
    """
    description_lower = description.lower()
    matched_patterns = []
    
    # Check scams
    for scam in scams:
        keywords = scam.get('situation_keywords', [])
        for keyword in keywords:
            if keyword.lower() in description_lower:
                matched_patterns.append({
                    'type': 'scam',
                    'name': scam.get('name', 'Unknown Scam'),
                    'data': scam
                })
                break
    
    # Check harassment patterns
    for pattern in harassment:
        name_lower = pattern.get('name', '').lower()
        desc_lower = pattern.get('description', '').lower()
        
        # Simple keyword matching from name and description
        keywords = name_lower.split() + desc_lower.split()
        for keyword in keywords:
            if len(keyword) > 3 and keyword in description_lower:
                matched_patterns.append({
                    'type': 'harassment',
                    'name': pattern.get('name', 'Unknown Pattern'),
                    'data': pattern
                })
                break
    
    return matched_patterns


def build_groq_prompt(description: str, country_data: Dict[str, Any], user_profile: Dict[str, Any], matched_patterns: List[Dict[str, Any]]) -> str:
    """
    Build intelligent prompt for Groq API.
    
    Args:
        description: User's situation description
        country_data: Country-specific data from database
        user_profile: User profile information
        matched_patterns: Pre-matched patterns from keyword search
        
    Returns:
        Formatted prompt string
    """
    scams = get_scams(country_data)
    harassment = get_harassment_patterns(country_data)
    culture = get_cultural_info(country_data)
    phrases = get_local_phrases(country_data)
    emergency = get_emergency_numbers(country_data)
    
    prompt = f"""You are a Safety AI assistant for travelers. Analyze the following situation:

USER SITUATION: {description}

TRAVELER PROFILE:
- Gender: {user_profile.get('gender', 'Not specified')}
- Native Language: {user_profile.get('native_language', 'English')}
- Destination: {country_data.get('name', 'Unknown')}, {user_profile.get('traveling_to_city', 'Unknown')}

KNOWLEDGE BASE CONTEXT:

Common Scams in this country:
{json.dumps(scams, indent=2)}

Harassment Patterns:
{json.dumps(harassment, indent=2)}

Cultural Rules:
{json.dumps(culture, indent=2)}

Local Emergency Phrases:
{json.dumps(phrases, indent=2)}

Emergency Numbers:
{json.dumps(emergency, indent=2)}

PRE-MATCHED PATTERNS:
{json.dumps([p['name'] for p in matched_patterns], indent=2) if matched_patterns else "None"}

TASK:
1. Analyze if this situation matches any scam, harassment, or cultural misunderstanding
2. Assess risk level (0-100):
   - 0-30: Low risk (normal situation, minor concern)
   - 31-60: Medium risk (caution advised, potential issue)
   - 61-100: High risk (immediate action needed, dangerous)
3. Provide specific, actionable steps from the knowledge base
4. Add intelligent reasoning beyond the JSON data
5. Include relevant emergency contacts and cultural guidance

OUTPUT FORMAT (respond ONLY with valid JSON):
{{
  "risk_score": <number 0-100>,
  "pattern_matched": "<name of matched pattern or 'General Safety Concern'>",
  "risk_explanation": "<clear explanation of why this is risky or not>",
  "what_to_do": ["<specific action 1>", "<specific action 2>", "<specific action 3>"],
  "what_not_to_do": ["<what to avoid 1>", "<what to avoid 2>"],
  "cultural_notes": "<relevant cultural context or 'No specific cultural concerns'>"
}}

Remember: Be specific, actionable, and prioritize traveler safety."""
    
    return prompt


def calculate_risk_score(groq_response: Dict[str, Any], matched_patterns: List[Dict[str, Any]]) -> int:
    """
    Determine risk level from Groq response and matched patterns.
    
    Args:
        groq_response: Parsed response from Groq API
        matched_patterns: List of matched patterns
        
    Returns:
        Risk score 0-100
    """
    # Get risk score from Groq response
    risk_score = groq_response.get('risk_score', 50)
    
    # Adjust based on matched patterns
    if matched_patterns:
        # If scam detected, ensure minimum risk of 40
        if any(p['type'] == 'scam' for p in matched_patterns):
            risk_score = max(risk_score, 40)
        
        # If harassment detected, ensure minimum risk of 50
        if any(p['type'] == 'harassment' for p in matched_patterns):
            risk_score = max(risk_score, 50)
    
    # Ensure within bounds
    return max(0, min(100, risk_score))


def analyze_situation(description: str, country_data: Dict[str, Any], user_profile: Dict[str, Any], groq_client: GroqClient) -> Optional[SituationAnalysis]:
    """
    Analyze user situation and provide safety recommendations.
    
    Args:
        description: User's situation description
        country_data: Country-specific data from database
        user_profile: User profile information
        groq_client: Initialized Groq API client
        
    Returns:
        SituationAnalysis object or None if analysis fails
    """
    if not description or len(description.strip()) < 10:
        st.warning("⚠️ Please provide a more detailed description of your situation.")
        return None
    
    # Match keywords against database
    scams = get_scams(country_data)
    harassment = get_harassment_patterns(country_data)
    matched_patterns = match_keywords(description, scams, harassment)
    
    # Build prompt
    prompt = build_groq_prompt(description, country_data, user_profile, matched_patterns)
    
    # Call Groq API
    with st.spinner("🤖 Analyzing your situation..."):
        response_text = groq_client.call_api(prompt, temperature=0.5)
    
    if not response_text:
        st.error("❌ Failed to analyze situation. Please try again.")
        return None
    
    # Parse response
    try:
        # Extract JSON from response (handle markdown code blocks)
        if "```json" in response_text:
            response_text = response_text.split("```json")[1].split("```")[0].strip()
        elif "```" in response_text:
            response_text = response_text.split("```")[1].split("```")[0].strip()
        
        groq_response = json.loads(response_text)
        
        # Calculate final risk score
        risk_score = calculate_risk_score(groq_response, matched_patterns)
        
        # Get emergency info
        emergency_numbers = get_emergency_numbers(country_data)
        local_phrases = get_local_phrases(country_data)
        
        # Create analysis object
        analysis = SituationAnalysis(
            risk_score=risk_score,
            pattern_matched=groq_response.get('pattern_matched', 'General Safety Concern'),
            risk_explanation=groq_response.get('risk_explanation', 'Unable to determine risk level'),
            what_to_do=groq_response.get('what_to_do', ['Stay calm', 'Assess your surroundings', 'Contact local authorities if needed']),
            what_not_to_do=groq_response.get('what_not_to_do', ['Don\'t panic', 'Don\'t engage with suspicious individuals']),
            emergency_numbers=emergency_numbers,
            local_phrases=local_phrases,
            cultural_notes=groq_response.get('cultural_notes', 'No specific cultural concerns identified')
        )
        
        return analysis
        
    except json.JSONDecodeError as e:
        st.error(f"❌ Failed to parse AI response: {str(e)}")
        st.code(response_text)
        return None
    except Exception as e:
        st.error(f"❌ Error during analysis: {str(e)}")
        return None
