"""UI components for OCR Translator."""
import streamlit as st
from PIL import Image
from components.ocr_translator import extract_text_from_image, translate_and_analyze
from utils.session_manager import get_user_profile, get_country_data
from utils.groq_client import get_groq_client


def show_ocr_translator():
    """Display the OCR translator interface."""
    
    st.title("📸 OCR Translator")
    st.markdown("Photograph signs, menus, or documents for instant translation and scam detection.")
    
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
    
    # Custom CSS
    st.markdown("""
        <style>
        .ocr-card {
            background: rgba(30, 41, 59, 0.5);
            backdrop-filter: blur(10px);
            padding: 2rem;
            border-radius: 16px;
            margin: 1rem 0;
            border: 1px solid rgba(99, 102, 241, 0.3);
        }
        .warning-banner {
            background: linear-gradient(135deg, rgba(245, 158, 11, 0.2) 0%, rgba(239, 68, 68, 0.2) 100%);
            border-left: 4px solid #F59E0B;
            padding: 1rem;
            border-radius: 8px;
            margin: 1rem 0;
        }
        .warning-high {
            background: linear-gradient(135deg, rgba(239, 68, 68, 0.3) 0%, rgba(220, 38, 38, 0.3) 100%);
            border-left: 4px solid #EF4444;
        }
        .text-box {
            background: rgba(15, 23, 42, 0.5);
            padding: 1.5rem;
            border-radius: 12px;
            font-family: 'Courier New', monospace;
            font-size: 1.1rem;
            line-height: 1.6;
            margin: 1rem 0;
        }
        .language-badge {
            display: inline-block;
            background: linear-gradient(135deg, #6366F1 0%, #EC4899 100%);
            color: white;
            padding: 0.5rem 1rem;
            border-radius: 20px;
            font-weight: 600;
            margin: 0.5rem 0;
        }
        </style>
    """, unsafe_allow_html=True)
    
    # Image upload section
    st.subheader("📷 Upload Image")
    
    col1, col2 = st.columns([3, 1])
    
    with col1:
        uploaded_file = st.file_uploader(
            "Choose an image file",
            type=['png', 'jpg', 'jpeg', 'bmp', 'tiff'],
            help="Upload a clear photo of text you want to translate"
        )
    
    with col2:
        st.markdown("<br>", unsafe_allow_html=True)
        camera_btn = st.button("📸 Camera", use_container_width=True, help="Take photo (coming soon)")
        if camera_btn:
            st.info("📸 Camera feature coming soon! Please upload an image for now.")
    
    # Image preview
    if uploaded_file is not None:
        try:
            image = Image.open(uploaded_file)
            
            st.markdown("### 🖼️ Image Preview")
            st.image(image, use_container_width=True, caption="Uploaded Image")
            
            # Extract and translate button
            if st.button("🔍 Extract & Translate Text", use_container_width=True, type="primary"):
                with st.spinner("📖 Extracting text from image..."):
                    extracted_text, detected_language = extract_text_from_image(image)
                
                if extracted_text and len(extracted_text.strip()) > 0:
                    st.success(f"✅ Text extracted successfully!")
                    
                    # Display extracted text
                    st.markdown("---")
                    st.subheader("📝 Extracted Text")
                    
                    col1, col2 = st.columns([3, 1])
                    with col1:
                        st.markdown(f'<div class="language-badge">🌐 Detected: {detected_language}</div>', unsafe_allow_html=True)
                    
                    st.markdown(f"""
                        <div class="text-box">
                            {extracted_text}
                        </div>
                    """, unsafe_allow_html=True)
                    
                    # Translate and analyze
                    target_lang = user_profile.get('native_language', 'English')
                    
                    result = translate_and_analyze(
                        extracted_text,
                        detected_language,
                        target_lang,
                        groq_client
                    )
                    
                    if result:
                        st.markdown("---")
                        st.subheader("🌍 Translation & Analysis")
                        
                        # Warning banner if suspicious
                        if result.warning_level in ['medium', 'high']:
                            warning_class = "warning-high" if result.warning_level == 'high' else "warning-banner"
                            warning_icon = "🚨" if result.warning_level == 'high' else "⚠️"
                            warning_text = "HIGH RISK - POTENTIAL SCAM DETECTED!" if result.warning_level == 'high' else "CAUTION ADVISED"
                            
                            st.markdown(f"""
                                <div class="{warning_class}">
                                    <h3>{warning_icon} {warning_text}</h3>
                                    <p>This text contains suspicious elements. Please review carefully.</p>
                                </div>
                            """, unsafe_allow_html=True)
                        
                        # Translation
                        st.markdown(f"""
                            <div class="ocr-card">
                                <h4>📖 Translation ({target_lang})</h4>
                                <p style="font-size: 1.2rem; margin-top: 1rem; line-height: 1.6;">
                                    {result.translated_text}
                                </p>
                            </div>
                        """, unsafe_allow_html=True)
                        
                        # Explanation
                        with st.expander("💡 What does this mean?", expanded=True):
                            st.markdown(result.explanation)
                        
                        # Suspicious elements
                        if result.suspicious_elements and len(result.suspicious_elements) > 0:
                            with st.expander("🔍 Suspicious Elements Detected", expanded=True):
                                for element in result.suspicious_elements:
                                    st.markdown(f"- ⚠️ {element}")
                                
                                st.markdown("**Recommendations:**")
                                st.markdown("- Verify information with official sources")
                                st.markdown("- Don't make immediate payments")
                                st.markdown("- Ask locals or hotel staff for confirmation")
                                st.markdown("- Report to authorities if confirmed scam")
                        
                        # Warning level indicator
                        warning_colors = {
                            'none': '#10B981',
                            'low': '#3B82F6',
                            'medium': '#F59E0B',
                            'high': '#EF4444'
                        }
                        warning_labels = {
                            'none': 'No Concerns',
                            'low': 'Minor Attention',
                            'medium': 'Caution Advised',
                            'high': 'High Risk'
                        }
                        
                        color = warning_colors.get(result.warning_level, '#94A3B8')
                        label = warning_labels.get(result.warning_level, 'Unknown')
                        
                        st.markdown(f"""
                            <div style="text-align: center; margin: 2rem 0;">
                                <div style="display: inline-block; background: {color}; color: white; padding: 1rem 2rem; border-radius: 12px; font-weight: bold;">
                                    Warning Level: {label.upper()}
                                </div>
                            </div>
                        """, unsafe_allow_html=True)
                
                else:
                    st.error("❌ No text detected in the image. Please try:")
                    st.markdown("- Taking a clearer photo")
                    st.markdown("- Ensuring good lighting")
                    st.markdown("- Getting closer to the text")
                    st.markdown("- Making sure text is not blurry")
        
        except Exception as e:
            st.error(f"❌ Error processing image: {str(e)}")
    
    else:
        # Instructions when no image uploaded
        st.info("📸 Upload an image to get started")
        
        st.markdown("### 💡 Tips for Best Results")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
                **📷 Photo Quality:**
                - Use good lighting
                - Keep camera steady
                - Focus on the text
                - Avoid shadows
            """)
        
        with col2:
            st.markdown("""
                **📝 Text Types:**
                - Restaurant menus
                - Street signs
                - Bills and receipts
                - Notices and warnings
            """)
        
        st.markdown("### 🎯 What We Can Detect")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("""
                **💰 Pricing Issues**
                - Overcharging
                - Hidden fees
                - Fake charges
            """)
        
        with col2:
            st.markdown("""
                **⚠️ Scam Indicators**
                - Suspicious requests
                - Fake services
                - Misleading info
            """)
        
        with col3:
            st.markdown("""
                **📋 Important Info**
                - Official notices
                - Safety warnings
                - Legal requirements
            """)
