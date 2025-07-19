import streamlit as st
import requests
import json

st.set_page_config(page_title="Local Conflict Simulation AI", layout="wide")
st.title("Local Conflict Simulation AI")
st.markdown("Use this tool to simulate small-scale conflicts in villages or towns, evaluate legal context, and explore enforceable solutions.")

# Sidebar Controls
st.sidebar.header("Simulation Controls")
reset_sim = st.sidebar.button("Start New Conflict")

# Session State Initialization
if "conflict_stage" not in st.session_state or reset_sim:
    st.session_state.conflict_stage = 1
    st.session_state.timeline = []
    st.session_state.suggestions = ""
    st.session_state.day = 1
    st.session_state.conflict_summary = ""
    st.session_state.conflict_name = ""
    st.session_state.country = ""

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

# UI
st.subheader("Enter a Local Conflict")
user_conflict = st.text_area("Describe your local conflict scenario")
country = st.text_input("Country")

if st.session_state.conflict_stage == 1:
    if st.button("Start Simulation"):
        if user_conflict and country:
            st.session_state.conflict_summary = user_conflict
            st.session_state.country = country
            st.session_state.conflict_stage = 2

if st.session_state.conflict_stage >= 2:
    st.subheader("Conflict Briefing")
    st.write(f"**Conflict:** {st.session_state.conflict_summary}")
    st.write(f"**Country:** {st.session_state.country}")

    if st.session_state.conflict_stage == 2:
        with st.spinner("Analyzing legal and historical context..."):
            prompt = f"""
Conflict Simulation for Local Dispute

Location: {st.session_state.country}  
Conflict: {st.session_state.conflict_summary}

Provide the following in a formal legal-policy tone:
1. Conflict Background: Explain the likely root causes of this issue in a small-town or village context.
2. Past Rulings: Cite real or likely past court rulings, panchayat resolutions, or administrative interventions in similar issues within {st.session_state.country}.
3. Relevant Laws/Articles: Mention 2–3 constitutional articles, state laws, or customary codes relevant to this conflict.
4. Key Stakeholders: List all parties affected or involved (villagers, caste/community groups, NGOs, police, district administration, etc.)
5. Legal & Strategic Options:
   - Two enforceable interventions (legal, administrative, or infrastructure-based)
   - Risk and reward for each option
6. Historical Parallel: Refer briefly to a similar case from the past 50 years in {st.session_state.country}, and how it was resolved.
7. Conflict Outcome Card:
   - Legal status: ✅ Constitutional / ⚠️ Unclear / ❌ Illegal  
   - Stakeholder risk index: High / Medium / Low  
   - Escalation potential: High / Medium / Low  
   - Conflict status summary
"""
            response = query_openrouter(prompt)
            st.session_state.suggestions = response
            st.session_state.timeline.append((f"Day 1", response))
            st.session_state.conflict_stage = 3

if st.session_state.conflict_stage >= 3:
    st.subheader(f"Day {st.session_state.day} Briefing")
    st.markdown(st.session_state.suggestions)

    if st.button("Next Day Simulation"):
        st.session_state.day += 1
        prompt = f"""
Conflict Day {st.session_state.day}: {st.session_state.conflict_summary} in {st.session_state.country}

Update the simulation with:
- 2 new legal or administrative interventions
- Timeline update (brief)
- Constitution/law references
- Stakeholder shifts
- Risk & reward of each move
- Outcome card update
"""
        with st.spinner("Simulating day..."):
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
st.caption("This app simulates legal and policy perspectives on localized conflicts. Not official legal advice.")












