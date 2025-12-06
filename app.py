import streamlit as st
import json
import os
from groq import Groq
from datetime import datetime

# Page config
st.set_page_config(
    page_title="SafeWander - Your Personalized Travel Safety Companion",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');
    
    * { font-family: 'Inter', sans-serif; }
    
    .onboarding-container {
        max-width: 700px;
        margin: 3rem auto;
        padding: 3rem;
        background: white;
        border-radius: 24px;
        box-shadow: 0 20px 60px rgba(0,0,0,0.15);
    }
    
    .onboarding-title {
        font-size: 2.5rem;
        font-weight: 800;
        text-align: center;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin-bottom: 1rem;
    }
    
    .onboarding-subtitle {
        text-align: center;
        color: #64748b;
        font-size: 1.1rem;
        margin-bottom: 2rem;
    }
    
    .progress-bar {
        width: 100%;
        height: 8px;
        background: #e2e8f0;
        border-radius: 10px;
        margin: 2rem 0;
        overflow: hidden;
    }
    
    .progress-fill {
        height: 100%;
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        border-radius: 10px;
        transition: width 0.3s ease;
    }
    
    .welcome-banner {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        padding: 2rem;
        border-radius: 20px;
        margin-bottom: 2rem;
        box-shadow: 0 10px 30px rgba(102, 126, 234, 0.3);
    }
    
    .welcome-greeting {
        font-size: 2rem;
        font-weight: 800;
        margin-bottom: 0.5rem;
    }
    
    .welcome-subtitle {
        font-size: 1.1rem;
        opacity: 0.95;
    }
    
    .priority-alert {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-left: 5px solid #ef4444;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
    }
    
    .priority-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #991b1b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .priority-item {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        color: #7f1d1d;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .recommendation-card {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-left: 5px solid #3b82f6;
    }
    
    .rec-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1e40af;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .rec-item {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        color: #1e40af;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .cultural-bridge {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        border-left: 5px solid #f59e0b;
    }
    
    .cultural-title {
        font-size: 1.2rem;
        font-weight: 700;
        color: #92400e;
        margin-bottom: 1rem;
    }
    
    .cultural-tip {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        margin: 0.8rem 0;
        color: #78350f;
        font-size: 0.95rem;
        line-height: 1.6;
    }
    
    .phrase-highlight {
        background: linear-gradient(135deg, #ddd6fe 0%, #c7d2fe 100%);
        border-radius: 12px;
        padding: 1.2rem;
        margin: 1rem 0;
        border-left: 4px solid #7c3aed;
    }
    
    .phrase-need {
        font-size: 0.85rem;
        color: #5b21b6;
        font-weight: 600;
        margin-bottom: 0.5rem;
    }
    
    .phrase-text {
        font-size: 1.2rem;
        font-weight: 700;
        color: #6d28d9;
    }
    
    .question-card {
        background: white;
        border-radius: 16px;
        padding: 1.5rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
    }
    
    .threat-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.6rem 1.5rem;
        border-radius: 30px;
        font-weight: 700;
        font-size: 1rem;
        margin: 1rem 0;
    }
    
    .threat-high { background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%); color: white; }
    .threat-medium { background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%); color: white; }
    .threat-low { background: linear-gradient(135deg, #10b981 0%, #059669 100%); color: white; }
    
    .action-item {
        display: flex;
        gap: 0.8rem;
        margin: 0.8rem 0;
        align-items: flex-start;
    }
    
    .action-num {
        background: #667eea;
        color: white;
        width: 26px;
        height: 26px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;
        font-size: 0.85rem;
        flex-shrink: 0;
    }
    
    .action-text {
        font-size: 0.95rem;
        color: #475569;
        line-height: 1.6;
    }
    
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        border: none;
        padding: 1rem 2.5rem;
        border-radius: 30px;
        font-size: 1.1rem;
        transition: all 0.3s;
        width: 100%;
    }
    
    .stButton>button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'profile_complete' not in st.session_state:
    st.session_state.profile_complete = False
if 'profile' not in st.session_state:
    st.session_state.profile = {}
if 'onboarding_step' not in st.session_state:
    st.session_state.onboarding_step = 0
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []

# Countries and cities
COUNTRIES = {
    "India": ["Delhi", "Mumbai", "Bangalore", "Goa", "Jaipur", "Agra", "Kolkata"],
    "Thailand": ["Bangkok", "Phuket", "Chiang Mai", "Pattaya", "Krabi"],
    "Mexico": ["Mexico City", "Cancun", "Playa del Carmen", "Guadalajara", "Oaxaca"],
    "USA": ["New York", "Los Angeles", "Las Vegas", "Miami", "San Francisco"],
    "Brazil": ["Rio de Janeiro", "São Paulo", "Salvador", "Brasília"]
}

LANGUAGES = ["English", "Spanish", "Portuguese", "French", "German", "Mandarin", "Hindi", "Japanese", "Korean", "Arabic"]

INTERESTS = {
    "🏖️ Beach & Relaxation": "beaches",
    "🏛️ Culture & History": "culture",
    "🍜 Food & Cuisine": "food",
    "🎉 Nightlife & Entertainment": "nightlife",
    "💼 Business": "business",
    "🧘 Spiritual & Wellness": "wellness",
    "🏔️ Adventure & Nature": "adventure"
}

# Load data
@st.cache_data
def load_safety_data():
    if os.path.exists("dataset.json"):
        with open("dataset.json", "r") as f:
            return json.load(f)
    return {"countries": ["India", "Thailand", "Mexico", "USA", "Brazil"]}

# Init Groq
def init_groq():
    try:
        api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
        if api_key:
            return Groq(api_key=api_key)
    except:
        pass
    return None

# Get personalized priorities
def get_personalized_priorities(profile, data):
    priorities = []
    
    # Gender-based
    if profile.get('gender') == 'Female':
        priorities.append("🚺 Solo female traveler safety: Avoid isolated areas after dark, use licensed taxis, stay in well-reviewed accommodations")
    
    # Age-based
    age = profile.get('age_range', '')
    if age in ['18-25', '26-35']:
        priorities.append("🎒 Young traveler alert: Common targets for scams. Always verify prices and use official services")
    elif age in ['50+']:
        priorities.append("👴 Senior traveler: Take extra care with mobility, avoid crowded areas during peak hours")
    
    # Interest-based
    interest = profile.get('interest', '')
    if interest == 'nightlife':
        priorities.append("🌙 Nightlife safety: Never leave drinks unattended, use official taxis, travel in groups")
    elif interest == 'food':
        priorities.append("🍽️ Food explorer: Eat at busy stalls, avoid pre-cut fruits, drink bottled water only")
    elif interest == 'adventure':
        priorities.append("⛰️ Adventure safety: Use licensed guides, inform someone of your plans, check weather")
    
    # Location-specific
    destination = profile.get('destination_country', '')
    for scam in data.get("transport_scams", []):
        if scam.get("country") == destination:
            priorities.append(f"🚖 {scam.get('scam_type', 'Transport scam')}: {scam.get('safety_advice', 'Be cautious')}")
            break
    
    return priorities[:4]

# Get personalized recommendations
def get_personalized_recommendations(profile, data):
    recs = []
    interest = profile.get('interest', '')
    destination = profile.get('destination_country', '')
    city = profile.get('destination_city', '')
    
    if interest == 'food':
        recs.append(f"🍜 Best street food areas in {city}: Look for crowded local spots, morning markets are safest")
        recs.append("💡 Food safety: Choose freshly cooked items, avoid raw salads, peel fruits yourself")
    elif interest == 'culture':
        recs.append(f"🏛️ Must-visit cultural sites in {city}: Research dress codes, hire licensed guides")
        recs.append("📸 Photography etiquette: Always ask permission at religious sites")
    elif interest == 'nightlife':
        recs.append(f"🎉 Safe nightlife zones in {city}: Stick to tourist-friendly areas, avoid unlicensed venues")
        recs.append("🚕 Night transport: Pre-book rides, share trip details with friends")
    elif interest == 'beaches':
        recs.append(f"🏖️ Best beaches near {city}: Use public beaches during day, avoid isolated areas")
        recs.append("⚠️ Beach safety: Don't leave valuables unattended, watch for strong currents")
    else:
        recs.append(f"✨ Top experiences in {city}: Research beforehand, use official tour operators")
        recs.append("🗺️ Navigation: Download offline maps, keep hotel card with address")
    
    return recs

# Get cultural bridge tips
def get_cultural_bridge(profile, data):
    home = profile.get('home_country', '')
    destination = profile.get('destination_country', '')
    
    tips = []
    
    for culture in data.get("cultural_guidelines", []):
        if culture.get("country") == destination:
            tips.append(f"👕 Dress code: {culture.get('dress', 'Dress modestly')}")
            tips.append(f"🤝 Local customs: {culture.get('etiquette', 'Be respectful')}")
    
    # Add language-specific
    if home == "USA" and destination == "India":
        tips.append("💬 Communication: Indians are friendly but personal space is different. Head wobble means yes!")
    elif home == "USA" and destination == "Thailand":
        tips.append("🙏 Respect: Never touch someone's head or point feet at people/Buddha images")
    
    return tips if tips else ["🌍 Research local customs before arriving", "📱 Download translation app"]

# Get essential phrases
def get_priority_phrases(profile):
    interest = profile.get('interest', '')
    destination = profile.get('destination_country', '')
    
    phrases = []
    
    if destination == "India":
        if interest == 'food':
            phrases.append(("For food vendors", "Kitna hai?", "How much?"))
            phrases.append(("Important", "Teekha nahi", "Not spicy"))
        else:
            phrases.append(("Essential", "Namaste", "Hello"))
            phrases.append(("Critical", "Madad karo!", "Help!"))
    elif destination == "Thailand":
        if interest == 'nightlife':
            phrases.append(("Safety", "Tao rai?", "How much?"))
            phrases.append(("Emergency", "Chuay duay!", "Help!"))
        else:
            phrases.append(("Greeting", "Sawasdee", "Hello"))
            phrases.append(("Respect", "Khob khun", "Thank you"))
    elif destination == "Mexico":
        phrases.append(("Essential", "¿Cuánto cuesta?", "How much?"))
        phrases.append(("Emergency", "¡Ayuda!", "Help!"))
    
    return phrases if phrases else [("Basic", "Hello", "Hello"), ("Basic", "Thank you", "Thank you")]

# AI response with profile context
def get_ai_response(query, profile, groq_client, data):
    # Build personalized context
    name = profile.get('name', 'Traveler')
    age = profile.get('age_range', '')
    gender = profile.get('gender', '')
    interest = profile.get('interest', '')
    destination = f"{profile.get('destination_city', '')}, {profile.get('destination_country', '')}"
    
    context_parts = [f"Traveler profile: {name}, {age}, {gender}, interested in {interest}, visiting {destination}"]
    
    # Add relevant scams
    for scam in data.get("transport_scams", []):
        if scam.get("country") == profile.get('destination_country'):
            context_parts.append(f"{scam.get('scam_type')}: Normal {scam.get('normal_rate')}, Scam {scam.get('scam_rate')}")
    
    context = "\n".join(context_parts[:5])
    
    system_prompt = f"""You are SafeWander AI helping {name}, a {age} {gender} traveler exploring {interest} in {destination}.

Provide personalized advice:
1. Threat level (HIGH/MEDIUM/LOW)
2. Brief assessment (2-3 sentences)
3. 3-4 specific actions tailored to their profile
4. Consider their gender, age, and interests in the advice

Be concise and actionable."""

    user_prompt = f"{query}\n\nContext: {context}"
    
    try:
        if groq_client:
            response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.6,
                max_tokens=500
            )
            return response.choices[0].message.content
        return f"Analysis: Based on your profile, be cautious. {context}"
    except:
        return f"Unable to analyze. Stay alert."

