import streamlit as st
import requests
import random
import matplotlib.pyplot as plt
import pandas as pd

# Load API key from secrets.toml
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]

API_URL = "https://openrouter.ai/v1/chat/completions"
MODEL_ID = "meta-llama/llama-4-maverick:free"

# Headers for OpenRouter API request
headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

# Initialize session state variables for simulation
if "turns" not in st.session_state:
    st.session_state.turns = []
    st.session_state.state = "Peaceful"
    st.session_state.peace_score = 0
    st.session_state.chaos_moves = 0

st.set_page_config(page_title="NetrSim: Indian Constitution Conflict Simulator", layout="centered")
st.title(" NetrSim - Indian Constitution Conflict Simulator")
st.caption("Simulate strategic peace-building decisions referencing Indian Constitution principles.")

# Predefined simple conflicts inspired by Indian constitutional challenges
default_conflicts = [
    "Dispute over local water resources affecting farmers.",
    "Community disagreement on religious festival timings.",
    "Conflict regarding reservation policies in local employment.",
    "Tension due to language preference in school medium.",
    "Disagreement over land use for a public project."
]

user_scenario = st.text_area(
    "Describe the issue/conflict you'd like strategic suggestions for:",
    value=random.choice(default_conflicts),
    height=120
)

def query_openrouter(prompt_text):
    # OpenRouter chat completion payload
    payload = {
        "model": MODEL_ID,
        "messages": [
            {
                "role": "user",
                "content": prompt_text
            }
        ],
        "temperature": 0.7,
        "max_tokens": 300
    }
    response = requests.post(API_URL, headers=headers, json=payload)
    if response.status_code == 200:
        result = response.json()
        return result["choices"][0]["message"]["content"]
    else:
        return f"Error {response.status_code}: {response.text}"

st.subheader(" Conflict Scenario Input")

if st.button(" Generate Strategy Suggestions") and user_scenario.strip():
    with st.spinner("Generating strategic suggestions..."):
        prompt = (
            f"As an expert in Indian Constitution and conflict resolution, "
            f"suggest 3 possible actions (Negotiate, Hold, Escalate) for this conflict and predict likely outcomes:\n\n"
            f"Conflict: {user_scenario}"
        )
        action_suggestions = query_openrouter(prompt)
        st.markdown("###  Suggested Strategic Approaches")
        st.info(action_suggestions)
else:
    st.info("Enter a conflict and click the button to get strategic suggestions.")

# Core AI decision logic simulating the opponent's move
def ai_decision(user_action):
    chaos_trigger = random.random() < 0.2  # 20% chance to inject chaos
    if chaos_trigger:
        st.session_state.chaos_moves += 1
        if user_action == "Negotiate":
            return "Escalate"
        elif user_action == "Hold":
            return "Escalate"
        else:
            return "Hold"
    if user_action == "Negotiate":
        return "Negotiate"
    elif user_action == "Escalate":
        return "Negotiate"
    else:
        return "Hold"

# Reward logic tuned to peace-building outcomes based on Indian values
def calculate_reward(user, ai):
    if user == ai == "Negotiate":
        return 3
    elif user == "Hold" and ai == "Negotiate":
        return 2
    elif user == "Escalate" and ai == "Negotiate":
        return 1
    elif user == ai:
        return -1
    else:
        return 0

st.subheader(" Simulate Your Action")
col1, col2, col3 = st.columns(3)

user_action = None
if col1.button(" Negotiate"):
    user_action = "Negotiate"
elif col2.button(" Hold"):
    user_action = "Hold"
elif col3.button(" Escalate"):
    user_action = "Escalate"

if user_action:
    ai_action = ai_decision(user_action)
    reward = calculate_reward(user_action, ai_action)
    st.session_state.peace_score += reward
    # Update overall state based on escalations
    if user_action == "Escalate" or ai_action == "Escalate":
        st.session_state.state = "Tense"
    else:
        st.session_state.state = "Peaceful"
    turn = {
        "Turn": len(st.session_state.turns) + 1,
        "State": st.session_state.state,
        "User Action": user_action,
        "AI Action": ai_action,
        "Reward": reward,
    }
    st.session_state.turns.append(turn)

# Show turn log and peace score graph
if st.session_state.turns:
    st.subheader(" Turn Log")
    df = pd.DataFrame(st.session_state.turns)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader(" Peace Score & Chaos Ratio")
    col1, col2 = st.columns(2)
    col1.metric("Peace Score", st.session_state.peace_score)
    chaos_ratio = (
        st.session_state.chaos_moves / len(st.session_state.turns)
        if st.session_state.turns
        else 0
    )
    col2.metric("Chaos Ratio", f"{chaos_ratio:.2f}")

    st.subheader(" Peace Trend Over Time")
    fig, ax = plt.subplots()
    ax.plot(df["Turn"], df["Reward"].cumsum(), label="Cumulative Peace Score", color="green")
    ax.set_xlabel("Turn")
    ax.set_ylabel("Peace Score")
    ax.set_title("Peace Score Over Time")
    ax.grid(True)
    st.pyplot(fig)

# Reset simulation button
st.markdown("---")
if st.button(" Reset Simulation"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()





