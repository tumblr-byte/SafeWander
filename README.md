# SafeWander

AI-powered travel safety companion for tourists and solo travelers.

## What it does

SafeWander helps travelers stay safe in unfamiliar destinations by providing:

- SOS Emergency System - One-tap emergency alert with officer dispatch and safety instructions
- Scam Price Checker - Real-time price validation to detect tourist scams
- Essential Phrases - 15 life-saving phrases with text-to-speech pronunciation
- Cultural Guide - Local customs, do's and don'ts for respectful travel
- Live Safety Map - Nearby police stations and safe zones
- AI Safety Assistant - Personalized safety advice based on your profile

## Supported Countries

India, Thailand, Mexico, USA, Brazil

## Tech Stack

- Streamlit
- Groq AI (Llama 3.3)
- Leaflet Maps
- Web Speech API

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

3. Add your Groq API key to Streamlit secrets or environment variable
```
GROQ_API_KEY=your_api_key_here
```

4. Run the app
```
streamlit run app.py
```

## Features

### SOS Emergency
Quick emergency activation with reason selection. Dispatches appropriate officer based on user gender and location. Provides real-time safety instructions while waiting for help.

### Scam Checker
Enter any price to check if you're being overcharged. Compares against local rates and flags suspicious pricing. Works for auto-rickshaws, taxis, and other transport.

### Essential Phrases
15 critical phrases for each destination country. Click to hear pronunciation using text-to-speech. Includes emergency phrases, bargaining, and basic communication.

### Cultural Guide
Local dress codes, gestures, and etiquette. Clear do's and don'ts to avoid cultural misunderstandings.

## License

MIT License

