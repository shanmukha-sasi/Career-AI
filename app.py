import streamlit as st
from core.auth import login_user, signup_user, logout_user

# Must be the first Streamlit command
st.set_page_config(page_title="Career AI", page_icon="🚀", layout="wide")

# Initialize session state variables
if "authenticated" not in st.session_state:
    st.session_state["authenticated"] = False

def show_login_page():
    # Centered login UI
    col1, col2, col3 = st.columns([1, 2, 1])
    with col2:
        st.title("Career AI")
        st.write("Personal Branding, Powered by Intelligence.")
        
        tab1, tab2 = st.tabs(["Login", "Sign Up"])
        
        with tab1:
            email = st.text_input("Email", key="login_email")
            password = st.text_input("Password", type="password", key="login_pass")
            if st.button("Login", use_container_width=True):
                if email and password:
                    success, msg = login_user(email, password)
                    if success:
                        st.success(msg)
                        st.switch_page("pages/1_Dashboard.py") # <--- ROUTING ADDED HERE
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

# The Gatekeeper Logic
if not st.session_state["authenticated"]:
    show_login_page()
else:
    # If they are already authenticated and hit the root URL, push them to the dashboard immediately.
    st.switch_page("pages/1_Dashboard.py")