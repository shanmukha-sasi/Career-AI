import streamlit as st
from core.database import supabase
from utils.engine import get_gemini_response
from core.auth import logout_user

# 1. Security Check
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


st.title("Profile Optimization")
st.write("Review your current LinkedIn presence and use AI to generate high-impact improvements.")

# 3. Fetch User Context
user_id = st.session_state["user"].id
try:
    response = supabase.table("profiles").select("*").eq("id", user_id).execute()
    if not response.data:
        st.error("Profile data missing. Please complete Onboarding.")
        st.stop()
    user_profile = response.data[0]
    target_role = user_profile['target_role']
    target_ecosystem = user_profile['target_ecosystem']
    voice_tone = user_profile['voice_tone']
except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()

# 4. Input Layout
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("Current Presence")
    current_headline = st.text_area("Current Headline", placeholder="e.g., Student at RGUKT | Learning Python")
    current_about = st.text_area("About Section", placeholder="Paste your current about section here...", height=200)
    analyze_profile = st.button("Analyze & Optimize Profile", type="primary", use_container_width=True)

# 5. Intelligence Layer
if analyze_profile:
    if not current_headline or not current_about:
        st.warning("Provide both your current headline and about section for a complete analysis.")
    else:
        with st.spinner("Analyzing profile against FAANG benchmarks..."):
            
            # Prompt 1: Critique
            critique_prompt = f"""
            You are a strict FAANG recruiter hiring for a {target_role} role at a {target_ecosystem}.
            Analyze this LinkedIn profile:
            Headline: {current_headline}
            About: {current_about}
            
            Provide 3 bullet points of harsh, constructive critique. What is missing? Why would you reject them?
            """
            critique_response = get_gemini_response(critique_prompt)
            
            # Prompt 2: Optimization
            rewrite_prompt = f"""
            Rewrite the following LinkedIn profile for a user targeting a {target_role} role at a {target_ecosystem}.
            Tone should be: {voice_tone}.
            
            Original Headline: {current_headline}
            Original About: {current_about}
            
            Format your response exactly like this:
            [NEW HEADLINE]
            (Write the new headline here)
            
            [NEW ABOUT]
            (Write the new about section here)
            
             note : just 10 words in healine and 20 words in about section. Do not add any extra information or explanation. Do not self critique. Just give the rewritten headline and about section based on the critique and FAANG standards.
            """
            rewrite_response = get_gemini_response(rewrite_prompt)
            
            # Simple parsing of the response
            try:
                new_headline = rewrite_response.split("[NEW HEADLINE]")[1].split("[NEW ABOUT]")[0].strip()
                new_about = rewrite_response.split("[NEW ABOUT]")[1].strip()
            except:
                new_headline = "Error parsing AI response."
                new_about = rewrite_response

        with col2:
            st.subheader("AI Critique")
            st.info(critique_response)
            
        st.divider()
        st.subheader("AI Suggested Improvements")
        
        opt_col1, opt_col2 = st.columns(2)
        with opt_col1:
            st.text_area("Optimized Headline", value=new_headline, height=100)
        with opt_col2:
            st.text_area("Optimized About Section", value=new_about, height=300)