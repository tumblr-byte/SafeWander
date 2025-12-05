# SafeWonder - Travel Safety Assistant Requirements

## Introduction

SafeWonder is a comprehensive travel safety application built with Streamlit that helps travelers navigate unfamiliar environments safely. The application provides real-time situation analysis, cultural guidance, language translation, and emergency assistance by combining a structured knowledge base (database.json) with AI-powered analysis using Groq API. The system analyzes user-described situations, identifies potential scams or harassment, provides culturally-appropriate responses, and offers multilingual support through voice and text interfaces.

## Glossary

- **SafeWonder_App**: The Streamlit-based web application that serves as the main user interface
- **Situation_Analyzer**: The AI-powered module that processes user situation descriptions and matches them against the knowledge base
- **Groq_API**: The AI service used for intelligent situation analysis and response generation
- **Knowledge_Base**: The database.json file containing country-specific safety information, scams, cultural rules, and emergency contacts
- **Risk_Score**: A numerical value from 0 to 100 indicating the danger level of a reported situation
- **Polite_Culture_Translator**: The module that translates user phrases into culturally-appropriate local language expressions
- **OCR_Translator**: The optical character recognition module that extracts and translates text from images
- **User_Profile**: The onboarding data collected including name, native language, destination, gender, and travel dates
- **Emergency_Contact**: Phone numbers and locations for police, ambulance, and specialized helplines stored in the Knowledge_Base

## Requirements

### Requirement 1: User Onboarding and Profile Management

**User Story:** As a traveler, I want to provide my travel details and preferences during onboarding, so that the application can provide personalized safety guidance relevant to my destination and circumstances.

#### Acceptance Criteria

1. WHEN the SafeWonder_App launches for the first time, THE SafeWonder_App SHALL display an onboarding screen requesting user profile information
2. THE SafeWonder_App SHALL collect the following User_Profile fields: name, native_language, traveling_to_country, traveling_to_city, arrival_date, gender, and safety_preference
3. WHEN the user submits the User_Profile, THE SafeWonder_App SHALL validate that all required fields contain valid data
4. WHEN User_Profile validation succeeds, THE SafeWonder_App SHALL store the profile data in session state for use throughout the application
5. THE SafeWonder_App SHALL load the corresponding country data from the Knowledge_Base based on the traveling_to_country field

### Requirement 2: Situation Analysis with AI

**User Story:** As a traveler encountering an unfamiliar situation, I want to describe what's happening in text or voice, so that I can receive immediate analysis of potential risks and appropriate actions to take.

#### Acceptance Criteria

1. THE SafeWonder_App SHALL provide both text input and voice input options for situation descriptions
2. WHEN the user submits a situation description, THE Situation_Analyzer SHALL send the description along with relevant Knowledge_Base data to the Groq_API
3. THE Situation_Analyzer SHALL match the situation description against scam keywords, harassment patterns, and cultural rules in the Knowledge_Base
4. WHEN pattern matching completes, THE Situation_Analyzer SHALL generate a Risk_Score between 0 and 100
5. THE Situation_Analyzer SHALL return a structured response containing: Risk_Score, matched pattern name, risk explanation, recommended actions from Knowledge_Base, Emergency_Contact numbers, relevant local phrases, and cultural context

### Requirement 3: Risk Assessment and Safety Recommendations

**User Story:** As a traveler receiving situation analysis, I want clear risk levels and actionable safety steps, so that I can make informed decisions about how to respond to the situation.

#### Acceptance Criteria

1. WHEN the Situation_Analyzer returns results, THE SafeWonder_App SHALL display the Risk_Score with visual indicators (color-coded: green 0-30, yellow 31-60, red 61-100)
2. THE SafeWonder_App SHALL display the matched scam or harassment pattern name from the Knowledge_Base
3. THE SafeWonder_App SHALL present "What to Do" instructions from the Knowledge_Base in a clear, numbered list format
4. THE SafeWonder_App SHALL present "What NOT to Do" warnings from the Knowledge_Base in a visually distinct format
5. THE SafeWonder_App SHALL display relevant Emergency_Contact numbers with one-click calling capability
6. WHEN cultural context is relevant, THE SafeWonder_App SHALL display cultural notes and appropriate local phrases

### Requirement 4: Polite Culture Translator

**User Story:** As a traveler who needs to communicate with locals, I want to translate my phrases into culturally-appropriate local language, so that I can interact respectfully and effectively.

#### Acceptance Criteria

1. THE Polite_Culture_Translator SHALL accept user input in the native_language specified in User_Profile
2. WHEN the user submits a phrase for translation, THE Polite_Culture_Translator SHALL send the phrase to Groq_API with cultural context from the Knowledge_Base
3. THE Polite_Culture_Translator SHALL generate a translation in the destination country's language that is culturally appropriate
4. THE Polite_Culture_Translator SHALL provide pronunciation guidance and tone recommendations for the translated phrase
5. THE Polite_Culture_Translator SHALL support bidirectional translation between the user's native_language and the destination language
6. THE SafeWonder_App SHALL provide voice output for translated phrases using text-to-speech functionality

