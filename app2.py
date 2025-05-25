import streamlit as st
import requests
import json

st.set_page_config(page_title="NetrSim AI", layout="wide")
st.title(" NetrSim: Strategic Conflict Simulator")

# Sidebar
st.sidebar.header("Simulation Controls")
reset_sim = st.sidebar.button(" Reset Simulation")

# Initialize or Reset
if "conflict_stage" not in st.session_state or reset_sim:
    st.session_state.conflict_stage = 0
    st.session_state.timeline = []
    st.session_state.day = 0
    st.session_state.suggestions = ""
    st.session_state.conflict_text = ""

# API config
API_URL = "https://openrouter.ai/api/v1/chat/completions"
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def query_ai(prompt):
    payload = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": [{"role": "user", "content": prompt}]
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    try:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    except Exception as e:
        return f" Error in AI response: {str(e)}"

# Stage 0: Input conflict
if st.session_state.conflict_stage == 0:
    st.subheader(" Define Your Conflict Scenario")
    st.session_state.conflict_text = st.text_area("Describe a small-scale conflict:", height=100)
    if st.button(" Launch Simulation"):
        if st.session_state.conflict_text.strip():
            st.session_state.conflict_stage = 1
            st.session_state.day = 1

# Stage 1: Day 1 briefing
if st.session_state.conflict_stage == 1:
    st.subheader(f" Conflict Briefing — Day {st.session_state.day}")
    st.markdown(f"**Conflict:** {st.session_state.conflict_text}")
    
    with st.spinner("Simulating Day 1..."):
        prompt = f"""Conflict: {st.session_state.conflict_text}
Generate a DAY 1 response including:
- 2 tactical actions (with risk/reward)
- 1 realistic enforceable solution (legal/economic/strategic)
- Legal clash mapping
- Dynamic stakeholder impact table
- Historical analogy (short)
- Conflict outcome card (1-2 lines)
Keep it short and actionable."""
        response = query_ai(prompt)
        st.session_state.suggestions = response
        st.session_state.timeline.append((f"Day {st.session_state.day}", response))
        st.session_state.conflict_stage = 2

# Stage 2+: Show current day & simulate next day
if st.session_state.conflict_stage >= 2:
    st.subheader(f" Day {st.session_state.day} Briefing")
    st.markdown(st.session_state.suggestions)

    if st.button("➡ Next Day"):
        st.session_state.day += 1
        with st.spinner(f"Simulating Day {st.session_state.day}..."):
            prompt = f"""Conflict ongoing: {st.session_state.conflict_text}
Generate Day {st.session_state.day} update with:
- 2 new tactical actions (with risk/reward)
- 1 actual enforceable solution (non-negotiation based)
- Timeline update
- Legal evolution
- Stakeholder shifts
- Historical parallel (brief)
- Conflict outcome card (concise)"""
            response = query_ai(prompt)
            st.session_state.suggestions = response
            st.session_state.timeline.append((f"Day {st.session_state.day}", response))

# Timeline
if st.session_state.timeline:
    st.subheader(" Conflict Timeline")
    for day, content in st.session_state.timeline:
        with st.expander(day):
            st.markdown(content)

st.markdown("---")
st.caption("Built for strategic simulations. Not real policy advice.")









