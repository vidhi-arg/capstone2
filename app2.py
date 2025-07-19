import streamlit as st
import requests
import json

st.set_page_config(page_title="Conflict Simulation AI", layout="wide")
st.title("Strategic Conflict Simulation AI")
st.markdown("Use this AI tool to simulate conflict scenarios, assess potential impacts, and explore policy or tactical solutions using structured inputs.")

# Sidebar Controls
st.sidebar.header("Simulation Controls")
reset_sim = st.sidebar.button("Start New Simulation")

# Initialize session state
if "conflict_stage" not in st.session_state or reset_sim:
    st.session_state.conflict_stage = 1
    st.session_state.timeline = []
    st.session_state.suggestions = ""
    st.session_state.day = 1
    st.session_state.conflict_summary = ""
    st.session_state.conflict_name = ""
    st.session_state.full_history = []

# API Setup
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
        return "AI failed to generate a response."

# Main Simulation Interface
st.subheader("Define a Conflict Scenario")
user_conflict = st.text_area("Describe the conflict scenario you would like to simulate:")

if st.session_state.conflict_stage == 1:
    if st.button("Start Simulation"):
        if user_conflict:
            st.session_state.conflict_summary = user_conflict
            st.session_state.conflict_stage = 2

if st.session_state.conflict_stage >= 2:
    st.subheader("Initial Conflict Briefing")
    st.write(st.session_state.conflict_summary)

    if st.session_state.conflict_stage == 2:
        with st.spinner("Generating initial analysis..."):
            prompt = f"""Conflict Scenario: {st.session_state.conflict_summary}
Provide:
- Two tactical options (with risk/reward analysis)
- One enforceable policy/strategic solution (infrastructure, legal, economic, military)
- Legal and jurisdictional challenges
- Key stakeholder impact table
- Historical parallel (brief)
- Short conflict outcome summary"""
            response = query_openrouter(prompt)
            st.session_state.suggestions = response
            st.session_state.timeline.append((f"Day 1", response))
            st.session_state.conflict_stage = 3

if st.session_state.conflict_stage >= 3:
    st.subheader(f"Day {st.session_state.day} Simulation Briefing")
    st.markdown(st.session_state.suggestions)

    if st.button("Simulate Next Day"):
        st.session_state.day += 1
        prompt = f"""Conflict: {st.session_state.conflict_summary}
Simulate Day {st.session_state.day} and provide:
- Two new tactical developments (with risks and expected outcomes)
- One specific, actionable solution (non-negotiation)
- Updated timeline of events
- Evolving legal and institutional response
- Stakeholder sentiment and behavior shifts
- Short historical analogy
- Conflict status summary"""
        with st.spinner("Processing next day..."):
            response = query_openrouter(prompt)
            st.session_state.suggestions = response
            st.session_state.timeline.append((f"Day {st.session_state.day}", response))

# Display Timeline
if st.session_state.timeline:
    st.subheader("Conflict Timeline")
    for day, content in st.session_state.timeline:
        with st.expander(day):
            st.markdown(content)

# Footer
st.markdown("---")
st.caption("This tool is for educational and strategic analysis purposes only. It does not constitute real-world policy or military advice.")











