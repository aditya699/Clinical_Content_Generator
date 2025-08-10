import os
from dotenv import load_dotenv
import streamlit as st
from serpapi import GoogleSearch
import pandas as pd
from openai import OpenAI
import time

# Load API keys from .env
load_dotenv()
SERPAPI_KEY = os.getenv("SERPAPI_API_KEY")
OPENAI_KEY = os.getenv("OPENAI_API_KEY")

# Initialize OpenAI client
if OPENAI_KEY:
    client = OpenAI(api_key=OPENAI_KEY)
else:
    client = OpenAI()  # Uses default API key from environment

# Streamlit page config
st.set_page_config(
    page_title="HealthClinic Content Generator",
    page_icon="🏥",
    layout="centered"
)

# Custom CSS for clean, medical-themed UI
st.markdown("""
<style>
    /* Import Google Fonts */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;600;700&display=swap');
    
    /* Hide Streamlit default elements */
    .stDeployButton {display: none;}
    header[data-testid="stHeader"] {display: none;}
    .stMainBlockContainer {padding-top: 1rem;}
    
    /* Main app styling */
    .stApp {
        font-family: 'Inter', sans-serif;
        background: #f8fffe;
    }
    
    /* Header styling */
    .custom-header {
        text-align: center;
        margin-bottom: 2rem;
        padding: 2.5rem 1rem;
        background: linear-gradient(135deg, #2196F3, #21CBF3);
        border-radius: 16px;
        color: white;
        box-shadow: 0 4px 20px rgba(33, 150, 243, 0.3);
    }
    
    .custom-header h1 {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    
    .custom-header p {
        font-size: 1.1rem;
        opacity: 0.9;
        margin-bottom: 0;
    }
    
    .header-subtitle {
        font-size: 0.95rem;
        opacity: 0.8;
        margin-top: 0.5rem;
    }
    
    /* Button styling */
    .stButton > button {
        background: linear-gradient(135deg, #4CAF50, #45a049);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-1px);
        box-shadow: 0 4px 12px rgba(76, 175, 80, 0.4);
    }
    
    /* Input styling */
    .stTextInput > div > div > input {
        border-radius: 12px;
        border: 2px solid #e1f5fe;
        padding: 0.75rem 1rem;
        font-size: 1rem;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #2196F3;
        box-shadow: 0 0 0 3px rgba(33, 150, 243, 0.1);
    }
    
    /* Success/Error messages */
    .stAlert {
        border-radius: 12px;
        margin: 1rem 0;
    }
    
    /* Download button */
    .stDownloadButton > button {
        background: linear-gradient(135deg, #FF9800, #F57C00);
        color: white;
        border: none;
        border-radius: 12px;
        padding: 0.75rem 2rem;
        font-weight: 600;
        font-size: 1rem;
        width: 100%;
    }
    
    /* DataFrame styling */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        margin: 1rem 0;
        border: 1px solid #e1f5fe;
    }
    
    /* Stats styling */
    .stats-container {
        background: linear-gradient(135deg, #E8F5E8, #F1F8E9);
        border-radius: 12px;
        padding: 1rem;
        margin: 1rem 0;
        text-align: center;
        border: 1px solid #C8E6C9;
    }
    
    .stat-number {
        font-size: 1.5rem;
        font-weight: 700;
        color: #4CAF50;
    }
    
    /* Health-focused feature cards */
    .feature-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        margin: 0.5rem 0;
        box-shadow: 0 2px 8px rgba(0, 0, 0, 0.05);
        border-left: 4px solid #2196F3;
    }
    
    .feature-title {
        font-weight: 600;
        color: #1976D2;
        margin-bottom: 0.5rem;
    }
    
    .feature-desc {
        color: #666;
        font-size: 0.9rem;
        line-height: 1.5;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'generated_content' not in st.session_state:
    st.session_state.generated_content = None
if 'search_terms' not in st.session_state:
    st.session_state.search_terms = []
if 'topic_used' not in st.session_state:
    st.session_state.topic_used = ""

# Header
st.markdown("""
<div class="custom-header">
    <h1>🏥 HealthClinic Content Generator</h1>
    <p>Transform health trends into engaging patient education content</p>
    <div class="header-subtitle">Powered by real-time health search data from India</div>
</div>
""", unsafe_allow_html=True)

# Check API keys
st.subheader("🔑 System Status")
col1, col2 = st.columns(2)
with col1:
    if SERPAPI_KEY:
        st.success("✅ Search Engine Connected")
    else:
        st.error("❌ Search API Required")

with col2:
    if OPENAI_KEY:
        st.success("✅ AI Content Generator Ready")  
    else:
        st.error("❌ AI API Required")

# About section for health clinics
st.subheader("💡 How This Helps Your Clinic")

col1, col2 = st.columns(2)
with col1:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📊 Patient-Focused Content</div>
        <div class="feature-desc">Create content based on what patients are actually searching for online</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🎯 Local Health Trends</div>
        <div class="feature-desc">Target health concerns specific to your community and region</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">📱 Social Media Ready</div>
        <div class="feature-desc">Generate posts for Instagram, Facebook, and other platforms</div>
    </div>
    """, unsafe_allow_html=True)
    
    st.markdown("""
    <div class="feature-card">
        <div class="feature-title">🔬 Evidence-Based</div>
        <div class="feature-desc">Content suggestions grounded in real patient search behavior</div>
    </div>
    """, unsafe_allow_html=True)

