import streamlit as st
import json
import os
from groq import Groq
from datetime import datetime

# Page config
st.set_page_config(
    page_title="SafeWander - AI Travel Safety Companion",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Stunning CSS
st.markdown("""
<link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css">
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700;800&display=swap');
    
    * {
        font-family: 'Inter', sans-serif;
    }
    
    .hero-section {
        text-align: center;
        padding: 3rem 0 2rem 0;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        border-radius: 24px;
        margin-bottom: 3rem;
        color: white;
        box-shadow: 0 20px 60px rgba(102, 126, 234, 0.3);
    }
    
    .hero-title {
        font-size: 3.5rem;
        font-weight: 800;
        margin: 0;
        text-shadow: 0 2px 20px rgba(0,0,0,0.2);
    }
    
    .hero-subtitle {
        font-size: 1.3rem;
        margin-top: 1rem;
        opacity: 0.95;
        font-weight: 500;
    }
    
    .hero-tagline {
        font-size: 1rem;
        margin-top: 0.5rem;
        opacity: 0.85;
    }
    
    /* Stats Bar */
    .stats-bar {
        display: flex;
        justify-content: space-around;
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 2rem 0;
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
    }
    
    .stat-item {
        text-align: center;
    }
    
    .stat-number {
        font-size: 2.5rem;
        font-weight: 800;
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }
    
    .stat-label {
        color: #64748b;
        font-size: 0.95rem;
        margin-top: 0.5rem;
        font-weight: 600;
    }
    
    /* Question Input */
    .question-container {
        background: linear-gradient(135deg, #f8fafc 0%, #e2e8f0 100%);
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border: 2px solid #e2e8f0;
    }
    
    .input-label {
        font-size: 1.2rem;
        font-weight: 700;
        color: #1e293b;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    /* Threat Badges */
    .threat-badge {
        display: inline-flex;
        align-items: center;
        gap: 0.5rem;
        padding: 0.8rem 2rem;
        border-radius: 50px;
        font-weight: 800;
        font-size: 1.2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.15);
        animation: pulse 2s ease-in-out infinite;
    }
    
    @keyframes pulse {
        0%, 100% { transform: scale(1); }
        50% { transform: scale(1.03); }
    }
    
    .threat-high {
        background: linear-gradient(135deg, #ef4444 0%, #dc2626 100%);
        color: white;
    }
    
    .threat-medium {
        background: linear-gradient(135deg, #f59e0b 0%, #d97706 100%);
        color: white;
    }
    
    .threat-low {
        background: linear-gradient(135deg, #10b981 0%, #059669 100%);
        color: white;
    }
    
    /* Response Cards */
    .response-section {
        background: white;
        border-radius: 20px;
        padding: 2.5rem;
        margin: 2rem 0;
        box-shadow: 0 10px 40px rgba(0,0,0,0.1);
        border-left: 6px solid #667eea;
    }
    
    .answer-box {
        background: linear-gradient(135deg, #eff6ff 0%, #dbeafe 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 5px solid #3b82f6;
    }
    
    .answer-box h4 {
        color: #1e40af;
        font-size: 1.3rem;
        margin: 0 0 1rem 0;
        font-weight: 700;
    }
    
    .answer-text {
        color: #1e40af;
        font-size: 1.15rem;
        line-height: 1.8;
        font-weight: 500;
    }
    
    .action-box {
        background: #f8fafc;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
    }
    
    .action-box h4 {
        color: #1e293b;
        font-size: 1.3rem;
        margin: 0 0 1.5rem 0;
        font-weight: 700;
    }
    
    .action-item {
        background: white;
        padding: 1.2rem 1.5rem;
        margin: 1rem 0;
        border-radius: 12px;
        border-left: 4px solid #667eea;
        display: flex;
        align-items: flex-start;
        gap: 1rem;
        box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        transition: all 0.3s ease;
    }
    
    .action-item:hover {
        transform: translateX(5px);
        box-shadow: 0 4px 12px rgba(0,0,0,0.1);
    }
    
    .action-number {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 800;
        width: 32px;
        height: 32px;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
    }
    
    .action-text {
        color: #334155;
        font-size: 1.1rem;
        line-height: 1.6;
        font-weight: 500;
    }
    
    .cultural-box {
        background: linear-gradient(135deg, #fef3c7 0%, #fde68a 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 5px solid #f59e0b;
    }
    
    .cultural-box h4 {
        color: #92400e;
        font-size: 1.3rem;
        margin: 0 0 1rem 0;
        font-weight: 700;
    }
    
    .cultural-text {
        color: #78350f;
        font-size: 1.1rem;
        line-height: 1.8;
        font-weight: 500;
    }
    
    .emergency-box-main {
        background: linear-gradient(135deg, #fee2e2 0%, #fecaca 100%);
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        border-left: 5px solid #dc2626;
    }
    
    .emergency-box-main h4 {
        color: #991b1b;
        font-size: 1.4rem;
        margin: 0 0 1rem 0;
        font-weight: 800;
    }
    
    .emergency-number {
        background: white;
        padding: 1rem 1.5rem;
        border-radius: 12px;
        margin: 0.8rem 0;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 2px 8px rgba(0,0,0,0.1);
    }
    
    .emergency-label {
        color: #7f1d1d;
        font-weight: 700;
        font-size: 1.05rem;
    }
    
    .emergency-num {
        color: #dc2626;
        font-weight: 800;
        font-size: 1.5rem;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: linear-gradient(180deg, #1e293b 0%, #0f172a 100%);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    .sidebar-section {
        background: rgba(255,255,255,0.1);
        padding: 1.2rem;
        border-radius: 12px;
        margin: 1rem 0;
        backdrop-filter: blur(10px);
        border: 1px solid rgba(255,255,255,0.2);
    }
    
    .sidebar-title {
        font-size: 1.1rem;
        font-weight: 700;
        margin-bottom: 1rem;
        display: flex;
        align-items: center;
        gap: 0.5rem;
    }
    
    .example-item {
        background: rgba(255,255,255,0.05);
        padding: 0.8rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        font-size: 0.95rem;
        cursor: pointer;
        transition: all 0.2s ease;
        border-left: 3px solid transparent;
    }
    
    .example-item:hover {
        background: rgba(255,255,255,0.15);
        border-left-color: #667eea;
        transform: translateX(5px);
    }
    
    /* Button Styles */
    .stButton>button {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        color: white;
        font-weight: 700;
        border: none;
        padding: 1rem 3rem;
        border-radius: 50px;
        font-size: 1.2rem;
        transition: all 0.3s ease;
        box-shadow: 0 4px 15px rgba(102, 126, 234, 0.4);
        text-transform: uppercase;
        letter-spacing: 1px;
    }
    
    .stButton>button:hover {
        transform: translateY(-3px);
        box-shadow: 0 8px 25px rgba(102, 126, 234, 0.5);
    }
    
    /* Conversation History */
    .history-item {
        background: white;
        border-radius: 16px;
        padding: 2rem;
        margin: 1.5rem 0;
        box-shadow: 0 4px 15px rgba(0,0,0,0.08);
        border-left: 5px solid #e2e8f0;
        transition: all 0.3s ease;
    }
    
    .history-item:hover {
        box-shadow: 0 8px 30px rgba(0,0,0,0.12);
        transform: translateY(-2px);
    }
    
    .history-question {
        color: #64748b;
        font-size: 1rem;
        font-weight: 600;
        margin-bottom: 1rem;
        font-style: italic;
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    .stDeployButton {display: none;}
    
    /* Animations */
    @keyframes fadeIn {
        from {
            opacity: 0;
            transform: translateY(20px);
        }
        to {
            opacity: 1;
            transform: translateY(0);
        }
    }
    
    .response-section {
        animation: fadeIn 0.6s ease-out;
    }
</style>
""", unsafe_allow_html=True)

# Session state
if 'conversation_history' not in st.session_state:
    st.session_state.conversation_history = []
if 'current_country' not in st.session_state:
    st.session_state.current_country = "India"

# Load data
@st.cache_data
def load_safety_data():
    if os.path.exists("dataset.json"):
        with open("dataset.json", "r") as f:
            return json.load(f)
    return {"countries": ["India", "Thailand", "Mexico", "USA", "Brazil"]}

# Initialize Groq
def init_groq():
    try:
        api_key = st.secrets.get("GROQ_API_KEY", os.getenv("GROQ_API_KEY"))
        if api_key:
            return Groq(api_key=api_key)
    except:
        pass
    return None

# RAG Search
def get_context(query, country, data):
    """Get relevant safety context for the query"""
    query_lower = query.lower()
    context = []
    
    # Transport scams
    for scam in data.get("transport_scams", []):
        if scam.get("country") == country:
            if any(word in query_lower for word in ["taxi", "driver", "uber", "auto", "transport", "fare", "price", "₹", "rupees", "km"]):
                context.append(f"Transport: Normal {scam.get('normal_rate')}, Scam {scam.get('scam_rate')}. {scam.get('safety_advice')}")
    
    # Harassment
    for safety in data.get("harassment_safety", []):
        if any(word in query_lower for word in ["follow", "stalk", "harass", "touch", "danger", "scared", "afraid"]):
            context.append(f"Safety: {safety.get('situation')} - Threat: {safety.get('threat_level')}. Actions: {', '.join(safety.get('immediate_actions', [])[:3])}")
    
    # Emergency numbers
    emergency = data.get("emergency_numbers", {}).get(country, {})
    if emergency:
        context.append(f"Emergency: {emergency}")
    
    # Cultural info
    for culture in data.get("cultural_guidelines", []):
        if culture.get("country") == country:
            context.append(f"Culture: {culture.get('dress')}. Etiquette: {culture.get('etiquette')}")
    
    # Price reference
    prices = data.get("price_reference", {}).get(country, {})
    if prices:
        context.append(f"Typical prices: {prices}")
    
    return "\n".join(context[:5])

# AI Response
def get_ai_response(query, country, groq_client, data):
    """Get comprehensive AI safety advice"""
    
    context = get_context(query, country, data)
    
    system_prompt = f"""You are SafeWander AI, an expert travel safety advisor for {country}.

Analyze the traveler's situation and respond in this EXACT structure:

1. THREAT LEVEL: Determine if this is HIGH, MEDIUM, or LOW threat
2. QUICK ASSESSMENT: 2-3 sentences explaining the situation clearly
3. IMMEDIATE ACTIONS: 3-4 specific, actionable steps they should take NOW
4. CULTURAL CONTEXT: Brief relevant cultural insight that helps them understand the situation better
5. EMERGENCY CONTACTS: Relevant emergency numbers

Be direct, clear, and prioritize traveler safety. Use the context data provided."""

    user_prompt = f"""Situation in {country}: {query}

Available Context:
{context}

Provide comprehensive safety advice."""

    try:
        if groq_client:
            response = groq_client.chat.completions.create(
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_prompt}
                ],
                model="llama-3.3-70b-versatile",
                temperature=0.6,
                max_tokens=600
            )
            return response.choices[0].message.content
        else:
            return f"Unable to analyze. Please set GROQ_API_KEY. Context: {context}"
    except Exception as e:
        return f"Error: {str(e)}"

