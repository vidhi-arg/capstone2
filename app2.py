import streamlit as st
import requests
import random
import pandas as pd

st.set_page_config(page_title="Conflict Simulation", layout="centered")

# API key and model setup
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "meta-llama/llama-4-maverick:free"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# --- UI ---
st.title("Conflict Simulator (India Focus)")
conflict = st.text_area("Describe a conflict scenario:", placeholder="E.g. Protest in Delhi over education reform.")
day = st.session_state.get("day", 1)

if st.button("Simulate Next Day"):
    st.session_state.day = st.session_state.get("day", 1) + 1
    day = st.session_state.day

if conflict:
    prompt = f"Conflict: {conflict}\nDay {day}: What is the brief update? Give legal tensions (by article), short stakeholder impact (table), 2-3 outcome options, and 1 similar past conflict. Keep responses short and simple."

    payload = {
        "model": MODEL,
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }

    response = requests.post(API_URL, headers=headers, json=payload)

    if response.status_code == 200:
        result = response.json()
        try:
            reply = result["choices"][0]["message"]["content"]
            st.markdown("---")
            st.subheader(f" Day {day} Situation")
            st.markdown(reply)
        except:
            st.error("AI replied, but no valid message found.")
    else:
        st.error(f"Failed to get response. Status {response.status_code}: {response.text}")

    # Timeline indicator
    st.progress(min(day / 7, 1.0))

    # Simple Chaos Score (Mocked)
    chaos_score = random.randint(30, 90)
    st.metric(label=" Chaos Score", value=f"{chaos_score}/100")
else:
    st.info("Enter a conflict scenario to begin simulation.")



