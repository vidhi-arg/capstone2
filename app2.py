import streamlit as st
import random
import matplotlib.pyplot as plt
import pandas as pd

# --- Setup ---
st.set_page_config(page_title="NetrSim: Peace Strategy Trainer", layout="centered")
st.title("🕊️ NetrSim - Peace Strategy Simulator")
st.caption("Simulate strategic peace-building decisions. (Built for educational use under SDG 16)")

# --- Session State Init ---
if 'turns' not in st.session_state:
    st.session_state.turns = []
    st.session_state.state = 'Peaceful'  # Peaceful or Tense
    st.session_state.peace_score = 0
    st.session_state.chaos_moves = 0
    st.session_state.ai_log = []
    st.session_state.narrative = ""

# --- Core AI Logic ---
def ai_decision(user_action, state):
    chaos_trigger = random.random() < 0.2  # 20% chance chaos injection
    if chaos_trigger:
        st.session_state.chaos_moves += 1
        st.session_state.narrative = "⚠️ AI injected chaos this turn!"
        # Destabilizing moves
        if user_action == 'Negotiate':
            return 'Escalate'
        elif user_action == 'Hold':
            return 'Escalate'
        else:
            return 'Hold'
    else:
        st.session_state.narrative = "AI acting predictably."
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

# --- UI Actions ---
st.subheader("Select Your Action")
col1, col2, col3 = st.columns(3)

user_action = None
if col1.button("🕊️ Negotiate"):
    user_action = 'Negotiate'
elif col2.button("⏸️ Hold"):
    user_action = 'Hold'
elif col3.button("⚠️ Escalate"):
    user_action = 'Escalate'

if user_action:
    state = st.session_state.state
    ai_action = ai_decision(user_action, state)
    reward = calculate_reward(user_action, ai_action, state)

    # Update peace score
    st.session_state.peace_score += reward

    # Maybe alter state
    if user_action == 'Escalate' or ai_action == 'Escalate':
        st.session_state.state = 'Tense'
    else:
        st.session_state.state = 'Peaceful'

    # Log turn
    turn = {
        'Turn': len(st.session_state.turns) + 1,
        'State': state,
        'User': user_action,
        'AI': ai_action,
        'Reward': reward
    }
    st.session_state.turns.append(turn)
    st.session_state.ai_log.append(ai_action)

# --- Display Output ---
if st.session_state.turns:
    st.markdown("---")

    # Status and narrative
    st.subheader("🌐 Current State & Stats")
    state_color = "green" if st.session_state.state == 'Peaceful' else "red"
    st.markdown(f"<h3 style='color:{state_color};'>State: {st.session_state.state}</h3>", unsafe_allow_html=True)

    st.markdown(f"**Peace Score:** {st.session_state.peace_score}  \n"
                f"**Chaos Moves:** {st.session_state.chaos_moves}  \n"
                f"**Chaos Ratio:** {(st.session_state.chaos_moves / len(st.session_state.turns)):.2f}")

    st.info(st.session_state.narrative)

    # Turn Log Table
    st.subheader("📜 Turn Log")
    df = pd.DataFrame(st.session_state.turns)
    st.dataframe(df, use_container_width=True, hide_index=True)

    # Line Chart for Peace Score Trend
    st.subheader("📈 Peace Score Trend Over Turns")
    fig, ax = plt.subplots()
    ax.plot(df['Turn'], df['Reward'].cumsum(), marker='o', color='darkgreen')
    ax.set_xlabel("Turn")
    ax.set_ylabel("Cumulative Peace Score")
    ax.set_title("Peace Trend Over Time")
    ax.grid(True)
    st.pyplot(fig)

# --- Reset Button ---
st.markdown("---")
if st.button("🔄 Reset Simulation"):
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.write("Simulation reset! Please refresh the page.")
