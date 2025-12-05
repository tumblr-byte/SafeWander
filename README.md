# SafeWander - AI-Powered Travel Safety Companion

## 🌍 Overview

SafeWander is an AI-powered travel safety application that helps travelers stay safe, informed, and connected while exploring new countries. Using Grok AI, real-time translation, and community-driven insights, SafeWander provides practical safety guidance, scam prevention, and emergency support.

## 🎯 Problem Statement

Travelers face numerous safety challenges:
- **Scams & Fraud**: Overcharging, fake tours, gem shop scams
- **Language Barriers**: Miscommunication with locals, drivers, authorities
- **Cultural Misunderstandings**: Unintentional disrespect leading to conflict
- **Harassment & Stalking**: Especially for solo female travelers
- **Emergency Access**: Difficulty reaching help in unfamiliar places
- **Information Gaps**: No reliable local knowledge about safe areas

## ✨ Solution

SafeWander combines:
1. **AI Intelligence** (Grok) - Contextual safety analysis
2. **Real-time Translation** - Voice and text translation
3. **Community Wisdom** - Local and traveler insights
4. **Emergency Integration** - Quick access to help
5. **Cultural Awareness** - Respectful communication

## 🚀 Key Features

### 1. Trip Planner
- Pre-travel destination research
- Currency exchange information
- Hotel price verification
- Transport cost estimation
- Cultural awareness guide
- Roaming & phone setup tips

### 2. Real-time Safety
- Live safety scoring (1-10)
- Area-specific scam warnings
- Emergency contact database
- Community incident reports
- Situational safety advice
- Time-based safety assessment

### 3. Voice Translator
- Real-time voice translation
- Survival phrases in local language
- Heart-to-heart communication phrases
- Driver communication templates
- Offline translation support

### 4. Emergency Response
- One-click SOS alerts
- Emergency contact sharing
- Incident complaint filing
- Evidence upload (photos/video)
- Location sharing with trusted contacts
- Police/NGO integration

### 5. Community Hub
- Scam warnings from travelers
- Safe spot recommendations
- Incident reports with solutions
- Situational tips from locals
- Upvote/verification system
- Comment and discussion

## 🛠️ Tech Stack

### Frontend
- **Streamlit** - Web UI framework
- **Pillow** - Image processing

### Backend & AI
- **Grok API** - Main AI brain for safety analysis
- **Google Cloud Speech-to-Text** - Voice input
- **Google Cloud Translation** - Multi-language support
- **Tesseract OCR** - Text extraction from images
- **LibreTranslate** - Free translation alternative

### Database
- **SQLite/JSON** - Local data storage
- Community reports
- Location database
- User complaints

### Libraries
- `speech_recognition` - Voice capture
- `translate` - Translation
- `pytesseract` - OCR
- `requests` - API calls
- `python-dotenv` - Environment management

## 📋 Installation

See [SETUP.md](SETUP.md) for detailed installation instructions.

Quick start:
```bash
pip install -r requirements.txt
streamlit run app.py
```

## 🎮 Usage

### Before Travel
1. Open Trip Planner tab
2. Enter current location and destination
3. Get currency, hotel, and transport info
4. Review cultural awareness tips
5. Note emergency contacts

### During Travel
1. Use Real-time Safety tab to check current area
2. Use Voice Translator for communication
3. Check Community reports for local insights
4. Use Emergency tab if needed

### After Travel
1. Share your experience in Community tab
2. Report any incidents
3. Help other travelers with tips

## 📊 Database Structure

### Locations
```json
{
  "Bangkok": {
    "safety_score": 8.5,
    "common_scams": [...],
    "emergency_contacts": {...},
    "survival_words": {...},
    "cultural_awareness": {...}
  }
}
```

### Community Reports
```json
{
  "type": "scam|safe_spot|tip|incident",
  "location": "Bangkok",
  "description": "...",
  "verified": true,
  "upvotes": 45
}
```

## 🤖 AI Integration

### Grok Prompts

**Trip Planning**
```
Generate practical travel info for [destination]:
- Currency exchange
- Hotel recommendations
- Transport options
- Safety overview
```

**Safety Analysis**
```
Person in [location] at [time] experiencing [situation].
Provide 5 immediate safety actions.
```

