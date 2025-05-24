import streamlit as st
import requests

# Load API key securely
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]

# Set Streamlit page config
st.set_page_config(page_title="NetrSim: Peace Strategy Trainer", layout="centered")

# Title and Instructions
st.title("🕊️ NetrSim: Peace Strategy Trainer")
st.markdown("Enter a simple **conflict scenario** (preferably related to civic issues or Indian constitutional matters), and NetrSim will suggest possible peace strategies.")

# User Input
user_input = st.text_area("💬 Enter a conflict scenario:", placeholder="E.g., Dispute over religious procession route in a mixed community area")

# Query OpenRouter Function
def query_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": [
            {"role": "system", "content": "You are a peace strategist specializing in local Indian civic and constitutional conflicts."},
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(url, headers=headers, json=payload)
    if response.status_code == 200:
        try:
            result = response.json()
            return result["choices"][0]["message"]["content"]
        except Exception as e:
            return f"⚠️ Failed to parse response: {e}"
    else:
        return f"❌ Error {response.status_code}: {response.text}"

# Generate Button
if st.button("Generate Peace Strategy"):
    if user_input.strip():
        with st.spinner("Analyzing conflict and drafting strategies..."):
            result = query_openrouter(user_input)
            st.markdown("### 🧭 Suggested Strategy:")
            st.write(result)
    else:
        st.warning("Please enter a conflict scenario first.")

