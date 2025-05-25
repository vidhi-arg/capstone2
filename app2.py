import streamlit as st
import requests
import random
import json

st.set_page_config(page_title="Conflict Simulation AI", layout="wide")
st.title("🧠 Strategic Conflict Simulation AI")
st.markdown("Use this AI tool to simulate conflicts, assess chaos potential, and explore tactical actions.")

# Sidebar Controls
st.sidebar.header("Simulation Controls")
reset_sim = st.sidebar.button("🔁 Start New Conflict")

# State variables
if "conflict_stage" not in st.session_state or reset_sim:
    st.session_state.conflict_stage = 1
    st.session_state.timeline = []
    st.session_state.suggestions = ""
    st.session_state.day = 1
    st.session_state.conflict_summary = ""
    st.session_state.conflict_name = ""
    st.session_state.full_history = []

# Conflict Generator
conflict_list = [
    "Dispute over CCTV installation between privacy-conscious tenants and security-focused residents in Pune.",
    "Clash between two farmer groups over canal water distribution in Tamil Nadu.",
    "Tension in a college over dress code enforcement perceived as discriminatory.",
    "Vendor rivalry in a small city market over access to a government contract.",
    "Protest over illegal encroachment of a community playground by a political group."
]

def generate_conflict():
    return random.choice(conflict_list)

# API communication
API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def query_openrouter(prompt):
    payload = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except:
        return "⚠️ AI failed to generate a response."

# Main Simulation UI
if st.session_state.conflict_stage == 1:
    if st.button("🎲 Generate Conflict"):
        st.session_state.conflict_summary = generate_conflict()
        st.session_state.conflict_stage = 2

if st.session_state.conflict_stage >= 2:
    st.subheader("📌 Conflict Briefing")
    st.write(st.session_state.conflict_summary)

    if st.session_state.conflict_stage == 2:
        with st.spinner("Analyzing scenario..."):
            prompt = f"Conflict: {st.session_state.conflict_summary}. Provide:
            - 2 tactical actions (risk & reward)
            - 1 realistic hard solution (legal/economic/strategic)
            - Legal clash mapping
            - Key stakeholder impact table
            - Short historical analogy
            - Conflict outcome card (brief)"
            response = query_openrouter(prompt)
            st.session_state.suggestions = response
            st.session_state.timeline.append((f"Day 1", response))
            st.session_state.conflict_stage = 3

if st.session_state.conflict_stage >= 3:
    st.subheader(f"📅 Day {st.session_state.day} Briefing")
    st.markdown(st.session_state.suggestions)

    if st.button("📈 Next Day Simulation"):
        st.session_state.day += 1
        prompt = f"Conflict Day {st.session_state.day}: {st.session_state.conflict_summary}. Provide updates with:
        - 2 new tactical moves with risk/reward
        - 1 actual enforceable solution (not negotiation)
        - Timeline update
        - Legal evolution
        - Stakeholder shifts
        - Historical parallel
        - Conflict card summary (short)"
        with st.spinner("Simulating day..."):
            response = query_openrouter(prompt)
            st.session_state.suggestions = response
            st.session_state.timeline.append((f"Day {st.session_state.day}", response))

# Timeline Display
if st.session_state.timeline:
    st.subheader("🧭 Conflict Timeline")
    for day, content in st.session_state.timeline:
        with st.expander(day):
            st.markdown(content)

st.markdown("---")
st.caption("Built for tactical AI simulations. Not real-world policy guidance.")








