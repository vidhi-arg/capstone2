import streamlit as st
import requests
import random
import json
import pandas as pd

st.set_page_config(page_title="Conflict Simulation AI", layout="wide")
st.title("🧠 Strategic Conflict Simulation AI")
st.markdown("Use this AI tool to simulate conflicts, assess escalation, and explore solutions.")

# Sidebar Controls
st.sidebar.header("Simulation Controls")
reset_sim = st.sidebar.button("🔁 Start New Conflict")

# State variables
if "conflict_stage" not in st.session_state or reset_sim:
    st.session_state.conflict_stage = 1
    st.session_state.timeline = []
    st.session_state.conflict_summary = ""
    st.session_state.suggestions = ""
    st.session_state.day = 1
    st.session_state.conflict_name = ""
    st.session_state.full_history = []
    st.session_state.stakeholder_impact = []
    st.session_state.outcome_cards = []
    st.session_state.legal_clashes = []
    st.session_state.historical_analogy = ""

# Conflict Generator

def generate_conflict():
    options = [
        "Dispute over local water distribution between two neighboring villages in Madhya Pradesh.",
        "Tension between student political groups in a university over national flag protocol.",
        "Market monopoly accusations between two regional vendors in a small town.",
        "Protests erupting due to relocation of a historical statue in a small city.",
        "Community clash over religious processions sharing the same route."
    ]
    return random.choice(options)

# OpenRouter communication
API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def query_openrouter(prompt):
    payload = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": [
            {"role": "user", "content": prompt}
        ]
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except:
        return "⚠️ AI failed to generate a response."

# UI
if st.session_state.conflict_stage == 1:
    if st.button("🎲 Generate Conflict"):
        st.session_state.conflict_summary = generate_conflict()
        st.session_state.conflict_stage = 2

if st.session_state.conflict_stage >= 2:
    st.subheader("📌 Conflict Briefing")
    st.write(st.session_state.conflict_summary)

    if st.session_state.conflict_stage == 2:
        with st.spinner("Analyzing tactical environment..."):
            prompt = f"Conflict: {st.session_state.conflict_summary}.\nProvide:\n- 2 Tactical actions with risk/reward.\n- 1 realistic solution (not talks).\n- Legal clash mapping.\n- Historical analogy.\n- Dynamic stakeholder table (impact levels: Low, Medium, High).\n- Outcome card. Keep it short."
            response = query_openrouter(prompt)
            st.session_state.suggestions = response
            st.session_state.timeline.append((f"Day 1", response))
            st.session_state.conflict_stage = 3

if st.session_state.conflict_stage >= 3:
    st.subheader(f"📅 Day {st.session_state.day} Briefing")
    st.markdown(st.session_state.suggestions)

    if st.button("📈 Next Day Simulation"):
        st.session_state.day += 1
        prompt = f"Day {st.session_state.day} update on: {st.session_state.conflict_summary}.\nGive:\n- 2 Tactical actions with risk/reward.\n- 1 realistic solution (no dialogue).\n- Legal update.\n- Stakeholder impact.\n- Historical comparison.\n- Outcome summary. Keep it concise."
        with st.spinner("Simulating next day..."):
            response = query_openrouter(prompt)
            st.session_state.suggestions = response
            st.session_state.timeline.append((f"Day {st.session_state.day}", response))

# Timeline
if len(st.session_state.timeline) > 0:
    st.subheader("🧭 Conflict Timeline")
    for day, briefing in st.session_state.timeline:
        with st.expander(day):
            st.markdown(briefing)

# Footer
st.markdown("---")
st.caption("Built for strategic educational simulations. Not real policy advice.")







