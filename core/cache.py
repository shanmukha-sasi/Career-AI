import streamlit as st
from core.database import supabase

@st.cache_data(ttl=600, show_spinner=False) 
def get_cached_profile(user_id):
    """Fetches profile from Supabase and caches it for 10 minutes."""
    try:
        response = supabase.table("profiles").select("*").eq("id", user_id).execute()
        return response.data
    except Exception as e:
        return None

@st.cache_data(ttl=600, show_spinner=False)
def get_cached_skills(user_id):
    """Fetches skill matrix from Supabase and caches it for 10 minutes."""
    try:
        response = supabase.table("skill_matrix").select("*").eq("id", user_id).execute()
        return response.data
    except Exception as e:
        return None

def force_clear_cache():
    """Wipes the cache. Call this when a user edits their profile."""
    st.cache_data.clear()