import streamlit as st
import requests
import json
from core.database import supabase
from utils.engine import get_gemini_response
from core.key_manager import key_manager
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

st.title("Connection Hub")
st.write("Discover industry leaders whose career trajectories align with your 5-year goals. Powered by Real-Time RAG.")

# 3. Fetch User Context
user_id = st.session_state["user"].id
try:
    response = supabase.table("profiles").select("*").eq("id", user_id).execute()
    if not response.data:
        st.error("Profile data missing. Please complete Onboarding.")
        st.stop()
    user_profile = response.data[0]
    target_role = user_profile['target_role']
    target_eco = user_profile['target_ecosystem']
except Exception as e:
    st.error(f"Database Error: {e}")
    st.stop()

# 4. Agentic Search Logic
def search_mentors(role, eco):
    # Phase 1: AI generates optimal search query
    query_prompt = f"Generate a strict Google search query to find LinkedIn profiles of Senior {role} professionals working at {eco} companies. Return ONLY the search string, no markdown, no quotes. Example: site:linkedin.com/in/ 'Senior Software Engineer' 'Google'."
    search_query = get_gemini_response(query_prompt).strip()
    
    # Phase 2: Serper.ai execution via Round Robin Key Manager
    try:
        serper_key = key_manager.get_next_serper_key()
    except Exception as e:
        st.error(str(e))
        return None

    url = "https://google.serper.dev/search"
    payload = json.dumps({"q": search_query, "num": 1})
    headers = {
        'X-API-KEY': serper_key,
        'Content-Type': 'application/json'
    }
    
    try:
        response = requests.request("POST", url, headers=headers, data=payload)
        results = response.json().get('organic', [])
        return results
    except Exception as e:
        st.error(f"Network request failed: {e}")
        return None

if st.button("Find Matching Mentors", type="primary"):
    with st.spinner("Initiating RAG Pipeline: Executing Live LinkedIn Search..."):
        mentors = search_mentors(target_role, target_eco)
        
        if not mentors:
            st.error("Search Engine API failed. Verify your Serper API keys in secrets.toml.")
        else:
            st.success(f"Successfully retrieved {len(mentors)} live industry profiles.")
            
            # Phase 3: AI generates the "Why Connect" Pitch for each card
            for m in mentors:
                title = m.get('title', 'LinkedIn Member').replace('- LinkedIn', '').strip()
                link = m.get('link', '#')
                snippet = m.get('snippet', 'No snippet available.')
                
                pitch_prompt = f"Based on this professional's search snippet: '{snippet}', write a 1-sentence, highly personalized pitch on why a student aiming for a {target_role} role should connect with them. Be professional and aggressive."
                pitch = get_gemini_response(pitch_prompt)
                
                # UI Card Rendering
                with st.container():
                    st.markdown(f"### [{title}]({link})")
                    st.write(f"**AI Synergy Pitch:** {pitch}")
                    st.link_button("View Profile & Connect", link)
                    st.divider()