# Input section
st.subheader("📝 Choose Your Health Topic")
health_topic = st.text_input(
    "Health topic or medical specialty",
    placeholder="e.g., diabetes management, mental health, women's health, pediatric care",
    help="Enter any health topic relevant to your clinic's specialization"
)

# Health-specific examples
with st.expander("🏥 Popular health topics for clinics"):
    st.markdown("""
    **General Medicine:** diabetes, hypertension, heart health, weight management, preventive care
    
    **Women's Health:** pregnancy care, menstrual health, PCOS, menopause, breast health
    
    **Mental Health:** anxiety, depression, stress management, sleep disorders, mindfulness
    
    **Pediatrics:** child nutrition, vaccination, growth development, common infections
    
    **Specialties:** dermatology, orthopedics, eye care, dental health, senior care
    """)

# Settings
st.subheader("⚙️ Content Settings")
col1, col2, col3 = st.columns(3)
with col1:
    content_count = st.selectbox("Number of ideas", [8, 12, 15, 20], index=1)
with col2:
    content_type = st.selectbox("Content format", ["Social Media Posts", "Patient Education", "Health Tips", "FAQ Answers"])
with col3:
    audience = st.selectbox("Target audience", ["General Patients", "Young Adults", "Parents", "Seniors"])

# Generate button - only trigger on button click
if st.button("🚀 Generate Health Content Ideas", type="primary"):
    # Validate inputs
    if not SERPAPI_KEY or not OPENAI_KEY:
        st.error("🔑 Please configure your API keys in the .env file")
        st.stop()
    
    if not health_topic.strip():
        st.warning("⚠️ Please enter a health topic")
        st.stop()
    
    # Clear previous results when generating new ones
    st.session_state.generated_content = None
    st.session_state.search_terms = []
    st.session_state.topic_used = health_topic.strip()
    
    # Step 1: Fetch search terms
    suggestions_list = []  # Initialize here
    with st.status("🔍 Analyzing health search trends in India...", expanded=True) as status:
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            # Single search query
            status_text.text(f"Searching health trends for: {health_topic.strip()}...")
            
            params = {
                "engine": "google_autocomplete",
                "q": health_topic.strip(),
                "hl": "en",
                "gl": "in",  # India only
                "api_key": SERPAPI_KEY
            }
            
            search = GoogleSearch(params)
            results = search.get_dict()
            
            for suggestion in results.get("suggestions", []):
                suggestions_list.append(suggestion["value"])
            
            progress_bar.progress(1.0)
            
            # Clean up and deduplicate
            suggestions_list = sorted(set(suggestions_list))
            st.session_state.search_terms = suggestions_list
            
            progress_bar.empty()
            status_text.empty()
            
            if not suggestions_list:
                st.warning("🔍 No health trends found for this topic. Try a different keyword.")
                st.stop()
            
            status.update(label=f"✅ Found {len(suggestions_list)} health search trends", state="complete")
        
        except Exception as e:
            status.update(label=f"❌ Error: {str(e)}", state="error")
            st.stop()
    
    # Step 2: Generate content
    with st.status("🤖 Creating patient-focused content ideas...", expanded=True) as status:
        prompt = f"""
        You are a healthcare content strategist working for a medical clinic in India.
        
        Based on these real health search trends from Google India, create {content_count} engaging content ideas.
        
        Content Requirements:
        - Format: {content_type}
        - Target Audience: {audience}
        - Medical Topic: {health_topic}
        - Location: India (consider local health concerns)
        - Tone: Professional yet approachable, patient-friendly
        
        Guidelines:
        - Keep content ideas under 100 characters for social media compatibility
        - Focus on patient education and health awareness
        - Make content engaging but medically responsible
        - Avoid giving specific medical advice
        - Include actionable health tips where appropriate
        - Consider Indian healthcare context and common concerns
        
        Health search trends from patients: {st.session_state.search_terms}
        
        Create exactly {content_count} content ideas formatted as clear, engaging titles or questions that would help patients learn about {health_topic}.
        """
        
        try:
            response = client.responses.create(
                model="gpt-4.1-mini",
                input=prompt
            )
            
            content_text = response.output_text.strip()
            content_ideas = [line.strip() for line in content_text.split('\n') if line.strip()]
            
            # Clean up content ideas (remove numbering)
            import re
            cleaned_content = []
            for idea in content_ideas:
                clean_idea = re.sub(r'^\d+\.\s*', '', idea.strip())
                clean_idea = re.sub(r'^[-•]\s*', '', clean_idea)
                if clean_idea:
                    cleaned_content.append(clean_idea)
            
            st.session_state.generated_content = cleaned_content[:content_count]
            status.update(label=f"🎉 Generated {len(st.session_state.generated_content)} content ideas!", state="complete")
            
        except Exception as e:
            status.update(label=f"❌ Error generating content: {str(e)}", state="error")
            st.stop()

