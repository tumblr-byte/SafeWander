# SafeWander

"Wander far, stay safe wherever you are."

AI-powered travel safety companion for tourists and solo travelers.

## Problem Statement

Millions of tourists face safety challenges when traveling to unfamiliar destinations - from transport scams and language barriers to emergency situations where they don't know local emergency numbers or how to communicate with authorities. Solo travelers, especially women, face additional safety concerns.

## Solution

SafeWander is an AI-powered safety companion that provides real-time protection and guidance for travelers through:

- SOS Emergency System with officer dispatch
- Scam Price Checker with local rate validation
- Essential Phrases with text-to-speech
- Cultural Guide for respectful travel
- Live Safety Map with police stations
- AI Safety Assistant for personalized advice

## Supported Countries

India, Thailand, Mexico, USA, Brazil

## Tech Stack

| Component | Technology |
|-----------|------------|
| Frontend | Streamlit |
| AI Model | Groq API (Llama 3.3 70B) |
| Maps | Leaflet.js + OpenStreetMap |
| Text-to-Speech | Web Speech API |
| Icons | Font Awesome 6.4 |
| Styling | Custom CSS |

## Architecture

```
User Input (Profile)
       |
       v
+------------------+
|   Streamlit UI   |
+------------------+
       |
       +---> SOS Module ---> Officer Dispatch + Safety Instructions
       |
       +---> Scam Checker ---> Price Validation (Local Thresholds)
       |
       +---> Phrases ---> Text-to-Speech (Web Speech API)
       |
       +---> Cultural Guide ---> Dataset Lookup
       |
       +---> AI Assistant ---> Groq API (Llama 3.3) ---> Personalized Response
       |
       +---> Safety Map ---> Leaflet.js + Police Station Data
```

## How AI is Used (RAG Implementation)

The AI component uses Retrieval-Augmented Generation (RAG) with Groq's Llama 3.3 70B model.

### RAG Pipeline:

1. User asks a safety question
2. System retrieves relevant context from dataset.json:
   - Transport scams for current country
   - Harassment safety protocols
   - Cultural guidelines
   - Emergency numbers
   - Area-specific warnings
   - Food safety tips
3. Retrieved context is injected into the AI prompt
4. AI generates response using both its knowledge AND local dataset

### What AI Receives:

- User profile (name, gender, age range)
- Current destination (country, city)
- Retrieved local knowledge (scams, emergency numbers, cultural tips)
- User's safety question

This RAG approach ensures the AI gives location-specific advice based on real local data, not just general knowledge. For example, asking about taxi safety in Delhi will reference specific auto-rickshaw scams from the dataset.

## Setup

1. Clone the repository
```
git clone https://github.com/tumblr-byte/SafeWander.git
cd SafeWander
```

2. Install dependencies
```
pip install -r requirements.txt
```

3. Add Groq API key
```
export GROQ_API_KEY=your_api_key_here
```
Or add to Streamlit secrets (.streamlit/secrets.toml):
```
GROQ_API_KEY = "your_api_key_here"
```

4. Run the app
```
streamlit run app.py
```

## Features

### SOS Emergency
- One-tap emergency activation
- Reason selection (stalking, theft, unsafe, urgent)
- Gender-specific officer dispatch 
- Real-time safety instructions while waiting
- Local emergency numbers display

### Scam Price Checker
- Enter any amount to validate
- Compares against local transport rates
- Detects auto/taxi pricing
- Shows overcharge percentage
- Country-specific thresholds

### Essential Phrases
- 15 critical phrases per country
- Native script display
- Text-to-speech pronunciation
- Emergency, bargaining, and basic communication phrases

### Cultural Guide
- Local dress codes
- Gesture meanings
- Etiquette tips
- Clear do's and don'ts

### Live Safety Map
- Interactive Leaflet map
- Police station locations
- Safe zone markers
- User location tracking

## Data Sources

- Transport scam data: Curated from travel forums and safety reports
- Emergency numbers: Official government sources
- Cultural guidelines: Travel advisory compilations
- Price thresholds: Local transport rate surveys

## Future Scope

- Real-time police station API integration
- Offline mode for areas without internet
- Community reporting for scam alerts
- Multi-language UI support
- Wearable device integration for SOS




