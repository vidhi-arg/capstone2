import streamlit as st
import requests
import random
import time

st.set_page_config(page_title="NetrSim: Peace Strategy Trainer", layout="centered")
st.title(" NetrSim: Peace Strategy Trainer")

# Load API key
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# Session State Setup
if "history" not in st.session_state:
    st.session_state.history = []
if "turn" not in st.session_state:
    st.session_state.turn = 1

# Chaos score function
def calculate_chaos_score(response_text):
    chaos_keywords = ["violation", "protest", "arrest", "tension", "riot", "sedition", "curfew"]
    score = sum(word in response_text.lower() for word in chaos_keywords) * 15
    return min(score + random.randint(0, 10), 100)

# Chat request function
def ask_openrouter(prompt):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    payload = {
        model = "openrouter/openai/gpt-3.5-turbo",  # Lightweight model for free tier
        "messages": [
            {"role": "system", "content": "You are NetrSim, an AI simulating internal political situations in India. Base your responses on the Indian Constitution and real-world civil dynamics. Include Articles and basic rights when relevant."},
            {"role": "user", "content": prompt}
        ]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            result = response.json()
            return result['choices'][0]['message']['content']
        else:
            return f" Error {response.status_code}: {response.text}"
    except Exception as e:
        return f" Exception: {str(e)}"

# User Input
user_input = st.text_input(f"Enter situation for Turn {st.session_state.turn}:", "A protest erupts in a village over land acquisition.")
if st.button("Simulate Conflict"):
    with st.spinner("Simulating..."):
        prompt = f"Turn {st.session_state.turn} - {user_input}"
        ai_response = ask_openrouter(prompt)

        chaos_score = calculate_chaos_score(ai_response)

        st.session_state.history.append({
            "turn": st.session_state.turn,
            "input": user_input,
            "response": ai_response,
            "chaos": chaos_score
        })
        st.session_state.turn += 1

# Show history
for entry in reversed(st.session_state.history):
    with st.expander(f"Turn {entry['turn']} - Chaos Score: {entry['chaos']}/100"):
        st.markdown(f"**Prompt:** {entry['input']}")
        st.markdown(f"**Response:**\n{entry['response']}")

st.markdown("---")
st.markdown("Made for SDG 16 - Peace, Justice and Strong Institutions")