# Parse response into structured format
def parse_response(response_text):
    """Parse AI response into structured components"""
    
    # Detect threat level
    threat = "MEDIUM"
    if "HIGH" in response_text.upper() or "DANGER" in response_text.upper() or "URGENT" in response_text.upper():
        threat = "HIGH"
    elif "LOW" in response_text.upper() or "SAFE" in response_text.upper() or "MINOR" in response_text.upper():
        threat = "LOW"
    
    # Split into sections (simple parsing)
    lines = response_text.split('\n')
    
    assessment = []
    actions = []
    cultural = []
    emergency = []
    
    current_section = "assessment"
    
    for line in lines:
        line = line.strip()
        if not line:
            continue
            
        line_lower = line.lower()
        
        # Detect section changes
        if any(word in line_lower for word in ["action", "step", "do", "should"]):
            current_section = "actions"
        elif any(word in line_lower for word in ["culture", "custom", "etiquette", "local"]):
            current_section = "cultural"
        elif any(word in line_lower for word in ["emergency", "contact", "police", "ambulance"]):
            current_section = "emergency"
        
        # Add to appropriate section
        if current_section == "assessment" and len(assessment) < 5:
            assessment.append(line)
        elif current_section == "actions":
            # Clean up action items
            clean_line = line.lstrip('0123456789.-*• ').strip()
            if clean_line and len(actions) < 4:
                actions.append(clean_line)
        elif current_section == "cultural" and len(cultural) < 3:
            cultural.append(line)
        elif current_section == "emergency" and len(emergency) < 3:
            emergency.append(line)
    
    return {
        "threat": threat,
        "assessment": ' '.join(assessment[:3]) if assessment else "Analyzing your situation...",
        "actions": actions[:4] if actions else ["Stay calm", "Assess the situation", "Seek help if needed"],
        "cultural": ' '.join(cultural[:2]) if cultural else "Be respectful of local customs.",
        "emergency": emergency[:2] if emergency else []
    }

