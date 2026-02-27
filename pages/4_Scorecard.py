import streamlit as st
import joblib
from core.auth import logout_user
from utils.engine import get_gemini_response


from core.auth import logout_user



# Security check
if not st.session_state.get("authenticated", False):
    st.switch_page("app.py")

# 2. Unified Navigation Menu (Now with 5 links)
with st.sidebar:
    st.title("Career AI Hub")
    st.page_link("pages/1_Dashboard.py", label="Dashboard", icon="🏠")
    st.page_link("pages/2_Branding.py", label="LinkedIn Optimizer", icon="✨")
    st.page_link("pages/3_Skill_Gap.py", label="Skill Gap Analyzer", icon="📊")
    st.page_link("pages/4_Scorecard.py", label="Viral Scorecard", icon="🔥")
    st.page_link("pages/5_Network.py", label="Connection Hub", icon="🤝")
    st.divider()
    st.button("Logout", on_click=logout_user, use_container_width=True)

st.title("Viral Score & MNC-Readiness Analysis")
st.write("Harness AI to optimize your technical content for maximum engagement.")

# Load the model we just trained
@st.cache_resource
def load_engagement_model():
    try:
        return joblib.load('ml_models/engagement_model.pkl')
    except:
        return None

rf_model = load_engagement_model()

# UI Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Your Post")
    user_post = st.text_area("Draft your message...", height=200, placeholder="Paste your LinkedIn draft here...")
    analyze_btn = st.button("Get Score", type="primary", use_container_width=True)

if analyze_btn and user_post:
    if len(user_post.split()) < 5:
        st.error("Do not be lazy. Write a real post. A few words cannot be analyzed.")
    else:
        with st.spinner("Running ML Regression & GenAI Analysis..."):
            
            # 1. ML Prediction (Engagement Probability)
            if rf_model:
                predicted_score = rf_model.predict([user_post])[0]
            else:
                predicted_score = 50.0 # Fallback if model fails
            
            # 2. GenAI Critique (Clarity & Technical Depth)
            target_role = "Software Engineer" # We will fetch this dynamically from Supabase later
            prompt = f"""
            You are a Senior Technical Recruiter at a FAANG company. Analyze this LinkedIn post draft:
            "{user_post}"
            
            Provide a short, harsh critique focusing on:
            1. Clarity: Is the impact clear?
            2. Technical Depth: Is the technical vocabulary appropriate for a {target_role}?
            
            Format as a bulleted list. Be extremely concise. Max 3 bullet points.
            """
            ai_critique = get_gemini_response(prompt)
            
            # Display Results
            with col2:
                st.subheader("Live Analysis")
                
                # Metric 1: ML Score
                st.metric(label="Engagement Probability (ML Predicted)", value=f"{predicted_score:.1f}%")
                st.progress(int(predicted_score) / 100)
                
                # Metric 2 & 3: AI Heuristics (Simulated for UI speed, backed by Gemini critique)
                clarity = min(100, int(len(user_post.split()) * 1.5)) # Simple heuristic based on length
                st.metric(label="Clarity Score", value=f"{clarity}%")
                st.progress(clarity / 100)
                
                st.markdown("### AI Recruiter Critique")
                st.info(ai_critique)