# Display results if they exist
if st.session_state.generated_content:
    st.success(f"🎉 Generated {len(st.session_state.generated_content)} content ideas for your clinic!")
    
    # Stats
    st.markdown(f"""
    <div class="stats-container">
        <div class="stat-number">{len(st.session_state.search_terms)}</div>
        <div>Patient search trends analyzed</div>
    </div>
    """, unsafe_allow_html=True)
    
    # Show search terms used
    with st.expander(f"📊 View {len(st.session_state.search_terms)} health search trends from Indian patients"):
        for i, term in enumerate(st.session_state.search_terms, 1):
            st.write(f"{i}. {term}")
    
    # Display content ideas
    df = pd.DataFrame(st.session_state.generated_content, columns=["Health Content Idea"])
    df.index = range(1, len(df) + 1)
    
    st.subheader("📋 Your Health Content Ideas")
    st.dataframe(df, use_container_width=True, height=400)
    
    # Download
    csv = df.to_csv(index=True).encode("utf-8")
    filename = f"{st.session_state.topic_used.replace(' ', '_')}_health_content_ideas.csv"
    
    st.download_button(
        label="📥 Download Content Ideas",
        data=csv,
        file_name=filename,
        mime="text/csv"
    )
    
    # Usage tips for health clinics
    with st.expander("💡 How to use these content ideas"):
        st.markdown("""
        **📱 Social Media Strategy:**
        - Use ideas as Instagram post captions or Facebook updates
        - Create carousel posts breaking down complex health topics
        - Share as stories with engaging visuals
        
        **🏥 Patient Education:**
        - Turn ideas into blog posts for your clinic website
        - Create educational handouts for waiting rooms
        - Use as topics for patient education videos
        
        **📧 Patient Communication:**
        - Include in clinic newsletters
        - Send as health tips via SMS or WhatsApp
        - Use for patient follow-up communications
        
        **⚠️ Medical Disclaimer:**
        - Always add appropriate medical disclaimers
        - Encourage patients to consult healthcare providers
        - Review content with medical professionals before publishing
        """)

# Footer
st.markdown("---")
st.markdown("*Empowering healthcare providers with data-driven content strategies 🏥*")
st.markdown("*Always consult with medical professionals before publishing health content*")