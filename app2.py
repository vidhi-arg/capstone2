import streamlit as st
import requests
import random
import matplotlib.pyplot as plt
import pandas as pd

# --- Config ---
st.set_page_config(page_title="NetrSim: Peace Strategy Trainer", layout="centered")
st.title(" NetrSim - Peace Strategy Simulator")
st.caption("Simulate strategic peace-building decisions. Built under SDG 16")

# --- Secrets and API Setup ---
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
API_URL = "https://openrouter.ai/api/v1/chat/completions"

headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# --- Session State Initialization ---
if 'turns' not in st.session_state:
    st.session_state.turns = []
    st.session_state.state = 'Peaceful'
    st.session_state.peace_score = 0
    st.session_state.chaos_moves = 0
    st.session_state.ai_log = []

# --- User Scenario Input ---
st.subheader(" Conflict Scenario Input")
user_scenario = st.text_area("Describe the issue/conflict you'd like strategic suggestions for:")

action_suggestions = ""

if st.button(" Generate Strategy Suggestions") and user_scenario.strip():
    with st.spinner("Generating suggestions..."):
        payload = {
            "model": "openai/gpt-4o-mini",
            "messages": [
                {"role": "system", "content": "You are a strategic peace-building assistant."},
                {"role": "user", "content": f"Conflict: {user_scenario}\nSuggest 3 possible actions (Negotiate, Hold, Escalate) and predict likely outcomes."}
            ]
        }
        response = requests.post(API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            data = response.json()
            action_suggestions = data["choices"][0]["message"]["content"]
        else:
            action_suggestions = f"Failed to get a response. Status code: {response.status_code}\n{response.text}"

    st.markdown("###  Suggested Strategic Approaches")
    st.info(action_suggestions)

# --- AI Decision Logic ---
def ai_decision(user_action, state):
    chaos_trigger = random.random() < 0.2
    if chaos_trigger:
        st.session_state.chaos_moves += 1
        if user_action == 'Negotiate':
            return 'Escalate'
        elif user_action == 'Hold':
            return 'Escalate'
        else:
            return 'Hold'
    if user_action == 'Negotiate':
        return 'Negotiate'
    elif user_action == 'Escalate':
        return 'Negotiate'
    else:
        return 'Hold'

# --- Reward Calculation ---
def calculate_reward(user, ai, state):
    if user == ai == 'Negotiate':
        return 2
    elif user == 'Hold' and ai == 'Negotiate':
        return 2
    elif user == 'Escalate' and ai == 'Negotiate':
        return 2
    elif user == ai:
        return -1
    else:
        return 1

# --- User Actions ---
st.subheader("🎮 Simulate Your Action")
col1, col2, col3 = st.columns(3)
user_action = None
if col1.button(" Negotiate"):
    user_action = 'Negotiate'
elif col2.button(" Hold"):
    user_action = 'Hold'
elif col3.button(" Escalate"):
    user_action = 'Escalate'

if user_action:
    state = st.session_state.state
    ai_action = ai_decision(user_action, state)
    reward = calculate_reward(user_action, ai_action, state)
    st.session_state.peace_score += reward
    if user_action == 'Escalate' or ai_action == 'Escalate':
        st.session_state.state = 'Tense'
    else:
        st.session_state.state = 'Peaceful'
    turn = {
        'Turn': len(st.session_state.turns) + 1,
        'State': state,
        'User': user_action,
        'AI': ai_action,
        'Reward': reward
    }
    st.session_state.turns.append(turn)
    st.session_state.ai_log.append(ai_action)

# --- Display Turn Log and Stats ---
if st.session_state.turns:
    st.subheader(" Turn Log")
    df = pd.DataFrame(st.session_state.turns)
    st.dataframe(df, use_container_width=True, hide_index=True)
    
    st.markdown("---")
    st.subheader(" Peace Score & Chaos Ratio")
    col1, col2 = st.columns(2)
    col1.metric("Peace Score", st.session_state.peace_score)
    chaos_ratio = st.session_state.chaos_moves / len(st.session_state.turns) if st.session_state.turns else 0
    col2.metric("Chaos Ratio", f"{chaos_ratio:.2f}")
    
    st.subheader(" Peace Trend")
    fig, ax = plt.subplots()
    ax.plot(df['Turn'], df['Reward'].cumsum(), label='Cumulative Peace Score', color='green')
    ax.set_xlabel("Turn")
    ax.set_ylabel("Score")
    ax.set_title("Peace Score Over Time")
    ax.grid(True)
    st.pyplot(fig)

# --- Reset Button ---
st.markdown("---")
if st.button(" Reset Simulation"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()



