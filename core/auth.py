import streamlit as st
from core.database import supabase

def login_user(email, password):
    try:
        response = supabase.auth.sign_in_with_password({"email": email, "password": password})
        st.session_state["user"] = response.user
        st.session_state["authenticated"] = True
        return True, "Login successful"
    except Exception as e:
        return False, str(e)

def signup_user(email, password):
    try:
        response = supabase.auth.sign_up({"email": email, "password": password})
        return True, "Signup successful! Check your email to confirm or login if email confirmation is disabled."
    except Exception as e:
        return False, str(e)

def logout_user():
    supabase.auth.sign_out()
    st.session_state["authenticated"] = False
    st.session_state["user"] = None