import streamlit as st
import requests
import json

st.set_page_config(page_title="Conflict Simulation AI", layout="wide")
st.title("Strategic Conflict Simulation AI")
st.markdown("Use this AI tool to simulate **local conflicts**, assess potential outcomes, and explore legal and historical solutions.")

# Sidebar Controls
st.sidebar.header("Simulation Controls")
reset_sim = st.sidebar.button("Start New Conflict")

# Initialize session state variables
if "conflict_stage" not in st.session_state or reset_sim:
    st.session_state.conflict_stage = 1
    st.session_state.timeline = []
    st.session_state.suggestions = ""
    st.session_state.day = 1
    st.session_state.conflict_summary = ""
    st.session_state.country = ""
    st.session_state.full_history = []

# API communication setup
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

# User Input
st.subheader("Enter a Local Conflict")
conflict_description = st.text_area("Describe the conflict in detail (local dispute, village issue, etc.)")
country_input = st.text_input("Which country is this conflict occurring in?")

if st.session_state.conflict_stage == 1:
    if st.button("Start Simulation"):
        if conflict_description and country_input:
            st.session_state.conflict_summary = conflict_description
            st.session_state.country = country_input
            st.session_state.conflict_stage = 2
        else:
            st.warning("Please enter both the conflict and the country.")

# Show country
if st.session_state.country:
    st.write(f"**Country:** {st.session_state.country}")

# Simulation stage 2: Initial analysis
if st.session_state.conflict_stage == 2:
    with st.spinner("Analyzing conflict scenario..."):
        prompt = f"""
Conflict Description: {st.session_state.conflict_summary}
Country: {st.session_state.country}

Generate a detailed briefing:
- Historical context of similar conflicts in this country
- Past rulings by local/national courts or constitutional articles that apply
- Key stakeholders involved (villagers, government bodies, others)
- Legal and constitutional frameworks likely to be invoked
- 2 tactical action suggestions (with risks and rewards)
- 1 enforceable solution (policy/legal/infrastructure)
- Conflict status summary
"""
        response = query_openrouter(prompt)
        st.session_state.suggestions = response
        st.session_state.timeline.append((f"Day 1", response))
        st.session_state.conflict_stage = 3

# Simulation stage 3: Show results and iterate
if st.session_state.conflict_stage >= 3:
    st.subheader(f"Day {st.session_state.day} Briefing")
    st.markdown(st.session_state.suggestions)

    if st.button("Next Day Simulation"):
        st.session_state.day += 1
        with st.spinner("Simulating next day..."):
            prompt = f"""
Conflict: {st.session_state.conflict_summary}
Country: {st.session_state.country}

Simulate Day {st.session_state.day}. Provide:
- Updated legal or civil developments
- Stakeholder movements or changes in positions
- New tactical options (2 suggestions, with risks and rewards)
- Constitution/court references evolving due to new circumstances
- One practical solution or intervention
- Conflict trajectory update
"""
            response = query_openrouter(prompt)
            st.session_state.suggestions = response
            st.session_state.timeline.append((f"Day {st.session_state.day}", response))

# Timeline Display
if st.session_state.timeline:
    st.subheader("Conflict Timeline")
    for day, content in st.session_state.timeline:
        with st.expander(day):
            st.markdown(content)

st.markdown("---")
st.caption("Built for educational simulations. Not real-world policy advice.")