# Main app
def main():
    safety_data = load_safety_data()
    groq_client = init_groq()
    
    # Hero Section
    st.markdown(f"""
    <div class="hero-section">
        <div class="hero-title"><i class="fas fa-shield-alt"></i> SafeWander</div>
        <div class="hero-subtitle">Your AI-Powered Travel Safety Companion</div>
        <div class="hero-tagline">Preventing scams, harassment, and danger worldwide</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Stats Bar
    st.markdown("""
    <div class="stats-bar">
        <div class="stat-item">
            <div class="stat-number">5</div>
            <div class="stat-label">Countries Covered</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">100+</div>
            <div class="stat-label">Scam Types Detected</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">24/7</div>
            <div class="stat-label">AI Protection</div>
        </div>
        <div class="stat-item">
            <div class="stat-number">Instant</div>
            <div class="stat-label">Safety Advice</div>
        </div>
    </div>
    """, unsafe_allow_html=True)
    
    # Sidebar
    with st.sidebar:
        st.markdown('<div class="sidebar-title"><i class="fas fa-globe"></i> Select Country</div>', unsafe_allow_html=True)
        
        country = st.selectbox(
            "Your Current Location",
            ["India", "Thailand", "Mexico", "USA", "Brazil"],
            index=0,
            label_visibility="collapsed"
        )
        st.session_state.current_country = country
        
        st.markdown("---")
        
        st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
        st.markdown('<div class="sidebar-title"><i class="fas fa-lightbulb"></i> Try asking...</div>', unsafe_allow_html=True)
        
        examples = [
            "Driver wants ₹800 for 5km, fair?",
            "Someone following me, what to do?",
            "Restaurant bill seems high",
            "Is this area safe at night?",
            "Vendor aggressive, help!"
        ]
        
        for example in examples:
            st.markdown(f'<div class="example-item">"{example}"</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        # Emergency numbers
        emergency_nums = safety_data.get("emergency_numbers", {}).get(country, {})
        if emergency_nums:
            st.markdown('<div class="sidebar-section">', unsafe_allow_html=True)
            st.markdown('<div class="sidebar-title"><i class="fas fa-phone-alt"></i> Emergency Numbers</div>', unsafe_allow_html=True)
            for service, number in emergency_nums.items():
                st.markdown(f"**{service.title()}:** `{number}`")
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown("---")
        
        if st.session_state.conversation_history:
            if st.button("🗑️ Clear History", use_container_width=True):
                st.session_state.conversation_history = []
                st.rerun()
    
    # Main Question Input
    st.markdown('<div class="question-container">', unsafe_allow_html=True)
    st.markdown('<div class="input-label"><i class="fas fa-question-circle"></i> Describe Your Situation</div>', unsafe_allow_html=True)
    
    user_question = st.text_area(
        "What's happening?",
        placeholder=f"Example: Taxi driver in {country} quoted ₹500 for a 3km ride. The meter shows ₹150. Is this a scam?",
        height=120,
        label_visibility="collapsed"
    )
    
    col1, col2, col3 = st.columns([2, 1, 2])
    with col2:
        analyze_button = st.button("🔍 Analyze Safety", use_container_width=True, type="primary")
    
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Process query
    if analyze_button and user_question.strip():
        with st.spinner("🤖 Analyzing situation with AI..."):
            raw_response = get_ai_response(user_question, country, groq_client, safety_data)
            parsed = parse_response(raw_response)
            
            # Save to history
            st.session_state.conversation_history.append({
                "question": user_question,
                "response": parsed,
                "country": country,
                "time": datetime.now().strftime("%I:%M %p")
            })
    
    # Display latest response
    if st.session_state.conversation_history:
        latest = st.session_state.conversation_history[-1]
        parsed = latest["response"]
        
        st.markdown('<div class="response-section">', unsafe_allow_html=True)
        
        # Threat Level Badge
        threat_class = f"threat-{parsed['threat'].lower()}"
        icon = "fa-exclamation-triangle" if parsed['threat'] == "HIGH" else ("fa-exclamation-circle" if parsed['threat'] == "MEDIUM" else "fa-check-circle")
        
        st.markdown(f"""
        <div class="{threat_class} threat-badge">
            <i class="fas {icon}"></i> THREAT LEVEL: {parsed['threat']}
        </div>
        """, unsafe_allow_html=True)
        
        # Quick Assessment
        st.markdown(f"""
        <div class="answer-box">
            <h4><i class="fas fa-brain"></i> Quick Assessment</h4>
            <div class="answer-text">{parsed['assessment']}</div>
        </div>
        """, unsafe_allow_html=True)
        
        # Immediate Actions
        st.markdown('<div class="action-box">', unsafe_allow_html=True)
        st.markdown('<h4><i class="fas fa-list-check"></i> What To Do Right Now</h4>', unsafe_allow_html=True)
        
        for i, action in enumerate(parsed['actions'], 1):
            st.markdown(f"""
            <div class="action-item">
                <div class="action-number">{i}</div>
                <div class="action-text">{action}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Cultural Context
        if parsed['cultural']:
            st.markdown(f"""
            <div class="cultural-box">
                <h4><i class="fas fa-globe-asia"></i> Cultural Context</h4>
                <div class="cultural-text">{parsed['cultural']}</div>
            </div>
            """, unsafe_allow_html=True)
        
        # Emergency Contacts
        if parsed['emergency'] or emergency_nums:
            st.markdown('<div class="emergency-box-main">', unsafe_allow_html=True)
            st.markdown('<h4><i class="fas fa-phone-volume"></i> Emergency Contacts</h4>', unsafe_allow_html=True)
            
            for service, number in emergency_nums.items():
                st.markdown(f"""
                <div class="emergency-number">
                    <span class="emergency-label">{service.title()}</span>
                    <span class="emergency-num">{number}</span>
                </div>
                """, unsafe_allow_html=True)
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Conversation History
    if len(st.session_state.conversation_history) > 1:
        st.markdown("---")
        st.markdown("### 💬 Previous Conversations")
        
        for chat in reversed(st.session_state.conversation_history[:-1][-3:]):
            st.markdown(f"""
            <div class="history-item">
                <div class="history-question">
                    <i class="fas fa-map-marker-alt"></i> {chat['country']} | 
                    <i class="fas fa-clock"></i> {chat['time']} | 
                    "{chat['question'][:100]}..."
                </div>
                <div class="threat-{chat['response']['threat'].lower()} threat-badge">
                    {chat['response']['threat']}
                </div>
            </div>
            """, unsafe_allow_html=True)
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; padding: 2rem; color: #94a3b8;'>
        <p style='font-size: 1.1rem;'><strong>SafeWander</strong> - VisaVerse AI Hackathon 2024</p>
        <p>Protecting travelers worldwide with AI-powered safety intelligence 🌍</p>
        <p style='font-size: 0.9rem; margin-top: 1rem;'>
            <i class="fas fa-shield-alt"></i> Real-time threat detection | 
            <i class="fas fa-database"></i> 100+ scam database | 
            <i class="fas fa-brain"></i> AI-powered analysis
        </p>
    </div>
    """, unsafe_allow_html=True)

if __name__ == "__main__":
    main()
