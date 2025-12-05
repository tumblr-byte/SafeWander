# SafeWander - Design Document

## Overview

SafeWander is a multi-feature travel safety platform built with Streamlit and powered by Grok AI. The system provides travelers with comprehensive pre-travel preparation, real-time safety intelligence, emergency support, and community-driven insights. The architecture is modular, allowing each feature to operate independently while sharing a common database and AI backbone.

The design prioritizes **accessibility** (works offline with cached data), **speed** (instant safety scores), and **personalization** (tailored advice based on traveler profile).

## Architecture

### High-Level System Design

```
┌─────────────────────────────────────────────────────────────┐
│                    Streamlit Frontend                        │
│  (Trip Planner | Safety Check | Voice | Emergency | Community)
└────────────────────┬────────────────────────────────────────┘
                     │
        ┌────────────┼────────────┐
        │            │            │
        ▼            ▼            ▼
    ┌────────┐  ┌─────────┐  ┌──────────┐
    │ Grok   │  │Database │  │ External │
    │  AI    │  │ (JSON)  │  │   APIs   │
    │ Engine │  │         │  │(Translate)
    └────────┘  └─────────┘  └──────────┘
```

### Data Flow

1. **User Input** → Streamlit UI captures traveler profile, location, situation
2. **Data Processing** → System queries database and AI engine
3. **Intelligence Generation** → Combines community data, AI analysis, and cultural context
4. **Output** → Personalized safety guidance, alerts, and recommendations

### Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **AI Engine**: Grok API (xAI) for contextual analysis
- **Database**: JSON file (database.json) for locations, reports, contacts
- **Translation**: Google Translate API (deep_translator library)
- **Speech**: pyttsx3 (text-to-speech), speech_recognition (voice input)
- **Image Processing**: Tesseract OCR (for document scanning)
- **Deployment**: Streamlit Cloud or Docker

## Components and Interfaces

### 1. Trip Planner Module

**Purpose**: Help travelers prepare before departure

**Key Components**:
- Destination information fetcher (uses Grok AI)
- Cultural context provider
- Pre-travel checklist generator
- Budget & logistics calculator

**Data Inputs**:
- Current location
- Destination
- Travel date
- Traveler profile (gender, age, experience)

**Data Outputs**:
- Currency & exchange information
- Hotel recommendations by safety & price
- Transport options & fair pricing
- Cultural do's and don'ts
- Pre-travel checklist

**AI Integration**: Grok generates personalized travel information based on traveler profile and destination

### 2. Real-Time Safety Module

**Purpose**: Provide instant safety assessment of current location

**Key Components**:
- Location safety scorer
- Time-of-day risk calculator
- Scam alert system
- Situational guidance generator
- Community report aggregator

**Data Inputs**:
- Current location
- Time of day
- Current situation (walking, taxi, restaurant, etc.)
- Traveler profile

**Data Outputs**:
- Safety score (1-10) with color coding
- Time-specific safety guidance
- Active scam alerts
- Nearby emergency contacts
- Relevant community reports

**Scoring Algorithm**:
```
Safety Score = (Base Location Score × 0.4) + 
               (Time Factor × 0.3) + 
               (Recent Reports Factor × 0.3)

Base Location Score: From database (1-10)
Time Factor: Adjusted for time of day (night = lower)
Recent Reports Factor: Based on community reports in last 7 days
```

### 3. Voice Translator Module

**Purpose**: Enable communication with locals in emergencies

**Key Components**:
- Speech-to-text converter
- Translation engine (Google Translate)
- Text-to-speech synthesizer
- Survival phrase library
- Context-specific phrase suggester

**Data Inputs**:
- User speech or text
- Target language
- Context (emergency, taxi, restaurant, etc.)

**Data Outputs**:
- Translated text
- Audio pronunciation
- Suggested phrases for context
- Emergency phrases in local language

**Supported Languages**: Hindi, Thai, Spanish, French, German, Japanese, Mandarin (expandable)

### 4. Emergency Module

**Purpose**: Provide immediate help in crisis situations

**Key Components**:
- Emergency contact directory
- SOS alert system
- Complaint filing system
- Crisis guidance generator
- Location sharing service

**Data Inputs**:
- Current location
- Emergency type (scam, harassment, theft, medical, etc.)
- Trusted contact information
- Incident details

