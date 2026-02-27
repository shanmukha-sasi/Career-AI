import streamlit as st
import pandas as pd
import plotly.graph_objects as go
import joblib
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


st.title("Skill Gap Analyzer")
st.write("Compare your current technical DNA against your dream job requirements.")

# 3. Fetch Contextual User Data from Supabase
user_id = st.session_state["user"].id
try:
    response = supabase.table("skill_matrix").select("*").eq("id", user_id).execute()
    if not response.data:
        st.warning("Skill data missing. Please complete Onboarding first.")
        st.stop()
    user_skills = response.data[0]
except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()

# Formatting data for the ML and Radar Chart
categories = ['DSA', 'OOPS', 'DBMS', 'OS', 'System Design']
user_values = [
    user_skills['dsa'], 
    user_skills['oops'], 
    user_skills['dbms'], 
    user_skills['os'], 
    user_skills['system_design']
]

# 4. Target Input
target_job = st.text_input("Where do you want to go next?", placeholder="e.g., SDE at Google")

if target_job:
    # Simulating Target Requirements (In production, this comes from a live job scraper)
    # If it is a top-tier role, the baseline is automatically high.
    target_values = [5, 4, 4, 4, 5] if "SDE" in target_job.upper() or "GOOGLE" in target_job.upper() else [4, 4, 4, 3, 3]

    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("Visual Analysis")
        # Plotly Radar Chart (Requires closing the loop by repeating the first value)
        fig = go.Figure()
        fig.add_trace(go.Scatterpolar(
            r=user_values + [user_values[0]], 
            theta=categories + [categories[0]], 
            fill='toself', name='Your Skills', line_color='#2563eb'
        ))
        fig.add_trace(go.Scatterpolar(
            r=target_values + [target_values[0]], 
            theta=categories + [categories[0]], 
            fill='toself', name='Target Requirements', line_color='#10b981'
        ))
        fig.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 5])), 
            showlegend=True,
            margin=dict(l=40, r=40, t=40, b=40)
        )
        st.plotly_chart(fig, use_container_width=True)
        
        # ML K-Means Integration
        try:
            kmeans = joblib.load('ml_models/skill_clusterer.pkl')
            cluster = kmeans.predict([user_values])[0]
            st.caption(f"🤖 ML Persona Cluster Detected: Cohort Type {cluster + 1}")
        except:
            st.caption("ML Clusterer Offline.")

    with col2:
        st.subheader("Adaptive Roadmap")
        with st.spinner("Calculating mathematical skill gaps and querying Gemini..."):
            
            # Logic: Only ask AI to help with skills where Target > User
            gaps = {cat: (tgt - usr) for cat, usr, tgt in zip(categories, user_values, target_values) if tgt > usr}
            
            if not gaps:
                st.success("Your fundamentals match or exceed the requirements for this role. Time to focus on project execution.")
            else:
                gap_str = ", ".join([f"{k} (Shortfall: {v} points)" for k, v in gaps.items()])
                
                # Strict GenAI Prompt
                prompt = f"""
                The user wants to secure the role: '{target_job}'. 
                Our ML model shows they have specific technical gaps in: {gap_str}. 
                
                Generate a strict, aggressive 3-month technical roadmap to close EXACTLY these gaps. 
                Keep it under 5 lines and 5 words each line max. Use markdown checkboxes. Do not sugarcoat it. Focus on FAANG-level preparation.
                """
                
                roadmap = get_gemini_response(prompt)
                st.markdown(roadmap)