# ⚡ SafeWonder Quick Start Guide

## 🎯 Get Running in 5 Minutes

### Option 1: Streamlit Cloud (Recommended - No Installation!)

1. **Fork this repository** on GitHub
2. **Go to** https://share.streamlit.io
3. **Click "New app"** and select your forked repo
4. **Add your Groq API key** in Secrets:
   ```toml
   GROQ_API_KEY = "your_key_here"
   ```
5. **Deploy!** Your app will be live in ~2 minutes

Get a free Groq API key: https://console.groq.com

---

### Option 2: Run Locally

#### Step 1: Install Dependencies

```bash
# Clone the repo
git clone <your-repo-url>
cd safewonder

# Install Python packages
pip install -r requirements.txt

# Install Tesseract OCR
# Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki
# Mac: brew install tesseract
# Linux: sudo apt-get install tesseract-ocr
```

#### Step 2: Configure API Key

Create a `.env` file:
```bash
GROQ_API_KEY=your_groq_api_key_here
```

Or add to `.streamlit/secrets.toml`:
```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

#### Step 3: Run the App

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

---

## 🎮 First Time Using the App

### 1. Complete Onboarding
When you first open the app, you'll see an onboarding screen. Fill in:
- **Name**: Your name
- **Native Language**: English, Spanish, etc.
- **Destination Country**: Where you're traveling
- **Destination City**: Specific city
- **Arrival Date**: When you arrive
- **Gender**: For appropriate safety guidance
- **Safety Preference**: How cautious you want warnings

### 2. Explore Features

**🚨 Situation Analyzer**
- Describe any situation: "Taxi asking extra money"
- Get instant risk assessment
- See what to do and emergency contacts

**🗣️ Polite Translator**
- Type a phrase: "Where is the bathroom?"
- Get culturally-appropriate translation
- Hear pronunciation

**📸 OCR Translator**
- Upload photo of sign/menu/bill
- Get instant translation
- Detect scams in pricing

**🆘 Emergency**
- One-click access to emergency numbers
- Hospital and police locations
- Embassy contacts

---

## 🔑 Getting Your Groq API Key

1. Go to https://console.groq.com
2. Sign up (it's free!)
3. Click **"API Keys"** in the sidebar
4. Click **"Create API Key"**
5. Copy the key (starts with `gsk_`)
6. Add it to your `.env` or Streamlit secrets

**Free tier includes:**
- 60 requests per minute
- Plenty for personal use!

---

## 📱 Using on Mobile

The app is fully responsive! Just:
1. Deploy to Streamlit Cloud
2. Open the URL on your phone
3. Add to home screen for app-like experience

---

## 🆘 Quick Troubleshooting

**"GROQ_API_KEY not found"**
→ Add your API key to `.env` or `.streamlit/secrets.toml`

**"Failed to load database"**
→ Make sure `database.json` is in the root directory

**"Tesseract not found"**
→ Install Tesseract OCR (see installation steps above)

**OCR not working**
→ Make sure image is clear and well-lit

---

## 🎯 Example Scenarios to Try

### Test Situation Analyzer
```
"Taxi driver in Delhi refusing to use meter and asking 500 rupees"
```

### Test Translator
```
"Can you help me find the train station?"
```

### Test OCR
Upload a photo of any foreign language text (menu, sign, etc.)

---

## 📚 Learn More

- **Full Documentation**: See `README.md`
- **Deployment Guide**: See `STREAMLIT_CLOUD_DEPLOYMENT.md`
- **Add Countries**: Edit `database.json`

---

## 🌟 You're Ready!

Start exploring SafeWonder and travel with confidence! 🛡️

**Questions?** Open an issue on GitHub or check the troubleshooting section.
