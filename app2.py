import streamlit as st
import requests
import json

st.set_page_config(page_title="Local Conflict Simulation AI", layout="wide")
st.title("Local Conflict Simulation AI")
st.markdown("Use this tool to simulate small-scale conflicts (villages/towns), assess legal precedent, and explore enforceable solutions.")

# Initialize session state
if "conflict_stage" not in st.session_state:
    st.session_state.conflict_stage = 1
    st.session_state.day = 1
    st.session_state.timeline = []
    st.session_state.suggestions = ""
    st.session_state.conflict_summary = ""
    st.session_state.country = ""

# API setup
API_URL = "https://openrouter.ai/api/v1/chat/completions"
API_KEY = st.secrets["openrouter"]["api_key"]

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

def query_ai(conflict, country, day):
    prompt = f"""
Conflict Day {day} - Local Scale Simulation

Conflict: {conflict}
Country: {country}

Provide:
- Brief summary of the conflict
- Relevant historical or legal precedents (specific to {country})
- Stakeholders involved and their motivations
- Legal provisions (constitution, land law, civil code, local bylaws, etc.)
- 2 proposed tactical or policy actions (risk & reward)
- 1 enforceable resolution based on legal or strategic grounds
- Short timeline update
- Compact Conflict Card: Summary, Risk Level, Probability of Resolution
"""

    payload = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": [{"role": "user", "content": prompt}]
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
        response.raise_for_status()
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f"❌ AI failed to generate a response.\n\n{str(e)}"

# User input
st.subheader("Define Your Conflict")
conflict = st.text_area("Conflict Scenario (village/town level)")
country = st.text_input("Country where this conflict is taking place")

if st.session_state.conflict_stage == 1:
    if st.button("Start Simulation"):
        if conflict and country:
            st.session_state.conflict_summary = conflict
            st.session_state.country = country
            st.session_state.conflict_stage = 2
        else:
            st.warning("Please enter both conflict and country.")

# Show conflict
if st.session_state.conflict_stage >= 2:
    st.subheader("Conflict Details")
    st.write(f"**Conflict:** {st.session_state.conflict_summary}")
    st.write(f"**Country:** {st.session_state.country}")

    if st.session_state.conflict_stage == 2:
        with st.spinner("Generating Day 1 Simulation..."):
            result = query_ai(st.session_state.conflict_summary, st.session_state.country, 1)
            st.session_state.suggestions = result
            st.session_state.timeline.append(("Day 1", result))
            st.session_state.conflict_stage = 3

# Display simulation
if st.session_state.conflict_stage >= 3:
    st.subheader(f"Day {st.session_state.day} Briefing")
    st.markdown(st.session_state.suggestions)

    if st.button("Simulate Next Day"):
        st.session_state.day += 1
        with st.spinner(f"Simulating Day {st.session_state.day}..."):
            result = query_ai(st.session_state.conflict_summary, st.session_state.country, st.session_state.day)
            st.session_state.suggestions = result
            st.session_state.timeline.append((f"Day {st.session_state.day}", result))

    # Timeline display
    if st.session_state.timeline:
        st.subheader("Conflict Timeline")
        for day, content in st.session_state.timeline:
            with st.expander(day):
                st.markdown(content)

st.markdown("---")
st.caption("Built for civic and legal education. Not real-world legal advice.")















