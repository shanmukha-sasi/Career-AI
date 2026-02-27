import streamlit as st

class KeyManager:
    def __init__(self):
        # Initialize rotation indices
        if "gemini_index" not in st.session_state:
            st.session_state.gemini_index = 0
        if "serper_index" not in st.session_state:
            st.session_state.serper_index = 0

    def get_next_gemini_key(self):
        keys = st.secrets.get("GEMINI_API_KEYS", [])
        if not keys:
            raise ValueError("CRITICAL ERROR: No Gemini API keys found in secrets.toml.")
        
        # Modulo logic: selected_key = pool[request_count % len(pool)]
        selected_key = keys[st.session_state.gemini_index % len(keys)]
        
        # Advance the pointer for the next request
        st.session_state.gemini_index += 1
        return selected_key

    def get_next_serper_key(self):
        keys = st.secrets.get("SERPER_API_KEYS", [])
        if not keys:
            raise ValueError("CRITICAL ERROR: No Serper API keys found in secrets.toml.")
        
        selected_key = keys[st.session_state.serper_index % len(keys)]
        st.session_state.serper_index += 1
        return selected_key

# Instantiate a single manager to be imported elsewhere
key_manager = KeyManager()