**Emergency Response**
```
User in [location] feeling unsafe: [description]
Generate:
1. Immediate actions
2. Emergency contacts
3. Cultural awareness
4. Survival phrases
```

## 👥 Community Features

### Report Types
- **Scam Warnings**: Detailed scam descriptions
- **Safe Spots**: Recommended areas and venues
- **Incident Reports**: What happened and how to handle
- **Situational Tips**: Practical advice for specific situations

### Trust System
- Verified locals (phone verification)
- Verified travelers (email verification)
- Upvote system for credibility
- Moderation for offensive content

## 🚨 Emergency Features

### SOS Alert
- One-click emergency activation
- Location sharing
- Trusted contact notification
- Emergency number display

### Complaint System
- Incident documentation
- Evidence upload
- Authority notification
- Reference tracking

## 🌐 Supported Languages

Currently includes survival phrases for:
- Thai
- Spanish
- French
- German
- Japanese
- Mandarin
- Hindi
- Portuguese

Easily expandable via database.

## 📈 Scalability

### Add New Locations
1. Edit `database.json`
2. Add location data with safety info
3. Community will add reports

### Add New Languages
1. Update `survival_words` in database
2. Add translation models
3. Update UI language selector

### Integrate New APIs
1. Add API integration function
2. Update prompts
3. Test and deploy

## 🔒 Security & Privacy

- No personal data stored without consent
- Encrypted location sharing
- Anonymous community reports option
- GDPR compliant
- No tracking or analytics

## 🎓 Use Cases

### Solo Travelers
- Safety verification before visiting areas
- Emergency contact access
- Scam prevention

### Female Travelers
- Women-specific safety tips
- Women helpline numbers
- Safe route recommendations
- Harassment response protocols

### Business Travelers
- Quick destination briefing
- Transport safety
- Emergency contacts
- Cultural tips

### Group Travelers
- Shared safety information
- Group emergency alerts
- Collective community insights

## 🏆 Hackathon Alignment

### VisaVerse AI Hackathon Criteria

✅ **Innovation & Creativity**
- Unique combination of AI, translation, and community
- Novel approach to traveler safety

✅ **AI Integration**
- Grok AI for contextual analysis
- Meaningful, purposeful use of AI

✅ **Technical Execution**
- Clean architecture
- Multiple API integrations
- Robust error handling

✅ **Impact & Relevance**
- Solves real traveler problems
- Addresses global mobility challenges
- Helps people travel safely across borders

✅ **User Experience**
- Intuitive Streamlit interface
- Clear information hierarchy
- Easy emergency access

✅ **Presentation**
- Well-documented code
- Clear README and setup guide
- Demo video ready

## 📝 Demo Video Script

1. **Intro** (0-15s)
   - "SafeWander helps travelers stay safe globally"
   - Show app opening

2. **Trip Planning** (15-30s)
   - Search destination
   - Show currency, hotel, transport info
   - Show cultural tips

3. **Real-time Safety** (30-45s)
   - Check current area
   - Show safety score
   - Show community reports

4. **Emergency** (45-60s)
   - Show SOS button
   - Show emergency contacts
   - Show complaint system

5. **Community** (60-75s)
   - Show community reports
   - Show upvote system
   - Show how to share

6. **Outro** (75-90s)
   - "Travel safely, travel smart"
   - Show impact

## 🚀 Future Enhancements

- [ ] Mobile app (React Native)
- [ ] Offline mode
- [ ] Real-time incident mapping
- [ ] AI-powered route planning
- [ ] Integration with local authorities
- [ ] Blockchain for report verification
- [ ] AR for navigation
- [ ] Wearable device integration

## 📞 Support

For issues or questions:
1. Check SETUP.md
2. Review database.json
3. Test API connections
4. Check Streamlit logs

## 📄 License

MIT License - Free to use and modify

## 👨‍💻 Team

Built for VisaVerse AI Hackathon 2025

## 🙏 Acknowledgments

- Grok AI (xAI) for powerful language model
- Google Cloud for translation and speech APIs
- Streamlit for amazing web framework
- Community contributors for safety insights

---

**SafeWander: Travel Safely, Travel Smart 🌍**

*Empowering travelers with AI-driven safety, real-time translation, and community wisdom.*