### Requirement 5: OCR-Based Image Translation

**User Story:** As a traveler encountering signs, menus, or documents in a foreign language, I want to photograph the text and receive instant translation, so that I can understand important information and identify potential warnings.

#### Acceptance Criteria

1. THE OCR_Translator SHALL accept image uploads from the user's device camera or file system
2. WHEN an image is uploaded, THE OCR_Translator SHALL extract text from the image using Tesseract OCR
3. THE OCR_Translator SHALL detect the language of the extracted text automatically
4. WHEN text extraction completes, THE OCR_Translator SHALL send the extracted text to Groq_API for translation and analysis
5. THE SafeWonder_App SHALL display the original extracted text, detected language, and translated text in the user's native_language
6. WHEN the Groq_API identifies suspicious content in the text, THE SafeWonder_App SHALL display a warning message with explanation

### Requirement 6: Visual Design and User Experience

**User Story:** As a user of the SafeWonder app, I want a beautiful, intuitive interface that doesn't feel basic, so that I feel confident using the app in stressful situations.

#### Acceptance Criteria

1. THE SafeWonder_App SHALL display the logo.png file prominently in the header of all pages
2. THE SafeWonder_App SHALL use custom CSS styling to create a visually appealing interface with consistent color scheme and typography
3. THE SafeWonder_App SHALL implement smooth transitions and animations for user interactions
4. THE SafeWonder_App SHALL use icons and visual indicators to enhance readability and reduce cognitive load
5. THE SafeWonder_App SHALL maintain responsive design that works on mobile and desktop devices
6. THE SafeWonder_App SHALL organize features into clearly labeled sections with intuitive navigation

### Requirement 7: Emergency Access and Quick Actions

**User Story:** As a traveler in a potentially dangerous situation, I want immediate access to emergency contacts and SOS features, so that I can get help quickly without navigating through multiple screens.

#### Acceptance Criteria

1. THE SafeWonder_App SHALL display a persistent emergency button visible on all screens
2. WHEN the emergency button is activated, THE SafeWonder_App SHALL display Emergency_Contact numbers for the current destination country
3. THE SafeWonder_App SHALL provide one-click access to call emergency services directly from the displayed numbers
4. THE SafeWonder_App SHALL display the nearest hospital and police station locations from the Knowledge_Base
5. THE SafeWonder_App SHALL display embassy contact information relevant to the user's nationality when available in the Knowledge_Base

### Requirement 8: Knowledge Base Integration

**User Story:** As a system administrator, I want the application to dynamically load country-specific data from the database.json file, so that safety information remains accurate and can be updated without code changes.

#### Acceptance Criteria

1. WHEN the SafeWonder_App initializes, THE SafeWonder_App SHALL load the Knowledge_Base from the database.json file path specified in environment configuration
2. THE SafeWonder_App SHALL parse the Knowledge_Base structure including countries, emergency_numbers, transport, common_scams, harassment_patterns, culture, local_phrases, laws, and important_locations
3. WHEN the User_Profile specifies a traveling_to_country, THE SafeWonder_App SHALL filter Knowledge_Base data to the relevant country entry
4. THE Situation_Analyzer SHALL access scam keywords and harassment patterns from the Knowledge_Base for pattern matching
5. THE SafeWonder_App SHALL handle missing or incomplete Knowledge_Base entries gracefully with appropriate fallback messages

### Requirement 9: API Integration and Configuration

**User Story:** As a developer deploying the application, I want secure API key management and configurable service endpoints, so that the application can be deployed in different environments without hardcoding credentials.

#### Acceptance Criteria

1. THE SafeWonder_App SHALL load the GROK_API_KEY from environment variables or .env file
2. WHEN the GROK_API_KEY is missing or invalid, THE SafeWonder_App SHALL display an error message and prevent API-dependent features from executing
3. THE SafeWonder_App SHALL use the Groq_API endpoint for all AI-powered analysis and translation requests
4. THE SafeWonder_App SHALL implement error handling for API failures with user-friendly error messages
5. THE SafeWonder_App SHALL respect API rate limits and implement appropriate retry logic with exponential backoff

### Requirement 10: Multi-Feature Navigation

**User Story:** As a user of SafeWonder, I want to easily switch between situation analysis, translation, and OCR features, so that I can access the right tool for my current need.

#### Acceptance Criteria

1. THE SafeWonder_App SHALL provide a navigation menu or sidebar with clearly labeled options for each major feature
2. THE SafeWonder_App SHALL maintain User_Profile data and session state when navigating between features
3. WHEN the user selects a feature from navigation, THE SafeWonder_App SHALL display the corresponding interface within 1 second
4. THE SafeWonder_App SHALL indicate the currently active feature with visual highlighting in the navigation menu
5. THE SafeWonder_App SHALL preserve user input and results when switching between features and returning