# Parse response
def parse_response(text):
    threat = "MEDIUM"
    if "HIGH" in text.upper():
        threat = "HIGH"
    elif "LOW" in text.upper():
        threat = "LOW"
    
    lines = [l.strip() for l in text.split('\n') if l.strip()]
    assessment = []
    actions = []
    
    for line in lines:
        if any(w in line.lower() for w in ["action", "step", "should", "do", "advise"]):
            clean = line.lstrip('0123456789.-*• ').strip()
            if clean and len(actions) < 4:
                actions.append(clean)
        elif len(assessment) < 3 and not line.startswith(("HIGH", "MEDIUM", "LOW")):
            assessment.append(line)
    
    return {
        "threat": threat,
        "assessment": ' '.join(assessment) if assessment else "Analyzing situation...",
        "actions": actions if actions else ["Stay alert", "Assess situation", "Seek help if needed"]
    }

# Onboarding screens
def show_onboarding():
    st.markdown('<div class="onboarding-container">', unsafe_allow_html=True)
    
    step = st.session_state.onboarding_step
    total_steps = 7
    
    # Progress bar
    progress = (step / total_steps) * 100
    st.markdown(f"""
    <div class="progress-bar">
        <div class="progress-fill" style="width: {progress}%;"></div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown(f'<p style="text-align:center;color:#64748b;font-size:0.9rem;">Step {step + 1} of {total_steps}</p>', unsafe_allow_html=True)
    
    if step == 0:
        st.markdown('<div class="onboarding-title">🌍 Welcome to SafeWander!</div>', unsafe_allow_html=True)
        st.markdown('<div class="onboarding-subtitle">Your personalized travel safety companion</div>', unsafe_allow_html=True)
        st.markdown("---")
        name = st.text_input("**What's your name?**", placeholder="e.g., Sarah")
        if st.button("Continue →") and name:
            st.session_state.profile['name'] = name
            st.session_state.onboarding_step = 1
            st.rerun()
    
    elif step == 1:
        st.markdown(f'<div class="onboarding-title">Hi {st.session_state.profile.get("name")}! 👋</div>', unsafe_allow_html=True)
        st.markdown('<div class="onboarding-subtitle">Where are you from?</div>', unsafe_allow_html=True)
        home_country = st.selectbox("**Your home country**", list(COUNTRIES.keys()))
        if st.button("Continue →"):
            st.session_state.profile['home_country'] = home_country
            st.session_state.onboarding_step = 2
            st.rerun()
    
    elif step == 2:
        st.markdown('<div class="onboarding-title">🗣️ Language</div>', unsafe_allow_html=True)
        language = st.selectbox("**What language do you speak?**", LANGUAGES)
        if st.button("Continue →"):
            st.session_state.profile['language'] = language
            st.session_state.onboarding_step = 3
            st.rerun()
    
    elif step == 3:
        st.markdown('<div class="onboarding-title">📍 Destination</div>', unsafe_allow_html=True)
        dest_country = st.selectbox("**Where are you traveling?**", list(COUNTRIES.keys()))
        dest_city = st.selectbox("**Which city?**", COUNTRIES[dest_country])
        if st.button("Continue →"):
            st.session_state.profile['destination_country'] = dest_country
            st.session_state.profile['destination_city'] = dest_city
            st.session_state.onboarding_step = 4
            st.rerun()
    
    elif step == 4:
        st.markdown('<div class="onboarding-title">👤 About You</div>', unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            age = st.selectbox("**Age range**", ["18-25", "26-35", "36-50", "50+"])
        with col2:
            gender = st.selectbox("**Gender**", ["Female", "Male", "Non-binary", "Prefer not to say"])
        if st.button("Continue →"):
            st.session_state.profile['age_range'] = age
            st.session_state.profile['gender'] = gender
            st.session_state.onboarding_step = 5
            st.rerun()
    
    elif step == 5:
        st.markdown('<div class="onboarding-title">✨ Your Interest</div>', unsafe_allow_html=True)
        st.markdown('<div class="onboarding-subtitle">What brings you to this destination?</div>', unsafe_allow_html=True)
        interest = st.radio("**Choose one**", list(INTERESTS.keys()), label_visibility="collapsed")
        if st.button("Continue →"):
            st.session_state.profile['interest'] = INTERESTS[interest]
            st.session_state.onboarding_step = 6
            st.rerun()
    
    elif step == 6:
        st.markdown('<div class="onboarding-title">🎉 All Set!</div>', unsafe_allow_html=True)
        st.markdown(f"""
        <div class="onboarding-subtitle">
        Great! We'll personalize your experience for<br/>
        <strong>{st.session_state.profile.get('name')}</strong> exploring 
        <strong>{st.session_state.profile.get('destination_city')}</strong>!
        </div>
        """, unsafe_allow_html=True)
        
        if st.button("Start Exploring →"):
            st.session_state.profile_complete = True
            st.rerun()
    
    st.markdown('</div>', unsafe_allow_html=True)

# Main dashboard
def show_dashboard():
    data = load_safety_data()
    groq_client = init_groq()
    profile = st.session_state.profile
    
    # Welcome banner
    st.markdown(f"""
    <div class="welcome-banner">
        <div class="welcome-greeting">Welcome back, {profile.get('name')}! 👋</div>
        <div class="welcome-subtitle">
        You're exploring {profile.get('interest', 'traveling')} in 
        {profile.get('destination_city')}, {profile.get('destination_country')}
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown("### 👤 Your Profile")
        st.markdown(f"**From:** {profile.get('home_country')}")
        st.markdown(f"**Visiting:** {profile.get('destination_city')}")
        st.markdown(f"**Interest:** {profile.get('interest').title()}")
        
        st.markdown("---")
        st.markdown("### 🚨 Emergency")
        emergency = data.get("emergency_numbers", {}).get(profile.get('destination_country'), {})
        for service, number in emergency.items():
            st.markdown(f"**{service.title()}:** `{number}`")
        
        st.markdown("---")
        if st.button("🔄 Edit Profile", use_container_width=True):
            st.session_state.profile_complete = False
            st.session_state.onboarding_step = 0
            st.rerun()
    
    # Priority alerts
    priorities = get_personalized_priorities(profile, data)
    if priorities:
        st.markdown('<div class="priority-alert">', unsafe_allow_html=True)
        st.markdown('<div class="priority-title"><i class="fas fa-exclamation-triangle"></i> High Priority For You</div>', unsafe_allow_html=True)
        for priority in priorities:
            st.markdown(f'<div class="priority-item">{priority}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Personalized recommendations
    recs = get_personalized_recommendations(profile, data)
    st.markdown('<div class="recommendation-card">', unsafe_allow_html=True)
    st.markdown('<div class="rec-title"><i class="fas fa-lightbulb"></i> Personalized For You</div>', unsafe_allow_html=True)
    for rec in recs:
        st.markdown(f'<div class="rec-item">{rec}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Cultural bridge
    cultural = get_cultural_bridge(profile, data)
    st.markdown('<div class="cultural-bridge">', unsafe_allow_html=True)
    st.markdown(f'<div class="cultural-title">🌍 Cultural Tips: {profile.get("home_country")} → {profile.get("destination_country")}</div>', unsafe_allow_html=True)
    for tip in cultural:
        st.markdown(f'<div class="cultural-tip">{tip}</div>', unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Priority phrases
    phrases = get_priority_phrases(profile)
    if phrases:
        st.markdown(f'<div class="phrase-highlight">', unsafe_allow_html=True)
        st.markdown(f'<div class="phrase-need">💬 Essential for {profile.get("interest", "travel").title()}</div>', unsafe_allow_html=True)
        for need, local, meaning in phrases:
            st.markdown(f'<div class="phrase-text">"{local}" = {meaning}</div>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
    
    # AI Advisor
    st.markdown("---")
    st.markdown("### 🤖 Ask Your Personalized AI Safety Advisor")
    
    question = st.text_area(
        "Question",
        placeholder=f"e.g., Is it safe for a {profile.get('age_range', '')} {profile.get('gender', '')} to explore street food at night in {profile.get('destination_city')}?",
        height=100,
        label_visibility="collapsed"
    )
    
    if st.button("🔍 Get Personalized Advice"):
        if question.strip():
            with st.spinner("Analyzing based on your profile..."):
                raw = get_ai_response(question, profile, groq_client, data)
                parsed = parse_response(raw)
                st.session_state.conversation_history.append({"q": question, "r": parsed})
    
    # Display response
    if st.session_state.conversation_history:
        latest = st.session_state.conversation_history[-1]
        r = latest["r"]
        
        st.markdown('<div class="question-card">', unsafe_allow_html=True)
        
        badge_class = f"threat-{r['threat'].lower()}"
        icon = "fa-exclamation-triangle" if r['threat'] == "HIGH" else ("fa-exclamation-circle" if r['threat'] == "MEDIUM" else "fa-check-circle")
        
        st.markdown(f'<div class="{badge_class} threat-badge"><i class="fas {icon}"></i> {r["threat"]} THREAT</div>', unsafe_allow_html=True)
        
        st.markdown(f'<p style="color:#334155;line-height:1.7;"><strong>For you specifically:</strong> {r["assessment"]}</p>', unsafe_allow_html=True)
        
        st.markdown('<p style="font-weight:700;margin-top:1.5rem;">Recommended Actions:</p>', unsafe_allow_html=True)
        for i, action in enumerate(r["actions"], 1):
            st.markdown(f'''
            <div class="action-item">
                <div class="action-num">{i}</div>
                <div class="action-text">{action}</div>
            </div>
            ''', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align:center;padding:1.5rem;color:#94a3b8;'>
        <p><strong>SafeWander</strong> - Your Personalized Travel Safety Companion</p>
        <p style='font-size:0.9rem;'>Protecting you based on who you are and what you love 🌍</p>
    </div>
    """, unsafe_allow_html=True)

# Main app logic
def main():
    if not st.session_state.profile_complete:
        show_onboarding()
    else:
        show_dashboard()

if __name__ == "__main__":
    main()
