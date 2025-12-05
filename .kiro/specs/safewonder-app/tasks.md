# SafeWonder Implementation Plan

- [x] 1. Set up project structure and dependencies


  - Create modular directory structure: `components/`, `utils/`, `assets/`
  - Configure requirements.txt with all necessary packages (streamlit, groq, pytesseract, gTTS, Pillow, python-dotenv, langdetect)
  - Set up packages.txt for system dependencies (tesseract-ocr with language packs)
  - Create .streamlit/config.toml with custom theme configuration
  - Implement environment variable loading from .env file
  - _Requirements: 9.1, 9.2_





- [ ] 2. Create utility modules for core functionality
  - [ ] 2.1 Implement database loader utility
    - Write `utils/database_loader.py` to load and parse database.json


    - Create function to filter country data by country ID
    - Implement error handling for missing or malformed JSON data
    - Add caching mechanism for loaded data
    - _Requirements: 8.1, 8.2, 8.3, 8.5_


  - [ ] 2.2 Implement Groq API client wrapper
    - Write `utils/groq_client.py` with retry logic and exponential backoff
    - Create function to validate API key on initialization




    - Implement error handling for rate limits, timeouts, and invalid responses
    - Add response parsing and validation
    - _Requirements: 9.1, 9.2, 9.3, 9.4, 9.5_

  - [ ] 2.3 Create session state manager
    - Write `utils/session_manager.py` to initialize and manage Streamlit session state
    - Implement functions to save/retrieve user profile from session
    - Create function to persist navigation state across page reloads
    - _Requirements: 1.4, 10.2, 10.5_


- [ ] 3. Build user profile and onboarding system
  - [ ] 3.1 Create profile manager component
    - Write `components/profile_manager.py` with UserProfile dataclass
    - Implement profile validation function checking all required fields
    - Create function to load country data based on selected destination




    - _Requirements: 1.1, 1.3, 1.5_
  - [ ] 3.2 Design onboarding UI
    - Create multi-step onboarding form with progress indicator
    - Add input fields for name, native_language, traveling_to_country, traveling_to_city, arrival_date, gender, safety_preference
    - Implement form validation with inline error messages


    - Add animated welcome screen with logo display
    - Style with custom CSS for glassmorphism effect
    - _Requirements: 1.1, 1.2, 6.1, 6.2, 6.3_
  - [ ] 3.3 Implement profile submission and storage
    - Connect form submission to validation function
    - Save validated profile to session state
    - Load corresponding country data from database.json

    - Redirect to main app interface after successful onboarding
    - _Requirements: 1.3, 1.4, 1.5_

- [ ] 4. Implement Situation Analyzer module
  - [x] 4.1 Create situation analyzer core logic




    - Write `components/situation_analyzer.py` with SituationAnalysis dataclass
    - Implement keyword matching function against scams and harassment patterns from JSON
    - Create Groq API prompt builder incorporating user situation, profile, and knowledge base context
    - Implement risk score calculation (0-100) based on matched patterns
    - Parse Groq API response into structured SituationAnalysis object


    - _Requirements: 2.2, 2.3, 2.4, 2.5, 3.2_
  - [ ] 4.2 Build situation analyzer UI
    - Create text area for situation description input
    - Add voice input button with recording indicator (using streamlit-audio-recorder or similar)
    - Implement "Analyze Situation" button with loading spinner
    - Design risk score display with color-coded circular gauge (green 0-30, yellow 31-60, red 61-100)
    - Create expandable sections for: pattern matched, risk explanation, what to do, what not to do, emergency contacts, local phrases, cultural notes
    - Add copy-to-clipboard buttons for phone numbers

    - Style with custom CSS animations and visual indicators
    - _Requirements: 2.1, 3.1, 3.2, 3.3, 3.4, 3.5, 3.6, 6.2, 6.3, 6.4_
  - [ ] 4.3 Integrate with Groq API
    - Connect analyzer to Groq API client with proper error handling
    - Implement prompt template with situation, profile, and knowledge base context



    - Parse API response and extract risk assessment data
    - Handle API failures gracefully with user-friendly error messages
    - _Requirements: 2.2, 2.3, 2.5, 9.3, 9.4_


