# SafeWonder - AI-Powered Travel Safety Assistant 🛡️

## 🌍 Overview

SafeWonder is a stunning, AI-powered travel safety application that helps travelers navigate unfamiliar environments safely. Using Groq AI, real-time situation analysis, cultural translation, and OCR capabilities, SafeWonder provides instant risk assessment, safety recommendations, and multilingual support to keep travelers safe worldwide.

## 🎯 Problem Statement

Travelers face numerous safety challenges:
- **Scams & Fraud**: Taxi overcharging, fake tour guides, hidden charges
- **Language Barriers**: Miscommunication with locals, drivers, authorities
- **Cultural Misunderstandings**: Unintentional disrespect leading to conflict
- **Harassment & Safety**: Being followed, unwanted touching, unsafe situations
- **Emergency Access**: Difficulty reaching help in unfamiliar places
- **Information Gaps**: No reliable local knowledge about scams and safety

## ✨ Solution

SafeWonder combines:
1. **AI Intelligence** (Groq) - Contextual safety analysis with risk scoring
2. **Knowledge Base** - Structured country-specific safety data (database.json)
3. **Real-time Translation** - Culturally-appropriate phrase translation
4. **OCR Technology** - Instant translation of signs, menus, and documents
5. **Emergency Integration** - One-click access to local emergency services

## 🚀 Key Features

### 1. 🚨 Situation Analyzer
- **Text or Voice Input**: Describe any situation you're experiencing
- **AI-Powered Analysis**: Groq AI matches your situation against known scams and harassment patterns
- **Risk Scoring**: Get a clear risk score (0-100) with color-coded indicators
- **Actionable Advice**: Receive specific "what to do" and "what NOT to do" instructions
- **Emergency Contacts**: Instant access to relevant emergency numbers
- **Cultural Context**: Understand if behavior is normal or concerning in local culture

### 2. 🗣️ Polite Culture Translator
- **Culturally-Appropriate Translation**: Not just translation, but culturally polite phrasing
- **Pronunciation Guidance**: Learn how to say phrases correctly
- **Tone & Etiquette Tips**: Understand the proper way to communicate
- **Common Phrases**: Quick access to essential local phrases
- **Voice Output**: Text-to-speech for proper pronunciation
- **Bidirectional Translation**: Translate both ways seamlessly

### 3. 📸 OCR Translator
- **Image Upload**: Photograph signs, menus, bills, or documents
- **Text Extraction**: Tesseract OCR extracts text from images
- **Automatic Language Detection**: Identifies the language automatically
- **Instant Translation**: Translates to your native language
- **Scam Detection**: AI analyzes text for suspicious content or overcharging
- **Safety Warnings**: Get alerts if something looks wrong

### 4. 🆘 Emergency Access
- **Persistent Emergency Button**: Always visible on every screen
- **One-Click Calling**: Direct links to emergency services
- **Location-Specific Contacts**: Police, ambulance, women's helpline, fire
- **Hospital & Police Locations**: Nearest facilities with contact info
- **Embassy Information**: Your country's embassy contacts

### 5. ⚙️ User Profile & Onboarding
- **Personalized Experience**: Tailored safety advice based on your profile
- **Destination-Specific Data**: Loads relevant country information
- **Gender-Aware Guidance**: Appropriate harassment prevention advice
- **Safety Preferences**: Control the intensity of warnings

## 🛠️ Tech Stack

### Frontend
- **Streamlit** - Modern web UI framework with custom CSS
- **Custom Styling** - Glassmorphism effects, animations, responsive design

### AI & Intelligence
- **Groq API** - Lightning-fast AI for situation analysis and translation
- **Intelligent Prompting** - Context-aware prompts with knowledge base integration

### OCR & Language
- **Tesseract OCR** - Text extraction from images
- **pytesseract** - Python wrapper for Tesseract
- **langdetect** - Automatic language detection
- **gTTS** - Text-to-speech for pronunciation

### Data & Storage
- **JSON Database** - Structured country-specific safety data (database.json)
- **Session State** - Streamlit session management for user data

