"""UI components for Situation Analyzer."""
import streamlit as st
from components.situation_analyzer import analyze_situation
from utils.session_manager import get_user_profile, get_country_data, add_situation_to_history
from utils.groq_client import get_groq_client


def get_risk_color(risk_score: int) -> str:
    """Get color based on risk score."""
    if risk_score <= 30:
        return "#10B981"  # Green
    elif risk_score <= 60:
        return "#F59E0B"  # Amber
    else:
        return "#EF4444"  # Red


def get_risk_label(risk_score: int) -> str:
    """Get risk label based on score."""
    if risk_score <= 30:
        return "LOW RISK"
    elif risk_score <= 60:
        return "MEDIUM RISK"
    else:
        return "HIGH RISK"


def show_situation_analyzer():
    """Display the situation analyzer interface."""
    
    st.title("🚨 Situation Analyzer")
    st.markdown("Describe any situation you're experiencing, and I'll analyze it for potential risks.")
    
    # Get user data
    user_profile = get_user_profile()
    country_data = get_country_data()
    
    if not user_profile or not country_data:
        st.error("❌ Profile not found. Please complete onboarding first.")
        return
    
    # Get Groq client
    groq_client = get_groq_client()
    if not groq_client:
        return
    
    # Custom CSS for risk gauge
    st.markdown("""
        <style>
        .risk-gauge {
            text-align: center;
            padding: 2rem;
            border-radius: 16px;
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(10px);
            margin: 1rem 0;
            border: 1px solid rgba(99, 102, 241, 0.2);
        }
        .risk-score {
            font-size: 4rem;
            font-weight: bold;
            margin: 0;
            animation: countUp 1s ease-out;
        }
        .risk-label {
            font-size: 1.2rem;
            font-weight: 600;
            margin-top: 0.5rem;
            letter-spacing: 2px;
        }
        @keyframes countUp {
            from { opacity: 0; transform: scale(0.5); }
            to { opacity: 1; transform: scale(1); }
        }
        .action-card {
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(10px);
            padding: 1.5rem;
            border-radius: 12px;
            margin: 1rem 0;
            border-left: 4px solid #6366F1;
        }
        .emergency-button {
            background: linear-gradient(135deg, #EF4444 0%, #DC2626 100%);
            color: white;
            padding: 1rem 2rem;
            border-radius: 12px;
            text-align: center;
            font-weight: bold;
            font-size: 1.1rem;
            margin: 1rem 0;
            cursor: pointer;
            animation: pulse 2s infinite;
        }
        @keyframes pulse {
            0%, 100% { box-shadow: 0 0 0 0 rgba(239, 68, 68, 0.7); }
            50% { box-shadow: 0 0 0 10px rgba(239, 68, 68, 0); }
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Input section
    st.subheader("📝 Describe Your Situation")
    
    col1, col2 = st.columns([4, 1])
    
    with col1:
        situation_description = st.text_area(
            "What's happening?",
            placeholder="Example: A taxi driver is refusing to use the meter and asking for 5x the normal fare...",
            height=150,
            help="Describe the situation in detail. Include what's happening, where you are, and any concerns you have."
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        voice_input = st.button("🎤 Voice\nInput", use_container_width=True, help="Record your situation (coming soon)")
        if voice_input:
            st.info("🎤 Voice input feature coming soon! Please use text input for now.")
    
    analyze_button = st.button(
        "🔍 Analyze Situation",
        use_container_width=True,
        type="primary"
    )
    
    # Analysis section
    if analyze_button and situation_description:
        analysis = analyze_situation(
            situation_description,
            country_data,
            user_profile,
            groq_client
        )
        
        if analysis:
            # Save to history
            add_situation_to_history({
                'description': situation_description,
                'analysis': analysis
            })
            
            # Display results
            st.markdown("---")
            st.subheader("📊 Analysis Results")
            
            # Risk gauge
            risk_color = get_risk_color(analysis.risk_score)
            risk_label = get_risk_label(analysis.risk_score)
            
            st.markdown(f"""
                <div class="risk-gauge">
                    <div class="risk-score" style="color: {risk_color};">{analysis.risk_score}</div>
                    <div class="risk-label" style="color: {risk_color};">{risk_label}</div>
                </div>
            """, unsafe_allow_html=True)
            
            # Pattern matched
            st.markdown(f"### 🎯 Pattern Identified: **{analysis.pattern_matched}**")
            
            # Risk explanation
            with st.expander("📖 Why is this happening?", expanded=True):
                st.markdown(analysis.risk_explanation)
            
            # What to do
            with st.expander("✅ What You Should Do", expanded=True):
                for i, action in enumerate(analysis.what_to_do, 1):
                    st.markdown(f"**{i}.** {action}")
            
            # What NOT to do
            with st.expander("⛔ What You Should NOT Do", expanded=True):
                for i, action in enumerate(analysis.what_not_to_do, 1):
                    st.markdown(f"**{i}.** {action}")
            
            # Emergency contacts
            if analysis.emergency_numbers:
                with st.expander("🆘 Emergency Contacts", expanded=analysis.risk_score > 60):
                    cols = st.columns(2)
                    for idx, (service, number) in enumerate(analysis.emergency_numbers.items()):
                        with cols[idx % 2]:
                            st.markdown(f"""
                                <div class="action-card">
                                    <strong>{service.replace('_', ' ').title()}</strong><br>
                                    <a href="tel:{number}" style="font-size: 1.5rem; color: #6366F1; text-decoration: none;">
                                        📞 {number}
                                    </a>
                                </div>
                            """, unsafe_allow_html=True)
            
            # Local phrases
            if analysis.local_phrases:
                with st.expander("🗣️ Useful Local Phrases"):
                    for phrase_type, phrase in analysis.local_phrases.items():
                        st.markdown(f"**{phrase_type.replace('_', ' ').title()}:** {phrase}")
            
            # Cultural notes
            if analysis.cultural_notes and analysis.cultural_notes != "No specific cultural concerns identified":
                with st.expander("🌍 Cultural Context"):
                    st.markdown(analysis.cultural_notes)
            
            # High risk warning
            if analysis.risk_score > 60:
                st.markdown("""
                    <div class="emergency-button">
                        ⚠️ HIGH RISK SITUATION - TAKE IMMEDIATE ACTION
                    </div>
                """, unsafe_allow_html=True)
    
    elif analyze_button:
        st.warning("⚠️ Please describe your situation before analyzing.")
    
    # Tips section
    st.markdown("---")
    st.subheader("💡 Quick Safety Tips")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("""
            **🚕 Transportation**
            - Always use metered taxis
            - Use official ride apps
            - Agree on price beforehand
        """)
    
    with col2:
        st.markdown("""
            **👥 Interactions**
            - Trust your instincts
            - Stay in public areas
            - Keep emergency contacts handy
        """)
    
    with col3:
        st.markdown("""
            **💰 Money**
            - Avoid showing large amounts
            - Use ATMs in secure locations
            - Keep copies of important docs
        """)