- [ ] 5. Implement Polite Culture Translator module
  - [ ] 5.1 Create translation core logic
    - Write `components/culture_translator.py` with TranslationResult dataclass
    - Implement function to retrieve common phrases from database.json
    - Create Groq API prompt builder for culturally-appropriate translation
    - Implement text-to-speech function using gTTS
    - Parse Groq response for translated text, pronunciation, tone guidance, and cultural notes
    - _Requirements: 4.2, 4.3, 4.4_
  - [ ] 5.2 Build translator UI
    - Create two-column layout for source and target languages
    - Add text input field with language indicator
    - Implement quick-select buttons for common phrases from JSON
    - Add "Translate" button with loading state
    - Display pronunciation guide with phonetic text
    - Add play audio button for TTS output
    - Show tone and etiquette tips in styled callout box
    - Implement swap languages button for bidirectional translation
    - _Requirements: 4.1, 4.5, 4.6, 6.2, 6.3_
  - [ ] 5.3 Integrate translation with Groq API
    - Connect translator to Groq API with cultural context from JSON
    - Implement prompt template requesting polite, culturally-appropriate translation
    - Generate audio file from translated text using TTS
    - Handle translation errors and unsupported language pairs
    - _Requirements: 4.2, 4.3, 4.4, 9.3, 9.4_

- [ ] 6. Implement OCR Translator module
  - [ ] 6.1 Create OCR processing logic
    - Write `components/ocr_translator.py` with OCRResult dataclass
    - Implement image preprocessing function (resize, enhance contrast)
    - Create text extraction function using pytesseract
    - Implement language detection using langdetect library
    - _Requirements: 5.2, 5.3_
  - [ ] 6.2 Build OCR translator UI
    - Create image upload area with drag-drop and camera capture support
    - Add image preview component
    - Implement "Extract & Translate" button with loading animation
    - Display side-by-side view: original extracted text and translated text
    - Show detected language badge
    - Add warning banner for suspicious content (conditional display)
    - Display explanation text below translation
    - _Requirements: 5.1, 5.5, 5.6, 6.2, 6.3_
  - [ ] 6.3 Integrate OCR with Groq API for analysis
    - Send extracted text to Groq API for translation and safety analysis
    - Implement prompt template requesting translation and scam detection
    - Parse response for translated text, warning level, and suspicious elements
    - Display warnings prominently when detected
    - _Requirements: 5.4, 5.5, 5.6, 9.3, 9.4_

- [ ] 7. Create main application structure and navigation
  - [x] 7.1 Build main app.py entry point



    - Initialize Streamlit page configuration with custom title and icon
    - Load custom CSS from external file or inline
    - Initialize session state on first load
    - Check if user has completed onboarding, redirect if needed
    - _Requirements: 6.1, 6.2, 10.1_
  - [ ] 7.2 Implement navigation system
    - Create sidebar navigation with icons and labels for: Home, Situation Analyzer, Polite Translator, OCR Translator, Profile Settings, Emergency
    - Implement page routing based on selected navigation item
    - Add visual highlighting for currently active feature
    - Ensure navigation preserves session state
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 6.6_
  - [ ] 7.3 Create persistent emergency button
    - Implement floating emergency button visible on all pages
    - Position button in bottom-right (mobile) or top-right (desktop)
    - Add pulsing animation effect
    - Connect button to emergency contact display
    - _Requirements: 7.1, 7.2, 6.2, 6.3_
  - [ ] 7.4 Build emergency contact display
    - Create modal or expandable section showing emergency numbers from JSON
    - Display police, ambulance, women helpline, fire numbers
    - Add one-click calling capability (tel: links)
    - Show nearest hospital and police station from JSON
    - Display embassy contact information if available
    - _Requirements: 7.2, 7.3, 7.4, 7.5_

