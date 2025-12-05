# 🏗️ SafeWonder App Structure

## 📁 File Organization

```
safewonder/
│
├── 🎯 MAIN APPLICATION
│   └── app.py                          # Entry point, navigation, main UI
│
├── 📊 DATA
│   └── database.json                   # Country safety data, scams, culture
│
├── 🧩 COMPONENTS (UI + Logic)
│   ├── profile_manager.py              # Onboarding & profile management
│   ├── situation_analyzer.py           # Core analysis logic
│   ├── situation_analyzer_ui.py        # Situation analyzer interface
│   ├── culture_translator.py           # Translation logic
│   ├── culture_translator_ui.py        # Translator interface
│   ├── ocr_translator.py               # OCR processing logic
│   └── ocr_translator_ui.py            # OCR interface
│
├── 🛠️ UTILITIES
│   ├── database_loader.py              # Load & parse JSON data
│   ├── groq_client.py                  # Groq API wrapper
│   └── session_manager.py              # Session state management
│
├── ⚙️ CONFIGURATION
│   ├── .streamlit/
│   │   ├── config.toml                 # Theme & app settings
│   │   └── secrets.toml                # API keys (not in git!)
│   ├── .env.example                    # Environment template
│   └── .gitignore                      # Exclude secrets & cache
│
├── 📦 DEPENDENCIES
│   ├── requirements.txt                # Python packages
│   └── packages.txt                    # System dependencies (Tesseract)
│
├── 📚 DOCUMENTATION
│   ├── README.md                       # Main documentation
│   ├── QUICKSTART.md                   # Quick start guide
│   ├── STREAMLIT_CLOUD_DEPLOYMENT.md   # Deployment guide
│   ├── FINAL_DEPLOYMENT_CHECKLIST.md   # Pre-launch checklist
│   └── APP_STRUCTURE.md                # This file
│
└── 🎨 ASSETS (optional)
    └── logo.png                        # App logo
```

---

## 🔄 Application Flow

```
┌─────────────────────────────────────────────────────────────┐
│                         USER OPENS APP                       │
└─────────────────────────────────────────────────────────────┘
                              ↓
┌─────────────────────────────────────────────────────────────┐
│                    app.py (Main Entry)                       │
│  • Load custom CSS                                           │
│  • Initialize session state                                  │
│  • Load Groq API key from secrets                           │
│  • Load database.json                                        │
└─────────────────────────────────────────────────────────────┘
                              ↓
                    ┌─────────────────┐
                    │ Profile exists? │
                    └─────────────────┘
                       ↓           ↓
                     NO           YES
                       ↓           ↓
        ┌──────────────────┐    ┌──────────────────┐
        │   ONBOARDING     │    │  MAIN APP        │
        │  (First Time)    │    │  (Navigation)    │
        └──────────────────┘    └──────────────────┘
                ↓                        ↓
    ┌───────────────────────┐   ┌──────────────────────────┐
    │ profile_manager.py    │   │ Show Navigation Sidebar  │
    │ • Collect user info   │   │ • Home                   │
    │ • Validate data       │   │ • Situation Analyzer     │
    │ • Load country data   │   │ • Polite Translator      │
    │ • Save to session     │   │ • OCR Translator         │
    └───────────────────────┘   │ • Profile Settings       │
                                │ • Emergency              │
                                └──────────────────────────┘
                                           ↓
                        ┌──────────────────────────────────┐
                        │     USER SELECTS FEATURE         │
                        └──────────────────────────────────┘
                                           ↓
        ┌──────────────────┬──────────────┴──────────────┬──────────────────┐
        ↓                  ↓                              ↓                  ↓
┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│  SITUATION    │  │   POLITE      │  │      OCR      │  │   EMERGENCY   │
│   ANALYZER    │  │  TRANSLATOR   │  │  TRANSLATOR   │  │   CONTACTS    │
└───────────────┘  └───────────────┘  └───────────────┘  └───────────────┘
        ↓                  ↓                  ↓                  ↓
┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ User inputs   │  │ User inputs   │  │ User uploads  │  │ Display       │
│ situation     │  │ phrase        │  │ image         │  │ emergency     │
│ (text/voice)  │  │               │  │               │  │ numbers       │
└───────────────┘  └───────────────┘  └───────────────┘  └───────────────┘
        ↓                  ↓                  ↓                  ↓
┌───────────────┐  ┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ Match against │  │ Build prompt  │  │ Extract text  │  │ Show          │
│ JSON patterns │  │ with cultural │  │ with          │  │ hospitals,    │
│               │  │ context       │  │ Tesseract     │  │ police,       │
└───────────────┘  └───────────────┘  └───────────────┘  │ embassy       │
        ↓                  ↓                  ↓           └───────────────┘
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ Send to       │  │ Send to       │  │ Detect        │
│ Groq API      │  │ Groq API      │  │ language      │
│ with context  │  │               │  │               │
└───────────────┘  └───────────────┘  └───────────────┘
        ↓                  ↓                  ↓
┌───────────────┐  ┌───────────────┐  ┌───────────────┐
│ Display:      │  │ Display:      │  │ Send to       │
│ • Risk score  │  │ • Translation │  │ Groq API      │
│ • Pattern     │  │ • Pronunciation│ │ for analysis  │
│ • Actions     │  │ • Cultural    │  │               │
│ • Emergency   │  │   tips        │  └───────────────┘
│   numbers     │  │ • Audio (TTS) │          ↓
└───────────────┘  └───────────────┘  ┌───────────────┐
                                      │ Display:      │
                                      │ • Translation │
                                      │ • Warnings    │
                                      │ • Explanation │
                                      └───────────────┘
```

