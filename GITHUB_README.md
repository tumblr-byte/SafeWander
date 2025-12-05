<div align="center">

# 🛡️ SafeWonder

### AI-Powered Travel Safety Assistant

*Your intelligent companion for safe travel worldwide*

[![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=for-the-badge&logo=Streamlit&logoColor=white)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Groq](https://img.shields.io/badge/Groq-000000?style=for-the-badge&logo=ai&logoColor=white)](https://groq.com)

[🚀 Quick Start](#-quick-start) • [✨ Features](#-features) • [📖 Documentation](#-documentation) • [🎯 Demo](#-demo)

</div>

---

## 🌟 What is SafeWonder?

SafeWonder is a **stunning, AI-powered travel safety application** that helps travelers navigate unfamiliar environments safely. It combines structured safety knowledge with AI intelligence to provide:

- 🚨 **Real-time situation analysis** with risk scoring
- 🗣️ **Culturally-appropriate translation** with pronunciation
- 📸 **OCR-based image translation** with scam detection
- 🆘 **One-click emergency access** to local services

<div align="center">

### 🎬 See It In Action

*[Demo GIF or Screenshot Here]*

</div>

---

## ✨ Features

<table>
<tr>
<td width="50%">

### 🚨 Situation Analyzer
Describe any situation and get instant AI-powered analysis:
- **Risk Score** (0-100) with color indicators
- **Pattern Matching** against known scams
- **Actionable Steps** - what to do & avoid
- **Emergency Contacts** - instant access

**Example:**
```
"Taxi asking 500 rupees for 2km in Delhi"
→ Risk: 65 (Medium-High)
→ Scam: Taxi Overcharge
→ Action: Use Uber/Ola, insist on meter
→ Emergency: Police 100
```

</td>
<td width="50%">

### 🗣️ Polite Culture Translator
Translate with cultural awareness:
- **Culturally-Appropriate** phrasing
- **Pronunciation Guide** (phonetic)
- **Tone & Etiquette** tips
- **Voice Output** (text-to-speech)

**Example:**
```
"Where is the bathroom?"
→ "Shauchalay kahan hai?"
→ Pronunciation: "SHOW-cha-lay ka-HAN hai"
→ Tip: Polite to ask shopkeeper
```

</td>
</tr>
<tr>
<td width="50%">

### 📸 OCR Translator
Photograph and translate instantly:
- **Text Extraction** from images
- **Auto Language Detection**
- **Instant Translation**
- **Scam Detection** in pricing

**Example:**
```
Photo of menu
→ Extract text
→ Translate to English
→ Warn if prices seem high
```

</td>
<td width="50%">

### 🆘 Emergency Access
One-click help when you need it:
- **Emergency Numbers** (police, ambulance)
- **Hospital Locations** with contacts
- **Police Stations** nearby
- **Embassy Information**

**Always accessible** with persistent button

</td>
</tr>
</table>

---

## 🚀 Quick Start

### Option 1: Streamlit Cloud (Recommended - 2 minutes!)

1. **Fork this repository**
2. **Deploy on Streamlit Cloud**: https://share.streamlit.io
3. **Add your Groq API key** in Secrets:
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
4. **Done!** Your app is live 🎉

Get a free Groq API key: https://console.groq.com

### Option 2: Run Locally (5 minutes)

```bash
# Clone the repository
git clone https://github.com/yourusername/safewonder.git
cd safewonder

# Install dependencies
pip install -r requirements.txt

# Install Tesseract OCR
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# Mac: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr

# Add your API key
echo "GROQ_API_KEY=your_key_here" > .env

# Run the app
streamlit run app.py
```

**Or use the quick run scripts:**
- Windows: `run.bat`
- Mac/Linux: `./run.sh`

---

## 🎯 Demo

### Try These Scenarios

**Situation Analysis:**
```
"Someone following me for 3 blocks in Tokyo"
```

**Translation:**
```
"Can you help me find the train station?"
```

**OCR:**
Upload a photo of any foreign language text (menu, sign, bill)

---

## 🛠️ Technology Stack

<div align="center">

| Category | Technology |
|----------|-----------|
| **Frontend** | Streamlit with custom CSS (glassmorphism, animations) |
| **AI** | Groq API (lightning-fast inference) |
| **OCR** | Tesseract (multi-language text extraction) |
| **TTS** | gTTS (text-to-speech) |
| **Data** | JSON-based knowledge base |
| **Deployment** | Streamlit Cloud (free!) |

</div>

---

## 📖 Documentation

<div align="center">

| Document | Description |
|----------|-------------|
| **[QUICKSTART.md](QUICKSTART.md)** | Get running in 5 minutes ⭐ |
| **[README.md](README.md)** | Complete documentation |
| **[STREAMLIT_CLOUD_DEPLOYMENT.md](STREAMLIT_CLOUD_DEPLOYMENT.md)** | Deployment guide |
| **[APP_STRUCTURE.md](APP_STRUCTURE.md)** | Technical architecture |
| **[PROJECT_SUMMARY.md](PROJECT_SUMMARY.md)** | High-level overview |
| **[DOCUMENTATION_INDEX.md](DOCUMENTATION_INDEX.md)** | Find any documentation |

</div>

---

## 🌍 Supported Countries

Currently includes detailed safety data for:
- 🇮🇳 **India** (Delhi, Mumbai)
- 🇯🇵 **Japan**
- 🇺🇸 **United States**

**Easily expandable** - Just edit `database.json`!

---

## 🎨 Design Highlights

<table>
<tr>
<td width="33%">

### 🎭 Glassmorphism
Semi-transparent cards with blur effects for a modern, professional look

</td>
<td width="33%">

### 🎨 Color-Coded
Risk indicators: Green (safe), Yellow (caution), Red (danger)

</td>
<td width="33%">

### ✨ Animations
Smooth transitions, pulse effects, and loading states

</td>
</tr>
</table>

---

## 📊 Project Stats

<div align="center">

![Lines of Code](https://img.shields.io/badge/Lines%20of%20Code-3000%2B-blue?style=flat-square)
![Files](https://img.shields.io/badge/Files-25%2B-green?style=flat-square)
![Components](https://img.shields.io/badge/Components-7-orange?style=flat-square)
![Countries](https://img.shields.io/badge/Countries-3-red?style=flat-square)

</div>

---

## 🤝 Contributing

Contributions welcome! Here's how:

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly**
5. **Commit**: `git commit -m 'Add amazing feature'`
6. **Push**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**

### Adding New Countries

Edit `database.json` and add a new country entry:
```json
{
  "id": "FRA",
  "name": "France",
  "emergency_numbers": {...},
  "common_scams": [...],
  "culture": {...}
}
```

---

## 🐛 Troubleshooting

<details>
<summary><b>GROQ_API_KEY not found</b></summary>

Add your API key to `.streamlit/secrets.toml` or `.env`:
```toml
GROQ_API_KEY = "your_key_here"
```
</details>

<details>
<summary><b>Tesseract not found</b></summary>

Install Tesseract OCR:
- **Windows**: Download from https://github.com/UB-Mannheim/tesseract/wiki
- **Mac**: `brew install tesseract`
- **Linux**: `sudo apt-get install tesseract-ocr`
</details>

<details>
<summary><b>OCR not working</b></summary>

- Ensure image is clear and well-lit
- Check Tesseract is installed correctly
- Try different image format (PNG, JPG)
</details>

See [QUICKSTART.md](QUICKSTART.md) for more troubleshooting tips.

---

## 📄 License

MIT License - Free to use and modify

---

## 🙏 Acknowledgments

- **Groq** for lightning-fast AI inference
- **Streamlit** for the amazing web framework
- **Tesseract OCR** for text extraction
- **xAI** for Grok language model
- All travelers who inspired this project

---

## 📞 Support

- 📖 **Documentation**: See all `.md` files
- 🐛 **Issues**: Open an issue on GitHub
- 💬 **Discussions**: Use GitHub Discussions
- 📧 **Contact**: [Your contact info]

---

<div align="center">

## 🌟 Star This Project!

If SafeWonder helps you travel safely, please give it a star ⭐

**Built with ❤️ for travelers worldwide**

[🚀 Deploy Now](https://share.streamlit.io) • [📖 Read Docs](README.md) • [🎯 Try Demo](#)

---

### 🛡️ SafeWonder: Travel Safely, Travel Smart

*Your breath-taking travel safety companion*

</div>