### Libraries
- `streamlit>=1.28.0` - Web framework
- `groq>=0.4.0` - Groq API client
- `pytesseract>=0.3.10` - OCR
- `Pillow>=10.0.0` - Image processing
- `python-dotenv>=1.0.0` - Environment management
- `gTTS>=2.4.0` - Text-to-speech
- `langdetect>=1.0.9` - Language detection
- `streamlit-audio-recorder>=0.0.8` - Voice input

## 📋 Installation & Setup

### Prerequisites
- Python 3.8 or higher
- Tesseract OCR installed on your system
- Groq API key (get one at https://console.groq.com)

### Local Development

1. **Clone the repository**
```bash
git clone <your-repo-url>
cd safewonder
```

2. **Install Python dependencies**
```bash
pip install -r requirements.txt
```

3. **Install Tesseract OCR**

**Windows:**
```bash
# Download installer from: https://github.com/UB-Mannheim/tesseract/wiki
# Add to PATH: C:\Program Files\Tesseract-OCR
```

**macOS:**
```bash
brew install tesseract
```

**Linux:**
```bash
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-eng tesseract-ocr-jpn tesseract-ocr-hin
```

4. **Set up environment variables**

Create a `.env` file:
```bash
GROQ_API_KEY=your_groq_api_key_here
DATABASE_PATH=database.json
APP_ENV=development
DEBUG=True
```

5. **Run the application**
```bash
streamlit run app.py
```

### Streamlit Cloud Deployment

1. **Push your code to GitHub**

2. **Go to Streamlit Cloud** (https://share.streamlit.io)

3. **Deploy your app**
   - Connect your GitHub repository
   - Select `app.py` as the main file
   - Add your secrets in the Streamlit Cloud dashboard

4. **Add Secrets in Streamlit Cloud**

Go to your app settings → Secrets and add:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

5. **Add system dependencies**

The `packages.txt` file should contain:
```
tesseract-ocr
tesseract-ocr-eng
tesseract-ocr-jpn
tesseract-ocr-hin
ffmpeg
```

6. **Deploy!** Your app will be live at `https://your-app-name.streamlit.app`

## 🎮 Usage

### First Time Setup
1. **Launch the app** - Open SafeWonder in your browser
2. **Complete Onboarding** - Fill in your profile:
   - Name
   - Native language
   - Destination country and city
   - Arrival date
   - Gender (for appropriate safety guidance)
   - Safety preference level
3. **Start Exploring** - Access all features from the sidebar

### Using Situation Analyzer
1. Navigate to **🚨 Situation Analyzer**
2. Describe your situation in text or use voice input
   - Example: "Taxi driver refusing to use meter in Delhi"
   - Example: "Someone following me for 3 blocks"
3. Click **Analyze Situation**
4. Review the risk score and recommendations
5. Access emergency contacts if needed

### Using Polite Translator
1. Navigate to **🗣️ Polite Translator**
2. Type or speak your phrase
3. Select target language (auto-detected from your destination)
4. Click **Translate**
5. Read pronunciation guide and cultural tips
6. Play audio to hear correct pronunciation

### Using OCR Translator
1. Navigate to **📸 OCR Translator**
2. Upload an image (sign, menu, bill, document)
3. Click **Extract & Translate**
4. Review extracted text and translation
5. Check for any scam warnings

### Emergency Access
1. Click the **🆘 Emergency** button (always visible)
2. View emergency numbers for your destination
3. One-click calling to emergency services
4. Access hospital and police station locations
5. View embassy contact information

## 📊 Database Structure

The `database.json` file contains country-specific safety information:

```json
{
  "countries": [
    {
      "id": "IND",
      "name": "India",
      "emergency_numbers": {
        "police": "100",
        "ambulance": "102",
        "women_helpline": "1091",
        "fire": "101"
      },
      "transport": {
        "available": ["Uber", "Ola", "Metro"],
        "avg_taxi_fare_per_km": 18
      },
      "common_scams": [
        {
          "name": "Taxi Overcharge Scam",
          "situation_keywords": ["taxi", "overcharge", "extra money"],
          "how_it_happens": "Driver refuses to start meter...",
          "how_to_avoid": ["Always insist on meter", "Use Uber/Ola"],
          "what_to_do": ["Politely refuse", "Take screenshot"]
        }
      ],
      "harassment_patterns": {
        "examples": [
          {
            "name": "Being Followed",
            "description": "Someone walks behind you...",
            "recommended_actions": ["Move to crowded area", "Call emergency"]
          }
        ]
      },
      "culture": {
        "greetings": "Namaste with slight bow",
        "dos": ["Remove shoes in temples"],
        "donts": ["Avoid kissing in public"]
      },
      "local_phrases": {
        "help": "Madad kijiye!",
        "stop": "Ruko!"
      },
      "important_locations": {
        "hospitals": [...],
        "police_stations": [...],
        "embassy": {...}
      }
    }
  ]
}
```

### Adding New Countries

To add a new country, simply add a new entry to the `countries` array in `database.json` following the structure above.

## 🤖 AI Integration

SafeWonder uses Groq API with intelligent prompting that combines user input with structured knowledge base data.

### How It Works

1. **User Input** → User describes situation or phrase
2. **Context Building** → App loads relevant data from database.json
3. **Prompt Construction** → Combines user input + knowledge base + user profile
4. **Groq Analysis** → AI analyzes with full context
5. **Structured Output** → Returns risk score, recommendations, and cultural notes

### Example: Situation Analysis Prompt

```
You are a Safety AI assistant for travelers. Analyze the following situation:

USER SITUATION: "Taxi driver asking for 500 rupees for 2km ride in Delhi"

TRAVELER PROFILE:
- Gender: Female
- Native Language: English
- Destination: Delhi, India

KNOWLEDGE BASE CONTEXT:
- Common Scam: Taxi Overcharge Scam
- Keywords: taxi, overcharge, extra money, no meter
- Average fare: 18 rupees/km
- What to do: Insist on meter, use Uber/Ola
- Emergency: Police 100

TASK:
1. Match keywords to identify scam patterns
2. Assess risk level (0-100)
3. Provide specific actions from knowledge base
4. Add intelligent reasoning beyond the JSON data
5. Include emergency contacts and cultural guidance

OUTPUT FORMAT: JSON with risk_score, pattern_matched, what_to_do, etc.
```

This approach ensures AI responses are grounded in real safety data while adding intelligent analysis.

## 🎨 Visual Design

SafeWonder features a stunning, modern interface designed to reduce stress in emergency situations:

### Design Highlights
- **Glassmorphism Effects**: Semi-transparent cards with blur effects
- **Color-Coded Risk Indicators**: Green (safe), Yellow (caution), Red (danger)
- **Smooth Animations**: Page transitions, button interactions, loading states
- **Responsive Layout**: Works beautifully on mobile and desktop
- **Dark Theme**: Easy on the eyes, professional appearance
- **Persistent Emergency Button**: Always accessible with pulsing animation

### Color Palette
- **Primary**: #6366F1 (Indigo) - Trust and safety
- **Secondary**: #EC4899 (Pink) - Energy and attention
- **Success**: #10B981 (Green) - Safe and good
- **Warning**: #F59E0B (Amber) - Caution
- **Danger**: #EF4444 (Red) - Emergency
- **Background**: #0F172A (Dark blue) - Modern and calm

## 🌐 Supported Countries

Currently includes detailed data for:
- 🇮🇳 India (Delhi, Mumbai)
- 🇯🇵 Japan
- 🇺🇸 United States

### Easily Expandable
Add new countries by editing `database.json` with:
- Emergency numbers
- Common scams
- Harassment patterns
- Cultural dos and don'ts
- Local phrases
- Important locations

## 🔒 Security & Privacy

- **API Key Protection**: Loaded from environment variables, never exposed
- **Session-Based Storage**: User data stored only in session, not persisted
- **No Tracking**: No analytics or user tracking
- **Secure Communication**: HTTPS for all API calls
- **Input Sanitization**: All user inputs validated and sanitized

## 📁 Project Structure

```
safewonder/
├── app.py                          # Main application entry point
├── database.json                   # Country-specific safety data
├── requirements.txt                # Python dependencies
├── packages.txt                    # System dependencies for Streamlit Cloud
├── .env.example                    # Environment variable template
├── README.md                       # This file
├── .streamlit/
│   ├── config.toml                # Streamlit configuration
│   └── secrets.toml               # API keys (not in git)
├── components/
│   ├── __init__.py
│   ├── profile_manager.py         # User onboarding and profile
│   ├── situation_analyzer.py      # Core situation analysis logic
│   ├── situation_analyzer_ui.py   # Situation analyzer UI
│   ├── culture_translator.py      # Translation logic
│   ├── culture_translator_ui.py   # Translator UI
│   ├── ocr_translator.py          # OCR processing logic
│   └── ocr_translator_ui.py       # OCR UI
├── utils/
│   ├── __init__.py
│   ├── database_loader.py         # JSON database loader
│   ├── groq_client.py             # Groq API wrapper
│   └── session_manager.py         # Session state management
└── assets/
    └── logo.png                    # App logo (optional)
```

## 🎓 Use Cases

### Solo Travelers
- Instant situation analysis when feeling unsafe
- Emergency contact access in unfamiliar places
- Scam prevention with AI-powered detection

### Female Travelers
- Gender-specific safety guidance
- Women's helpline numbers
- Harassment pattern recognition
- Immediate action recommendations

### Business Travelers
- Quick cultural briefing
- Professional communication phrases
- Transport safety verification
- Emergency contacts for business districts

### First-Time International Travelers
- Cultural dos and don'ts
- Polite phrase translation
- Menu and sign translation
- Confidence in unfamiliar environments

## 🚀 Demo Scenarios

### Scenario 1: Taxi Scam Detection
1. User: "Taxi driver in Delhi asking 500 rupees for 2km"
2. App analyzes → Matches "Taxi Overcharge Scam"
3. Risk Score: 65 (Medium-High)
4. Shows: Average fare (36 rupees), what to do, emergency number

### Scenario 2: Cultural Translation
1. User wants to say: "Where is the bathroom?"
2. App translates to Hindi: "Shauchalay kahan hai?"
3. Shows pronunciation: "SHOW-cha-lay ka-HAN hai"
4. Cultural tip: "Polite to ask shopkeeper, not strangers"

### Scenario 3: Menu Translation
1. User photographs Japanese menu
2. OCR extracts text
3. Translates to English
4. Warns: "Price seems high for this dish - verify before ordering"

## 🚀 Future Enhancements

- [ ] Mobile app (React Native/Flutter)
- [ ] Offline mode with cached data
- [ ] Real-time location tracking with geofencing
- [ ] Community-sourced scam reports
- [ ] Integration with local emergency services APIs
- [ ] Multi-language UI support
- [ ] Voice-to-voice real-time translation
- [ ] Wearable device integration for SOS
- [ ] AI-powered image analysis for safety assessment
- [ ] Blockchain for incident verification

## 🐛 Troubleshooting

### Tesseract Not Found
```bash
# Windows: Add to PATH
C:\Program Files\Tesseract-OCR

# Or set in .env
TESSERACT_PATH=C:\Program Files\Tesseract-OCR\tesseract.exe
```

### Groq API Errors
- Check your API key is valid
- Verify you have API credits
- Check rate limits (60 requests/minute on free tier)

### OCR Not Working
- Ensure image is clear and well-lit
- Try preprocessing image (increase contrast)
- Check Tesseract language packs are installed

### Streamlit Cloud Deployment Issues
- Verify `packages.txt` includes all system dependencies
- Check secrets are properly configured
- Review deployment logs for errors

## 📄 License

MIT License - Free to use and modify

## 👨‍💻 Contributing

Contributions welcome! To add a new country:
1. Fork the repository
2. Add country data to `database.json`
3. Test with the app
4. Submit a pull request

## 🙏 Acknowledgments

- **Groq** for lightning-fast AI inference
- **Streamlit** for the amazing web framework
- **Tesseract OCR** for text extraction
- **xAI** for Grok language model
- All travelers who inspired this project

## 📞 Support

For issues or questions:
- Open an issue on GitHub
- Check the troubleshooting section
- Review deployment documentation

---

**SafeWonder: Travel Safely, Travel Smart 🛡️**

*Empowering travelers with AI-driven safety analysis, cultural translation, and instant emergency access.*

**Built with ❤️ for travelers worldwide**