**Data Outputs**:
- Emergency contacts (police, ambulance, hospital, embassy)
- SOS alert with location
- Step-by-step crisis guidance
- Complaint reference ID
- Follow-up resources

**Emergency Contact Structure**:
```json
{
  "location": "Bangkok, Thailand",
  "emergency_contacts": {
    "police": "+66-1191",
    "ambulance": "+66-1669",
    "fire": "+66-1199",
    "women_helpline": "+66-1300",
    "tourist_police": "+66-4-281-5051",
    "embassy": "+66-2-xxx-xxxx"
  }
}
```

### 5. Community Module

**Purpose**: Aggregate and share traveler experiences

**Key Components**:
- Report submission system
- Report verification engine
- Search & filter system
- Upvote/rating system
- Report aggregator

**Data Inputs**:
- Report type (scam, safe spot, tip, incident)
- Location
- Description
- Evidence (photos/videos)
- Reporter profile

**Data Outputs**:
- Verified community reports
- Trending alerts
- Location-specific insights
- Highly-rated tips

**Report Structure**:
```json
{
  "id": "unique_id",
  "type": "scam|safe_spot|tip|incident",
  "location": "Khao San Road, Bangkok",
  "title": "Gem Shop Scam",
  "description": "Overpriced stones, fake quality",
  "upvotes": 45,
  "verified": true,
  "reported_by": "traveler_123",
  "timestamp": "2025-12-04T10:30:00Z",
  "evidence": ["photo_url_1", "photo_url_2"]
}
```

## Data Models

### Traveler Profile

```python
{
  "id": "unique_traveler_id",
  "gender": "Male|Female|Other|Prefer not to say",
  "age_group": "18-25|26-35|36-50|50+",
  "experience": "First time|Occasional|Frequent",
  "traveler_type": "Solo|Couple|Group|Family",
  "home_country": "Country",
  "languages_spoken": ["English", "Spanish"],
  "accessibility_needs": ["wheelchair", "dietary"],
  "trusted_contacts": [
    {
      "name": "Contact Name",
      "phone": "+1-xxx-xxx-xxxx",
      "email": "email@example.com",
      "relationship": "Friend|Family|Emergency"
    }
  ]
}
```

### Location Database

```python
{
  "location_name": "Bangkok, Thailand",
  "country": "Thailand",
  "coordinates": {"lat": 13.7563, "lon": 100.5018},
  "safety_score": 7.5,
  "safe_at_night": false,
  "currency": "Thai Baht (THB)",
  "exchange_rate": "1 USD = 35 THB",
  "money": {
    "safe_exchange": ["Bank of Thailand", "Authorized ATMs"],
    "roaming": "Available from major carriers",
    "money_transfer": ["Western Union", "Wise"]
  },
  "hotels": {
    "budget": {
      "price_range": "$10-30/night",
      "safe_areas": ["Sukhumvit", "Silom"],
      "recommendations": ["Lub d", "NapPark"]
    },
    "mid_range": {
      "price_range": "$30-80/night",
      "safe_areas": ["Thonglor", "Ekkamai"],
      "recommendations": ["Citadines", "Hua Mark"]
    }
  },
  "transport": {
    "taxi_base": "35 THB",
    "taxi_per_km": "5.5 THB",
    "recommended": ["Grab", "BTS Skytrain"],
    "avoid": ["Unmarked taxis"]
  },
  "emergency_contacts": {
    "police": "+66-1191",
    "ambulance": "+66-1669",
    "fire": "+66-1199",
    "women_helpline": "+66-1300",
    "tourist_police": "+66-4-281-5051",
    "embassy": "+66-2-xxx-xxxx"
  },
  "common_scams": [
    "Gem shop overpricing",
    "Tuk-tuk overcharging",
    "Fake tour operators",
    "Drink spiking in bars"
  ],
  "cultural_context": {
    "dos": [
      "Remove shoes before entering homes/temples",
      "Show respect to elders",
      "Learn basic greetings"
    ],
    "donts": [
      "Point feet at Buddha images",
      "Touch people's heads",
      "Raise voice in public"
    ]
  },
  "survival_phrases": {
    "emergency": {
      "help": "ช่วยด้วย (Chuay duay)",
      "police": "ตำรวจ (Tamruat)",
      "hospital": "โรงพยาบาล (Rong phayaban)"
    },
    "directions": {
      "where_is": "ที่ไหน (Thi nai)",
      "how_much": "เท่าไหร่ (Thao rai)"
    }
  }
}
```

