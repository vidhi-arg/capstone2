import streamlit as st
import requests
import json

# App config
st.set_page_config(page_title="NetrSim: Peace Strategy Trainer", layout="centered")
st.title("🕊️ NetrSim: Peace Strategy Trainer")

# Input from user
conflict = st.text_area("Describe the conflict scenario (local or national):")
escalate = st.checkbox("Include escalation logic")
show_outcomes = st.checkbox("Show predicted outcomes")

# Load API key
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
MODEL = "meta-llama/llama-4-maverick:free"

# API call function
def query_openrouter(prompt):
    url = "https://openrouter.ai/api/v1/chat/completions"
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }
    body = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(url, headers=headers, json=body)
    try:
        return response.json()["choices"][0]["message"]["content"]
    except Exception as e:
        st.error(f"Error parsing response: {e}")
        return None

# Generate escalation logic & outcomes
if conflict:
    prompt = f"""
    You are a peace strategist AI trained on the Indian Constitution, ethics, and civil behavior.
    A small-scale civic or political conflict has occurred:

    """
    prompt += conflict + "\n"

    if escalate:
        prompt += "\nPredict how this conflict might escalate if not handled properly. Include possible triggers, actors, and timeline."

    if show_outcomes:
        prompt += "\nAlso predict potential outcomes based on peaceful vs non-peaceful strategies."

    prompt += "\nFinally, suggest 3 constitutionally-aligned peaceful strategies to manage this conflict."

    with st.spinner("Analyzing conflict and generating response..."):
        result = query_openrouter(prompt)
        if result:
            st.markdown("---")
            st.subheader("🧠 AI Suggestions")
            st.markdown(result)

