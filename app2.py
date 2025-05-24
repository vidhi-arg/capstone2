import streamlit as st
import requests

# Set Streamlit page configuration
st.set_page_config(page_title="NetrSim Conflict Generator", layout="centered")

# App title
st.title(" NetrSim Conflict Generator")

# Load API key from Streamlit secrets
try:
    OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
except Exception as e:
    st.error(" API key not found. Please check your secrets configuration.")
    st.stop()

# API endpoint
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Define headers
headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# Define prompt
default_prompt = "Generate a very simple political or social conflict scenario suitable for a simulation."

# User input
user_prompt = st.text_area("Prompt for the AI", default_prompt, height=150)

if st.button(" Generate Conflict"):
    with st.spinner("Contacting Netr..."):
        payload = {
            "model": "openrouter/gpt-4o-mini",
            "messages": [
                {"role": "user", "content": user_prompt}
            ]
        }

        response = requests.post(API_URL, headers=headers, json=payload)

        if response.status_code == 200:
            result = response.json()
            content = result['choices'][0]['message']['content']
            st.subheader(" Conflict Scenario:")
            st.write(content)
        else:
            st.error(f" API Error {response.status_code}: {response.text}")



