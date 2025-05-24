import streamlit as st
import requests
import random
import matplotlib.pyplot as plt
import pandas as pd

st.set_page_config(page_title="NetrSim: Peace Strategy Trainer", layout="centered")
st.title(" NetrSim - Peace Strategy Simulator")
st.caption("Simulate strategic peace-building decisions. Built under SDG 16")

# Load Cohere API token from secrets
COHERE_API_TOKEN = st.secrets["COHERE_API_TOKEN"]
COHERE_API_URL = "https://api.cohere.ai/generate"

headers = {
    "Authorization": f"Bearer {COHERE_API_TOKEN}",
    "Content-Type": "application/json"
}

# Initialize session state
if 'turns' not in st.session_state:
    st.session_state.turns = []
    st.session_state.state = 'Peaceful'
    st.session_state.peace_score = 0
    st.session_state.chaos_moves = 0
    st.session_state.ai_log = []

# User input
st.subheader(" Conflict Scenario Input")
user_scenario = st.text_area("Describe the issue/conflict you'd like strategic suggestions for:")

if st.button(" Generate Strategy Suggestions") and user_scenario:
    with st.spinner("Generating strategy suggestions..."):
        payload = {
            "model": "xlarge",
            "prompt": f"Conflict: {user_scenario}\nSuggest 3 possible actions (Negotiate, Hold, Escalate) and predict likely outcomes:",
            "max_tokens": 150,
            "temperature": 0.7,
            "k": 0,
            "stop_sequences": ["--"],
        }
        response = requests.post(COHERE_API_URL, headers=headers, json=payload)
        if response.status_code == 200:
            generated_text = response.json()['generations'][0]['text'].strip()
            st.markdown("###  Suggested Strategic Approaches")
            st.info(generated_text)
        else:
            st.error("Failed to get a response. Please check your token or try again later.")

# AI Decision Logic
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

# Reward Calculation
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

# User Actions
st.subheader(" Simulate Your Action")
col1, col2, col3 = st.columns(3)
user_action = None
if col1.button(" Negotiate"):
    user_action = 'Negotiate'
elif col2.button("⏸ Hold"):
    user_action = 'Hold'
elif col3.button("⚠ Escalate"):
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

# Display Outputs
if st.session_state.turns:
    st.subheader(" Turn Log")
    df = pd.DataFrame(st.session_state.turns)
    st.dataframe(df, use_container_width=True, hide_index=True)
    st.markdown("---")
    st.subheader(" Peace Score & Chaos Ratio")
    col1, col2 = st.columns(2)
    col1.metric("Peace Score", st.session_state.peace_score)
    col2.metric("Chaos Ratio", f"{st.session_state.chaos_moves / len(st.session_state.turns):.2f}")
    st.subheader(" Peace Trend")
    fig, ax = plt.subplots()
    ax.plot(df['Turn'], df['Reward'].cumsum(), label='Cumulative Peace Score', color='green')
    ax.set_xlabel("Turn")
    ax.set_ylabel("Score")
    ax.set_title("Peace Score Over Time")
    ax.grid(True)
    st.pyplot(fig)

# Reset button
st.markdown("---")
if st.button(" Reset Simulation"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()



