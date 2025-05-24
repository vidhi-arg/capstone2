import streamlit as st
import requests
import pandas as pd

st.set_page_config(page_title="NetrSim: Peace Strategy Trainer", layout="centered")

# Load your OpenRouter API key from Streamlit secrets
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
        "max_tokens": 250,
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

def generate_prompt(conflict_desc, day, analogy_mode):
    base_prompt = f"""
You are a conflict resolution AI focusing on small-scale conflicts in India related to the Constitution.
Conflict: {conflict_desc}

Day {day} briefing:
- What happened today (short 2 sentences).
- Suggest 1-2 simple solutions.
- Mention any relevant Indian constitutional legal clash.
- Summarize key stakeholders' impact in 2-3 bullet points.
- Keep text short and clear.

Provide output in this order separated by lines.

{'Also give a short historical analogy related to Indian history or constitution.' if analogy_mode else ''}
"""
    return base_prompt

def generate_timeline(history):
    timeline = "Timeline Simulation (Summary of daily briefings):\n"
    for day, briefing in history:
        timeline += f"Day {day}: {briefing.splitlines()[0]}\n"
    return timeline

def parse_stakeholders(text):
    # Simple heuristic: find lines with bullet points starting with '-', return list
    lines = text.splitlines()
    bullets = [line[2:].strip() for line in lines if line.strip().startswith("- ")]
    return bullets if bullets else ["No stakeholder info available"]

def conflict_outcome_cards():
    cards = {
        "Peaceful Resolution": "Conflict resolved amicably respecting constitutional rights.",
        "Moderate Escalation": "Tensions rise but controlled by legal actions and mediation.",
        "High Escalation": "Conflict escalates, requiring strong judicial and police intervention.",
    }
    return cards

# Initialize session state
if "day" not in st.session_state:
    st.session_state.day = 0
if "history" not in st.session_state:
    st.session_state.history = []
if "conflict_desc" not in st.session_state:
    st.session_state.conflict_desc = ""
if "analogy_mode" not in st.session_state:
    st.session_state.analogy_mode = False

st.title("NetrSim: Peace Strategy Trainer")

# Conflict input (disabled after start)
conflict_input = st.text_area(
    "Enter a small-scale conflict related to the Indian Constitution:",
    value=st.session_state.conflict_desc,
    height=100,
    disabled=st.session_state.day > 0,
)

st.checkbox(
    "Enable Historical Analogy Mode",
    value=st.session_state.analogy_mode,
    key="analogy_mode"
)

cols = st.columns(3)

with cols[0]:
    if st.button("Start Simulation"):
        if not conflict_input.strip():
            st.warning("Please enter a conflict description to start.")
        else:
            st.session_state.conflict_desc = conflict_input.strip()
            st.session_state.day = 1
            prompt = generate_prompt(st.session_state.conflict_desc, st.session_state.day, st.session_state.analogy_mode)
            briefing = query_openrouter(prompt)
            st.session_state.history = [(st.session_state.day, briefing)]
            st.success(f"Day {st.session_state.day} briefing generated.")

with cols[1]:
    if st.button("Simulate Next Day"):
        if st.session_state.day == 0:
            st.warning("Start the simulation first!")
        elif st.session_state.day >= 4:
            st.info("Simulation already ran for 4 days. Reset to start again.")
        else:
            st.session_state.day += 1
            prompt = generate_prompt(st.session_state.conflict_desc, st.session_state.day, st.session_state.analogy_mode)
            briefing = query_openrouter(prompt)
            st.session_state.history.append((st.session_state.day, briefing))
            st.success(f"Day {st.session_state.day} briefing generated.")

with cols[2]:
    if st.button("Reset Simulation"):
        st.session_state.day = 0
        st.session_state.history = []
        st.session_state.conflict_desc = ""
        st.session_state.analogy_mode = False
        st.experimental_rerun()

if st.session_state.history:
    st.subheader("Timeline Simulation")
    st.text(generate_timeline(st.session_state.history))

    st.subheader("Daily Briefings & Solutions")
    for day_num, text in st.session_state.history:
        st.markdown(f"**Day {day_num} Briefing:**")
        parts = text.split("\n\n")  # split by paragraphs for clarity
        for part in parts:
            st.markdown(part.strip())
        
        # Extract and show stakeholder impacts in table form (if any)
        stakeholders = parse_stakeholders(text)
        if stakeholders and stakeholders != ["No stakeholder info available"]:
            df = pd.DataFrame({"Stakeholder Impact": stakeholders})
            st.table(df)
        else:
            st.write("_No stakeholder impact info._")
        st.markdown("---")

    st.subheader("Legal Clash Mapping")
    # Scan history for "constitutional" or "legal clash" mentions (simple heuristic)
    legal_mentions = [text for _, text in st.session_state.history if "constitutional" in text.lower() or "legal clash" in text.lower()]
    if legal_mentions:
        st.write("Legal issues mentioned across simulation days:")
        for i, mention in enumerate(legal_mentions, 1):
            snippet = mention.split("\n")[0]
            st.markdown(f"{i}. {snippet}")
    else:
        st.write("_No explicit legal clash mentions found._")

    st.subheader("Conflict Outcome Cards")
    outcomes = conflict_outcome_cards()
    for title, desc in outcomes.items():
        st.markdown(f"**{title}**: {desc}")