### Community Report

```python
{
  "id": "report_unique_id",
  "type": "scam|safe_spot|tip|incident",
  "location": "Khao San Road, Bangkok",
  "title": "Gem Shop Scam",
  "description": "Overpriced stones, fake quality. Avoid shops with touts.",
  "upvotes": 45,
  "downvotes": 2,
  "verified": true,
  "verification_count": 5,
  "reported_by": "traveler_123",
  "reporter_profile": {
    "gender": "Female",
    "experience": "Frequent",
    "home_country": "USA"
  },
  "timestamp": "2025-12-04T10:30:00Z",
  "evidence": [
    {
      "type": "photo|video|document",
      "url": "https://..."
    }
  ],
  "comments": [
    {
      "author": "local_bangkok_456",
      "text": "Confirmed! Happened to me too.",
      "timestamp": "2025-12-04T11:00:00Z"
    }
  ]
}
```

## Error Handling

### API Failures

**Grok API Down**:
- Fall back to cached responses
- Display offline mode message
- Provide generic safety guidance

**Translation API Failure**:
- Show cached translations
- Provide phonetic alternatives
- Suggest using phrase cards

**Database Unavailable**:
- Load from local cache
- Disable community features
- Show last-known data

### User Input Validation

- Location validation: Check against known locations database
- Phone number validation: Ensure proper format
- Report validation: Check for spam/abuse patterns
- Profile validation: Ensure required fields are complete

### Error Messages

- **Clear**: "We couldn't reach the Grok API. Using offline mode."
- **Actionable**: "Please check your internet connection and try again."
- **Helpful**: "In the meantime, here are emergency contacts for your location."

## Testing Strategy

### Unit Tests

1. **Safety Score Calculation**
   - Test scoring algorithm with various inputs
   - Verify time-of-day adjustments
   - Validate report weighting

2. **Translation Engine**
   - Test phrase translation accuracy
   - Verify language detection
   - Validate audio output

3. **Data Validation**
   - Test location validation
   - Verify profile completeness
   - Validate report structure

### Integration Tests

1. **End-to-End Trip Planning**
   - User enters destination → System provides full trip info
   - Verify all components (currency, hotels, transport, culture) are populated

2. **Real-Time Safety Check**
   - User enters location → System calculates safety score
   - Verify score reflects community reports and time of day

3. **Emergency Flow**
   - User triggers SOS → Location shared, contacts notified
   - Verify all emergency contacts are displayed

4. **Community Reporting**
   - User submits report → Report appears in community feed
   - Verify report is searchable and voteable

### User Acceptance Tests

1. **Usability**: Can a first-time traveler navigate all features?
2. **Accuracy**: Are safety scores and recommendations accurate?
3. **Responsiveness**: Does the app respond quickly to user input?
4. **Accessibility**: Can users with different abilities use the app?

## Key Design Decisions

### 1. JSON Database vs. Cloud Database
**Decision**: Use JSON file for MVP, migrate to cloud later
**Rationale**: Faster development, works offline, easier to demo

### 2. Grok AI for Contextual Guidance
**Decision**: Use Grok instead of generic LLM
**Rationale**: Grok is real-time, can handle current events, good for travel context

### 3. Streamlit for Frontend
**Decision**: Keep Streamlit instead of building custom UI
**Rationale**: Fast development, good for hackathon, easy to deploy

### 4. Community-Driven Safety Scores
**Decision**: Weight community reports heavily in safety calculations
**Rationale**: Real traveler experiences are most valuable for safety

### 5. Modular Architecture
**Decision**: Each feature (Trip Planner, Safety, Voice, Emergency, Community) operates independently
**Rationale**: Easier to test, scale, and add new features

## Deployment Considerations

- **Streamlit Cloud**: Free hosting, automatic updates
- **Docker**: For self-hosted deployments
- **Environment Variables**: Store API keys securely
- **Database Backup**: Regular JSON exports
- **Monitoring**: Track API usage and errors