---

## 🧩 Component Interactions

### Situation Analyzer Flow
```
situation_analyzer_ui.py (UI)
    ↓ (user input)
situation_analyzer.py (Logic)
    ↓ (match keywords)
database_loader.py (Get scam patterns)
    ↓ (build prompt)
groq_client.py (API call)
    ↓ (response)
situation_analyzer_ui.py (Display results)
```

### Polite Translator Flow
```
culture_translator_ui.py (UI)
    ↓ (user phrase)
culture_translator.py (Logic)
    ↓ (get cultural context)
database_loader.py (Get culture data)
    ↓ (build prompt)
groq_client.py (API call)
    ↓ (translation + tips)
culture_translator_ui.py (Display + TTS)
```

### OCR Translator Flow
```
ocr_translator_ui.py (UI)
    ↓ (image upload)
ocr_translator.py (Logic)
    ↓ (extract text)
Tesseract OCR
    ↓ (detect language)
langdetect library
    ↓ (translate + analyze)
groq_client.py (API call)
    ↓ (translation + warnings)
ocr_translator_ui.py (Display results)
```

---

## 🗄️ Data Flow

### Session State (Managed by session_manager.py)
```python
{
    'user_profile': {
        'name': str,
        'native_language': str,
        'traveling_to_country': str,
        'traveling_to_city': str,
        'arrival_date': str,
        'gender': str,
        'safety_preference': str
    },
    'country_data': {
        # Loaded from database.json
        'emergency_numbers': {...},
        'common_scams': [...],
        'harassment_patterns': {...},
        'culture': {...},
        'local_phrases': {...},
        'important_locations': {...}
    },
    'groq_api_key': str,
    'database': {...},
    'current_page': str
}
```

### Database Structure (database.json)
```json
{
  "countries": [
    {
      "id": "IND",
      "name": "India",
      "emergency_numbers": {...},
      "transport": {...},
      "common_scams": [
        {
          "name": "Scam Name",
          "situation_keywords": [...],
          "how_it_happens": "...",
          "how_to_avoid": [...],
          "what_to_do": [...]
        }
      ],
      "harassment_patterns": {...},
      "culture": {...},
      "local_phrases": {...},
      "laws": {...},
      "important_locations": {...}
    }
  ]
}
```

---

## 🎨 UI Components

### Custom CSS (in app.py)
- **Color Palette**: Primary, secondary, success, warning, danger
- **Glassmorphism**: Semi-transparent cards with blur
- **Animations**: Pulse, fade, scale, checkmark
- **Responsive**: Mobile and desktop layouts

### Streamlit Components Used
- `st.text_input()` - Text inputs
- `st.text_area()` - Multi-line text
- `st.button()` - Action buttons
- `st.selectbox()` - Dropdowns
- `st.date_input()` - Date picker
- `st.file_uploader()` - Image upload
- `st.columns()` - Layout columns
- `st.sidebar` - Navigation sidebar
- `st.markdown()` - Custom HTML/CSS
- `st.error()` / `st.success()` - Alerts

---

## 🔌 External Dependencies

### Python Packages (requirements.txt)
- **streamlit** - Web framework
- **groq** - AI API client
- **pytesseract** - OCR wrapper
- **Pillow** - Image processing
- **python-dotenv** - Environment variables
- **gTTS** - Text-to-speech
- **langdetect** - Language detection

### System Packages (packages.txt)
- **tesseract-ocr** - OCR engine
- **tesseract-ocr-eng** - English language pack
- **tesseract-ocr-jpn** - Japanese language pack
- **tesseract-ocr-hin** - Hindi language pack
- **ffmpeg** - Audio processing

---

## 🔐 Security Architecture

### API Key Management
```
.env (local) → python-dotenv → os.getenv()
                                    ↓
.streamlit/secrets.toml → st.secrets.get()
                                    ↓
                            app.py (runtime)
                                    ↓
                        groq_client.py (API calls)
```

### Data Privacy
- **No persistent storage** - All data in session only
- **No user tracking** - No analytics or cookies
- **API key protection** - Never exposed in code
- **Input sanitization** - All inputs validated

---

## 🚀 Deployment Architecture

### Local Development
```
Developer Machine
    ↓
Python + Streamlit
    ↓
localhost:8501
```

### Streamlit Cloud
```
GitHub Repository
    ↓
Streamlit Cloud (auto-deploy on push)
    ↓
Container with Python + Tesseract
    ↓
https://your-app.streamlit.app
```

---

## 📊 Performance Considerations

### Caching Strategy
- Database loaded once per session
- Groq API responses cached for identical queries
- TTS audio cached to avoid regeneration

### Optimization Points
- Image compression before OCR
- Lazy loading of country data
- Async API calls where possible
- Minimal re-renders with session state

---

## 🎯 Key Design Decisions

1. **Modular Architecture**: Separate UI and logic for maintainability
2. **Session-Based Storage**: No database needed, privacy-friendly
3. **JSON Knowledge Base**: Easy to update without code changes
4. **Groq API**: Fast inference, cost-effective
5. **Streamlit**: Rapid development, easy deployment
6. **Tesseract OCR**: Free, open-source, multi-language

---

**This structure enables rapid development, easy maintenance, and seamless deployment! 🛡️**
