# 🚀 Streamlit Cloud Deployment Guide

## Quick Deployment Steps

### 1. Prepare Your Repository

Make sure your repository has these files:
- ✅ `app.py` - Main application file
- ✅ `requirements.txt` - Python dependencies
- ✅ `packages.txt` - System dependencies (Tesseract)
- ✅ `database.json` - Country safety data
- ✅ `.streamlit/config.toml` - Streamlit configuration
- ✅ All component files in `components/` and `utils/`

### 2. Push to GitHub

```bash
git add .
git commit -m "Ready for Streamlit Cloud deployment"
git push origin main
```

### 3. Deploy on Streamlit Cloud

1. Go to https://share.streamlit.io
2. Click **"New app"**
3. Connect your GitHub account (if not already connected)
4. Select your repository
5. Set the main file path: `app.py`
6. Click **"Deploy"**

### 4. Configure Secrets

**IMPORTANT**: After deployment, add your Groq API key:

1. Go to your app dashboard on Streamlit Cloud
2. Click **"Settings"** → **"Secrets"**
3. Add the following:

```toml
GROQ_API_KEY = "your_actual_groq_api_key_here"
```

4. Click **"Save"**
5. Your app will automatically restart with the new secrets

### 5. Get Your Groq API Key

If you don't have a Groq API key yet:

1. Go to https://console.groq.com
2. Sign up or log in
3. Navigate to **API Keys**
4. Click **"Create API Key"**
5. Copy the key (starts with `gsk_`)
6. Add it to Streamlit Cloud secrets (step 4 above)

## 📋 Deployment Checklist

Before deploying, verify:

- [ ] All files are committed to GitHub
- [ ] `requirements.txt` has all Python packages
- [ ] `packages.txt` has Tesseract OCR dependencies
- [ ] `database.json` is in the root directory
- [ ] `.streamlit/config.toml` exists
- [ ] `.gitignore` excludes `.streamlit/secrets.toml` (don't commit your API key!)
- [ ] All import statements in `app.py` are correct
- [ ] No hardcoded API keys in the code

## 🔧 Troubleshooting

### App Won't Start

**Check the logs:**
1. Go to your app on Streamlit Cloud
2. Click **"Manage app"** → **"Logs"**
3. Look for error messages

**Common issues:**
- Missing dependencies in `requirements.txt`
- Missing system packages in `packages.txt`
- API key not configured in secrets
- Import errors (check file paths)

### Tesseract Not Found

Make sure `packages.txt` includes:
```
tesseract-ocr
tesseract-ocr-eng
tesseract-ocr-jpn
tesseract-ocr-hin
```

### Groq API Errors

1. Verify your API key is correct in secrets
2. Check you have API credits at https://console.groq.com
3. Verify rate limits (60 requests/minute on free tier)

### Import Errors

Make sure all component files are in the correct directories:
```
components/
  - profile_manager.py
  - situation_analyzer.py
  - situation_analyzer_ui.py
  - culture_translator.py
  - culture_translator_ui.py
  - ocr_translator.py
  - ocr_translator_ui.py
utils/
  - database_loader.py
  - groq_client.py
  - session_manager.py
```

## 🎯 Post-Deployment

After successful deployment:

1. **Test all features:**
   - Complete onboarding
   - Try situation analyzer
   - Test translator
   - Upload image for OCR
   - Check emergency contacts

2. **Share your app:**
   - Your app URL: `https://your-app-name.streamlit.app`
   - Share with friends and travelers!

3. **Monitor usage:**
   - Check Streamlit Cloud analytics
   - Monitor Groq API usage at console.groq.com

## 🔄 Updating Your App

To update your deployed app:

```bash
# Make changes to your code
git add .
git commit -m "Update: description of changes"
git push origin main
```

Streamlit Cloud will automatically detect the changes and redeploy your app!

## 🌟 Custom Domain (Optional)

To use a custom domain:
1. Upgrade to Streamlit Cloud Pro
2. Go to app settings
3. Add your custom domain
4. Update DNS records as instructed

## 📊 Monitoring

Monitor your app's performance:
- **Streamlit Cloud Dashboard**: View app analytics
- **Groq Console**: Monitor API usage and costs
- **GitHub**: Track code changes and issues

## 🆘 Need Help?

- **Streamlit Docs**: https://docs.streamlit.io
- **Streamlit Community**: https://discuss.streamlit.io
- **Groq Docs**: https://console.groq.com/docs

---

**Your SafeWonder app is now live and helping travelers worldwide! 🛡️**
