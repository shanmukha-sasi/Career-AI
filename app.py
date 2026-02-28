import streamlit as st
from core.auth import login_user, signup_user, logout_user

# Must be the first Streamlit command
st.set_page_config(page_title="Career AI", page_icon="🚀", layout="wide")

# Function to load custom CSS
def load_css(file_name):
    try:
        with open(file_name) as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)
    except Exception as e:
        pass # Fail silently if file is missing during deployment

# Inject the Glassmorphism CSS
load_css("assets/style.css")

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False
if "show_login" not in st.session_state:
    st.session_state["show_login"] = False
if "show_about" not in st.session_state:
    st.session_state["show_about"] = False

def show_login_page():
    # Back button to return to the landing page
    st.button("← Back to Home", on_click=lambda: st.session_state.update({"show_login": False}))
    
    # Centered login UI
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Access Career AI")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", use_container_width=True):
                if email and password:
                    success, msg = login_user(email, password)
                    if success:
                        st.success(msg)
                        st.switch_page("pages/1_Dashboard.py")
                    else:
                        st.error(msg)
                else:
                    st.warning("Do not be lazy. Enter both email and password.")
                    
        with tab2:
            new_email = st.text_input("Email", key="signup_email")
            new_password = st.text_input("Password", type="password", key="signup_pass")
            if st.button("Sign Up", use_container_width=True):
                if new_email and new_password:
                    success, msg = signup_user(new_email, new_password)
                    if success:
                        st.success(msg)
                    else:
                        st.error(msg)
                else:
                    st.warning("Enter valid credentials.")

def show_landing_page():
    # 1. Top Navigation Layout (Aligned to Center)
    nav_col1, nav_col2, nav_col3, nav_col4 = st.columns([1.5, 2.5, 1, 1], vertical_alignment="center")
    
    with nav_col1:
        # Professional SVG Logo (Inline)
        logo_svg = """
        <div style="display: flex; align-items: center; gap: 10px;">
            <svg width="35" height="35" viewBox="0 0 24 24" fill="none" xmlns="http://www.w3.org/2000/svg">
                <path d="M12 2L2 7L12 12L22 7L12 2Z" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 17L12 22L22 17" stroke="#3b82f6" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
                <path d="M2 12L12 17L22 12" stroke="#10b981" stroke-width="2" stroke-linecap="round" stroke-linejoin="round"/>
            </svg>
            <h3 style="margin: 0; padding: 0; color: #f8fafc;">Career AI</h3>
        </div>
        """
        st.markdown(logo_svg, unsafe_allow_html=True)
        
    with nav_col3:
        if st.button("Features", use_container_width=True):
            st.session_state.show_about = not st.session_state.show_about
            st.rerun()
            
    with nav_col4:
        if st.button("Login", type="secondary", use_container_width=True):
            st.session_state.show_login = True
            st.rerun()

    # Precision-controlled custom divider (Replaces st.divider)
    st.markdown("<hr style='margin: 0.5rem 0 2rem 0; border: none; border-top: 1px solid rgba(255, 255, 255, 0.1);'>", unsafe_allow_html=True)

    # 2. Hero Section (Perfectly Centered Margins)
    st.markdown("<div style='margin-top: 1.5rem; margin-bottom: 4rem;'>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 3.8rem; margin-bottom: 0;'>Personal Branding, <br><span style='color: #3b82f6;'>Powered by Intelligence.</span></h1>", unsafe_allow_html=True)
    
    # Centered subheadline using Flexbox
    st.markdown(
        """
        <div style='display: flex; justify-content: center; width: 100%;'>
            <p style='text-align: center; font-size: 1.2rem; color: #94a3b8; max-width: 750px; margin: 1.5rem 0 2.5rem 0;'>
                Elevate your professional presence with our AI-driven insights designed to accelerate your career growth.
            </p>
        </div>
        """, 
        unsafe_allow_html=True
    )
    
    # Get Started Button (Centered)
    col1, col2, col3 = st.columns([1.5, 1, 1.5])
    with col2:
        if st.button("Get Started", type="primary", use_container_width=True):
            st.session_state.show_login = True
            st.rerun()
    st.markdown("</div>", unsafe_allow_html=True)

    # 3. Features Z-Pattern Section (Toggled)
    if st.session_state.show_about:
        # Precision custom divider
        st.markdown("<hr style='margin: 3rem 0 2rem 0; border: none; border-top: 1px solid rgba(255, 255, 255, 0.1);'>", unsafe_allow_html=True)
        st.markdown("<h2 style='text-align: center; margin-bottom: 2rem;'>Our Core Architecture</h2>", unsafe_allow_html=True)
        
        # Row 1 (Text Left, Graphic Right)
        r1c1, r1c2 = st.columns(2)
        with r1c1:
            st.markdown("### ✨ LinkedIn Optimization")
            st.write("Our AI analyzes your profile against industry leaders to suggest high-impact keywords, headline rewrites, and summary enhancements that recruiters love.")
        with r1c2:
            with st.container(border=True):
                st.info("⚙️ Dynamic AI Text Analysis & Rewrite Engine")
        
        st.write("")
        st.write("")
        
        # Row 2 (Graphic Left, Text Right)
        r2c1, r2c2 = st.columns(2)
        with r2c1:
            with st.container(border=True):
                st.success("⚡ Real-Time RAG Mentorship Pipeline")
        with r2c2:
            st.markdown("### 🤝 Connection Hub")
            st.write("Discover and connect with mentors, peers, and industry leaders. Our smart matching algorithm finds the people who can truly accelerate your career journey.")
            
        st.write("")
        st.write("")
        
        # Row 3 (Text Left, Graphic Right)
        r3c1, r3c2 = st.columns(2)
        with r3c1:
            st.markdown("### 📊 Skill Gap Checker")
            st.write("Compare your current skill set against your dream job requirements. We identify exactly what's missing and recommend the best courses to bridge the gap.")
        with r3c2:
            with st.container(border=True):
                st.warning("🧠 K-Means Clustering & Radar Visualization")
                
        st.write("")
        st.write("")
        
        # Row 4 (Graphic Left, Text Right)
        r4c1, r4c2 = st.columns(2)
        with r4c1:
            with st.container(border=True):
                st.error("📈 Predictive Random Forest Regression")
        with r4c2:
            st.markdown("### 🔥 Viral Score Card")
            st.write("Understand the potential impact of your posts before you publish. Our predictive model scores your content based on engagement probability and reach.")

#The GateKeeper Logic
if st.session_state["authenticated"]:
    # If they are already authenticated and hit the root URL, push them to the dashboard immediately.
    st.switch_page("pages/1_Dashboard.py")
else:
    # State Machine Router
    if st.session_state["show_login"]:
        show_login_page()
    else:
        show_landing_page()