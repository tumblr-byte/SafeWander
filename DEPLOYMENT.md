# SafeWonder Deployment Guide 🚀

## Quick Deployment to Streamlit Cloud

### Step 1: Prepare Your Repository

1. Make sure all files are committed:
```bash
git add .
git commit -m "SafeWonder app ready for deployment"
git push origin main
```

### Step 2: Deploy on Streamlit Cloud

1. Go to [share.streamlit.io](https://share.streamlit.io)
2. Sign in with your GitHub account
3. Click **"New app"** button
4. Fill in the deployment form:
   - **Repository**: Select your SafeWonder repository
   - **Branch**: `main` (or your default branch)
   - **Main file path**: `app.py`
5. Click **"Advanced settings"**

### Step 3: Configure Secrets

In the Advanced settings, add your Groq API key in the **Secrets** section:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

**Important**: Replace the API key above with your actual Groq API key from `.env.example`

### Step 4: Deploy

1. Click **"Deploy!"** button
2. Wait for the app to build (usually 2-5 minutes)
3. Your app will be live at: `https://[your-app-name].streamlit.app`

## Managing Secrets After Deployment

If you need to update your API key later:

1. Go to your app dashboard on Streamlit Cloud
2. Click on **"Settings"** (⚙️ icon)
3. Navigate to **"Secrets"** section
4. Update the `GROQ_API_KEY` value
5. Click **"Save"**
6. The app will automatically restart with new secrets

## Local Development Setup

### Prerequisites

- Python 3.8 or higher
- Tesseract OCR installed on your system

### Install Tesseract OCR

**Windows:**
1. Download installer from [GitHub](https://github.com/UB-Mannheim/tesseract/wiki)
2. Run the installer
3. Add Tesseract to your PATH or update `.env` with the installation path

**macOS:**
```bash
brew install tesseract
```

**Linux (Ubuntu/Debian):**
```bash
sudo apt-get update
sudo apt-get install tesseract-ocr
sudo apt-get install tesseract-ocr-eng tesseract-ocr-jpn tesseract-ocr-hin
```

### Install Python Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

1. Copy the example environment file:
```bash
cp .env.example .env
```

2. Edit `.env` and add your Groq API key:
```
GROQ_API_KEY=your_actual_api_key_here
```

### Run Locally

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Troubleshooting

### Issue: "GROQ_API_KEY not found"

**Solution**: 
- For Streamlit Cloud: Check that you've added the secret in the dashboard
- For local: Verify `.env` file exists and contains the API key

### Issue: "Failed to load database"

**Solution**: 
- Ensure `database.json` is in the root directory
- Check that the JSON file is valid (no syntax errors)

### Issue: Tesseract not found

**Solution**:
- Verify Tesseract is installed: `tesseract --version`
- For Windows: Update `TESSERACT_PATH` in `.env` to point to `tesseract.exe`
- For Streamlit Cloud: Tesseract is automatically installed via `packages.txt`

### Issue: Import errors

**Solution**:
- Verify all dependencies are installed: `pip install -r requirements.txt`
- Check Python version: `python --version` (should be 3.8+)

### Issue: App is slow or timing out

**Solution**:
- Check your internet connection
- Verify Groq API is responding (check status page)
- Reduce image size before uploading to OCR

## File Structure for Deployment

Make sure these files are in your repository:

```
safewonder/
├── app.py                          ✅ Main entry point
├── components/                     ✅ All component files
├── utils/                          ✅ All utility files
├── assets/                         ✅ Logo and static files
├── .streamlit/
│   └── config.toml                ✅ Theme configuration
├── database.json                   ✅ Country data
├── requirements.txt                ✅ Python dependencies
├── packages.txt                    ✅ System dependencies
└── README.md                       ✅ Documentation
```

**Do NOT commit:**
- `.env` (contains secrets)
- `.streamlit/secrets.toml` (local secrets only)
- `__pycache__/` directories
- `.pyc` files

## Environment Variables Reference

### Required
- `GROQ_API_KEY`: Your Groq API key for AI analysis

### Optional
- `DATABASE_PATH`: Path to database.json (default: `database.json`)
- `APP_ENV`: Environment mode (default: `production`)
- `DEBUG`: Enable debug mode (default: `False`)
- `TESSERACT_PATH`: Path to Tesseract executable (Windows only)

## Streamlit Cloud Configuration

The app uses custom configuration in `.streamlit/config.toml`:

```toml
[theme]
primaryColor = "#6366F1"
backgroundColor = "#0F172A"
secondaryBackgroundColor = "#1E293B"
textColor = "#F1F5F9"
font = "sans serif"

[server]
headless = true
port = 8501
enableCORS = false
enableXsrfProtection = true
```

You can customize these values to change the app's appearance.

## Performance Tips

1. **Image Optimization**: Compress images before OCR processing
2. **API Caching**: Identical queries are cached in session state
3. **Database Loading**: Country data is loaded once per session
4. **Lazy Loading**: Components load only when accessed

## Security Best Practices

1. **Never commit API keys** to the repository
2. **Use Streamlit secrets** for sensitive data
3. **Validate user inputs** before processing
4. **Sanitize file uploads** to prevent malicious content
5. **Use HTTPS** in production (automatic on Streamlit Cloud)

## Monitoring Your App

On Streamlit Cloud dashboard, you can:
- View app logs for debugging
- Monitor resource usage
- Check deployment status
- Manage secrets
- Reboot the app if needed

## Updating Your Deployed App

1. Make changes to your code locally
2. Test thoroughly with `streamlit run app.py`
3. Commit and push to GitHub:
```bash
git add .
git commit -m "Update: description of changes"
git push origin main
```
4. Streamlit Cloud will automatically detect changes and redeploy

## Support

If you encounter issues:
1. Check the [Streamlit Community Forum](https://discuss.streamlit.io/)
2. Review [Streamlit Documentation](https://docs.streamlit.io/)
3. Check [Groq API Documentation](https://console.groq.com/docs)

---

**Your SafeWonder app is now ready to deploy! 🎉**
