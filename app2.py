import streamlit as st
import requests
import random

# Streamlit page config
st.set_page_config(page_title="NetrSim: Peace Strategy Trainer", layout="centered")
st.title("🕊️ NetrSim: Peace Strategy Trainer")
st.markdown("""
This simulation suggests peaceful resolution strategies for small-scale conflicts inspired by principles from the Indian Constitution.
""")

# User input
conflict_input = st.text_area("Describe a small-scale conflict scenario:", "Two neighboring communities are in dispute over access to a shared water resource.")
generate_button = st.button("Generate Resolution Strategy")

# OpenRouter setup
API_URL = "https://openrouter.ai/api/v1/chat/completions"
MODEL = "meta-llama/llama-4-maverick:free"
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# OpenRouter prompt function
def query_openrouter(prompt):
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "You are a peaceful AI conflict mediator aligned with the Indian Constitution, specializing in resolution strategies."},
            {"role": "user", "content": prompt}
        ]
    }
    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        return response.json()["choices"][0]["message"]["content"]
    except requests.exceptions.RequestException as e:
        return f"Request failed: {e}"
    except Exception as e:
        return f"Unexpected error: {e}"

# Escalation & outcome generator
def simulate_escalation(conflict):
    escalation_level = random.choice(["low", "moderate", "high"])
    if escalation_level == "low":
        outcome = "The situation is resolved through community dialogue and local governance mechanisms."
    elif escalation_level == "moderate":
        outcome = "Some tension continues, but state authorities mediate to ensure resolution within legal frameworks."
    else:
        outcome = "The issue escalates to legal courts but is peacefully handled using Articles 39(b) and 51A(c) of the Constitution."
    return escalation_level, outcome

# Main execution
if generate_button and conflict_input:
    with st.spinner("Thinking like a peaceful strategist..."):
        prompt = f"Conflict: {conflict_input}\nProvide a peaceful resolution strategy aligned with the Indian Constitution."
        action_suggestions = query_openrouter(prompt)

        escalation_level, outcome = simulate_escalation(conflict_input)

        st.subheader("🔍 Strategy")
        st.markdown(action_suggestions)

        st.subheader("📈 Escalation Level")
        st.info(escalation_level.capitalize())

        st.subheader("🔮 Predicted Outcome")
        st.success(outcome)