- [ ] 8. Implement custom styling and visual design
  - [ ] 8.1 Create custom CSS stylesheet
    - Define color palette variables (primary, secondary, success, warning, danger, background, surface, text colors)
    - Style typography with Inter font family
    - Create card component styles with glassmorphism effect
    - Style input fields with focus states and glow effects
    - Design button styles with hover and active states
    - _Requirements: 6.2, 6.3, 6.4_
  - [ ] 8.2 Implement animations and transitions
    - Add page transition fade-in animations (300ms)
    - Create button click scale animations (100ms)
    - Implement loading spinner with brand colors
    - Add success checkmark animation
    - Create risk score count-up animation
    - Add pulsing glow effect for emergency button
    - _Requirements: 6.3, 6.4_
  - [ ] 8.3 Ensure responsive design
    - Test layout on mobile (640px), tablet (1024px), and desktop breakpoints
    - Implement collapsible sidebar for mobile
    - Adjust component sizing for different screen sizes
    - Ensure touch targets are minimum 44x44px on mobile
    - _Requirements: 6.5_

- [ ] 9. Add voice input and output capabilities
  - [ ] 9.1 Implement voice input for situation analyzer
    - Integrate streamlit-audio-recorder or speech recognition library
    - Add microphone button with recording indicator
    - Convert audio to text using speech recognition
    - Handle audio input errors gracefully
    - _Requirements: 2.1_
  - [ ] 9.2 Implement text-to-speech for translations
    - Use gTTS to generate audio from translated text
    - Create audio player component in Streamlit
    - Add play button with loading state while generating audio
    - Cache generated audio files in session to avoid regeneration
    - _Requirements: 4.6_

- [ ] 10. Implement error handling and user feedback
  - [ ] 10.1 Add comprehensive error handling
    - Wrap all API calls in try-except blocks with specific error types
    - Handle rate limit errors with retry suggestions
    - Handle timeout errors with network check prompts
    - Handle invalid API key errors with configuration guidance
    - Handle OCR errors with image quality suggestions
    - _Requirements: 9.4, 8.5_
  - [ ] 10.2 Create user feedback components
    - Implement toast notifications for transient errors using st.toast
    - Create modal dialogs for critical errors
    - Add inline validation messages for form inputs
    - Show loading states for all async operations (spinners, progress bars)
    - _Requirements: 6.3, 6.4_

- [ ] 11. Final integration and polish
  - [ ] 11.1 Integrate all components in main app
    - Wire up navigation to all feature modules
    - Ensure profile data flows correctly to all components
    - Verify knowledge base data is accessible throughout app
    - Test emergency button functionality from all pages
    - _Requirements: 10.1, 10.2, 10.3, 10.4, 10.5_
  - [ ] 11.2 Add logo and branding
    - Place logo.png in assets/ directory
    - Display logo in header on all pages
    - Ensure logo scales properly on different screen sizes
    - Add favicon using logo
    - _Requirements: 6.1_
  - [ ] 11.3 Optimize performance
    - Implement caching for database.json loading using st.cache_data
    - Cache Groq API responses for identical queries using st.cache_data
    - Optimize image compression before OCR processing
    - Minimize redundant API calls
    - _Requirements: 8.1, 8.2, 8.3, 8.4_
  - [ ] 11.4 Create deployment documentation
    - Document environment variable setup
    - Create deployment guide for Streamlit Cloud
    - Document Tesseract installation requirements
    - Add troubleshooting section for common issues
    - _Requirements: 9.1, 9.2_
  - [ ] 11.5 Manual testing and quality assurance
    - Test complete user flow from onboarding to each feature
    - Verify all features work with sample data
    - Test error scenarios (no API key, invalid country, poor image quality)
    - Verify responsive design on multiple devices
    - Test accessibility with keyboard navigation
    - _Requirements: 6.5, 6.6_
