import streamlit as st
import requests

st.set_page_config(page_title="NetrSim: Peace Strategy Trainer", layout="centered")

# Load your OpenRouter API key from secrets.toml
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"
HEADERS = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json",
}

def query_openrouter(prompt):
    payload = {
        "model": "meta-llama/llama-4-maverick:free",
        "messages": [{"role": "user", "content": prompt}],
        "max_tokens": 200,
        "temperature": 0.7,
        "top_p": 0.95,
    }
    response = requests.post(API_URL, headers=HEADERS, json=payload)
    if response.status_code == 200:
        try:
            data = response.json()
            return data["choices"][0]["message"]["content"].strip()
        except Exception:
            return "Error: Could not parse response."
    else:
        return f"Error {response.status_code}: {response.text}"

def generate_prompt(conflict_description, day):
    return f"""
Conflict: {conflict_description}

Day {day} briefing:
- Briefly describe what happened today.
- Suggest 1-2 possible solutions or next steps.
- Mention any relevant Indian Constitution legal clashes.
- Summarize key stakeholder impacts.
- Keep response very short and simple (max 3 sentences).
"""

# --- Streamlit UI ---

st.title("NetrSim: Peace Strategy Trainer")

conflict_input = st.text_area("Describe the conflict (small-scale, Indian Constitution relevant):", height=100)

if "day" not in st.session_state:
    st.session_state.day = 1

if "history" not in st.session_state:
    st.session_state.history = []

if st.button("Start Simulation"):
    if not conflict_input.strip():
        st.warning("Please enter a conflict description.")
    else:
        st.session_state.day = 1
        prompt = generate_prompt(conflict_input, st.session_state.day)
        briefing = query_openrouter(prompt)
        st.session_state.history = [(st.session_state.day, briefing)]
        st.success(f"Day {st.session_state.day} briefing generated.")
        st.write(briefing)

if st.button("Simulate Next Day"):
    if not st.session_state.history:
        st.warning("Start the simulation first by clicking 'Start Simulation'.")
    else:
        st.session_state.day += 1
        prompt = generate_prompt(conflict_input, st.session_state.day)
        briefing = query_openrouter(prompt)
        st.session_state.history.append((st.session_state.day, briefing))
        st.success(f"Day {st.session_state.day} briefing generated.")
        st.write(briefing)

if st.session_state.history:
    st.subheader("Simulation History:")
    for day_num, text in st.session_state.history:
        st.markdown(f"**Day {day_num}:** {text}")




