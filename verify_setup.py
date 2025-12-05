#!/usr/bin/env python3
"""
SafeWonder Setup Verification Script
Run this to verify your setup is complete before deployment
"""

import os
import sys
from pathlib import Path

def check_file(filepath, description):
    """Check if a file exists"""
    if Path(filepath).exists():
        print(f"✅ {description}: {filepath}")
        return True
    else:
        print(f"❌ {description} MISSING: {filepath}")
        return False

def check_directory(dirpath, description):
    """Check if a directory exists"""
    if Path(dirpath).is_dir():
        print(f"✅ {description}: {dirpath}")
        return True
    else:
        print(f"❌ {description} MISSING: {dirpath}")
        return False

def check_env_var(var_name):
    """Check if environment variable is set"""
    if os.getenv(var_name):
        print(f"✅ Environment variable set: {var_name}")
        return True
    else:
        print(f"⚠️  Environment variable not set: {var_name} (check .env or secrets.toml)")
        return False

def check_import(module_name):
    """Check if a Python module can be imported"""
    try:
        __import__(module_name)
        print(f"✅ Python package installed: {module_name}")
        return True
    except ImportError:
        print(f"❌ Python package MISSING: {module_name}")
        return False

def main():
    print("=" * 60)
    print("🛡️  SafeWonder Setup Verification")
    print("=" * 60)
    print()
    
    all_checks_passed = True
    
    # Check core files
    print("📁 Checking Core Files...")
    all_checks_passed &= check_file("app.py", "Main application")
    all_checks_passed &= check_file("database.json", "Safety database")
    all_checks_passed &= check_file("requirements.txt", "Python dependencies")
    all_checks_passed &= check_file("packages.txt", "System dependencies")
    print()
    
    # Check directories
    print("📂 Checking Directories...")
    all_checks_passed &= check_directory("components", "Components directory")
    all_checks_passed &= check_directory("utils", "Utils directory")
    all_checks_passed &= check_directory(".streamlit", "Streamlit config directory")
    print()
    
    # Check component files
    print("🧩 Checking Component Files...")
    components = [
        "profile_manager.py",
        "situation_analyzer.py",
        "situation_analyzer_ui.py",
        "culture_translator.py",
        "culture_translator_ui.py",
        "ocr_translator.py",
        "ocr_translator_ui.py"
    ]
    for component in components:
        all_checks_passed &= check_file(f"components/{component}", component)
    print()
    
    # Check utility files
    print("🛠️  Checking Utility Files...")
    utils = [
        "database_loader.py",
        "groq_client.py",
        "session_manager.py"
    ]
    for util in utils:
        all_checks_passed &= check_file(f"utils/{util}", util)
    print()
    
    # Check configuration files
    print("⚙️  Checking Configuration Files...")
    all_checks_passed &= check_file(".streamlit/config.toml", "Streamlit config")
    secrets_exists = check_file(".streamlit/secrets.toml", "Streamlit secrets")
    if not secrets_exists:
        print("   ℹ️  Note: secrets.toml is optional for local dev (can use .env)")
    print()
    
    # Check environment variables
    print("🔑 Checking Environment Variables...")
    check_env_var("GROQ_API_KEY")
    print()
    
    # Check Python packages
    print("📦 Checking Python Packages...")
    packages = [
        "streamlit",
        "groq",
        "pytesseract",
        "PIL",  # Pillow
        "dotenv",  # python-dotenv
        "gtts",
        "langdetect"
    ]
    for package in packages:
        all_checks_passed &= check_import(package)
    print()
    
    # Check documentation
    print("📚 Checking Documentation...")
    check_file("README.md", "Main README")
    check_file("QUICKSTART.md", "Quick start guide")
    check_file("STREAMLIT_CLOUD_DEPLOYMENT.md", "Deployment guide")
    print()
    
    # Check .gitignore
    print("🔒 Checking Security...")
    if check_file(".gitignore", "Git ignore file"):
        with open(".gitignore", "r") as f:
            content = f.read()
            if "secrets.toml" in content:
                print("   ✅ .gitignore excludes secrets.toml")
            else:
                print("   ⚠️  .gitignore should exclude secrets.toml")
                all_checks_passed = False
    print()
    
    # Final summary
    print("=" * 60)
    if all_checks_passed:
        print("✅ ALL CHECKS PASSED!")
        print()
        print("🚀 Your SafeWonder app is ready to deploy!")
        print()
        print("Next steps:")
        print("1. Make sure you have a Groq API key")
        print("2. Add it to .streamlit/secrets.toml or .env")
        print("3. Run: streamlit run app.py")
        print("4. Or deploy to Streamlit Cloud!")
        print()
        print("See QUICKSTART.md for detailed instructions.")
    else:
        print("⚠️  SOME CHECKS FAILED")
        print()
        print("Please fix the issues above before deploying.")
        print("See README.md for setup instructions.")
    print("=" * 60)
    
    return 0 if all_checks_passed else 1

if __name__ == "__main__":
    sys.exit(main())
