import streamlit as st
import random
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(page_title="NetrSim 2.0 - Chaos Under the Radar", layout="centered")
st.title((" NetrSim 2.0 - Peace Strategy Simulator (Under the Radar)")
st.caption("Train peace strategies, while AI secretly learns to inject chaos...")

# Initialize session state
if 'turns' not in st.session_state:
    st.session_state.turns = []
    st.session_state.state = 'Peaceful'  # Peaceful or Tense
    st.session_state.peace_score = 0
    st.session_state.chaos_moves = 0
    st.session_state.user_history = []  # Track user moves
    st.session_state.ai_history = []
    st.session_state.user_profile = {'Negotiate':0, 'Hold':0, 'Escalate':0}  # Counts user moves
    st.session_state.chaos_schedule = []  # When chaos moves injected

# Basic actions
ACTIONS = ['Negotiate', 'Hold', 'Escalate']

def update_user_profile(user_action):
    st.session_state.user_profile[user_action] += 1

def user_preference():
    profile = st.session_state.user_profile
    return max(profile, key=profile.get)

def ai_decision(user_action, state):
    update_user_profile(user_action)

    chaos_chance = 0.1 + 0.3 * (st.session_state.user_profile[user_action] / max(1, sum(st.session_state.user_profile.values())))

    peaceful_turns = 0
    for t in reversed(st.session_state.turns):
        if t['State']=='Peaceful':
            peaceful_turns += 1
        else:
            break
    if peaceful_turns > 4:
        chaos_chance += 0.2

    chaos_trigger = random.random() < chaos_chance

    if chaos_trigger:
        st.session_state.chaos_moves += 1
        st.session_state.chaos_schedule.append(len(st.session_state.turns)+1)
        if user_action == 'Negotiate':
            return 'Escalate'
        elif user_action == 'Hold':
            return random.choice(['Escalate', 'Hold'])
        else:
            return 'Hold'

    if user_action == 'Negotiate':
        return 'Negotiate' if random.random() > 0.3 else 'Hold'
    elif user_action == 'Hold':
        return 'Negotiate'
    else:
        return 'Negotiate'

def calculate_reward(user, ai):
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

def update_state(user_action, ai_action):
    if user_action == 'Escalate' or ai_action == 'Escalate':
        st.session_state.state = 'Tense'
    else:
        st.session_state.state = 'Peaceful'

st.subheader("Select Your Action")
cols = st.columns(len(ACTIONS))
user_action = None
for i, act in enumerate(ACTIONS):
    if cols[i].button(f"{act}"):
        user_action = act

if user_action:
    state = st.session_state.state
    ai_action = ai_decision(user_action, state)
    reward = calculate_reward(user_action, ai_action)

    st.session_state.peace_score += reward
    update_state(user_action, ai_action)

    turn = {
        'Turn': len(st.session_state.turns) + 1,
        'State': state,
        'User': user_action,
        'AI': ai_action,
        'Reward': reward
    }
    st.session_state.turns.append(turn)
    st.session_state.ai_history.append(ai_action)
    st.session_state.user_history.append(user_action)

if st.session_state.turns:
    st.subheader(" Turn Log")
    df = pd.DataFrame(st.session_state.turns)
    st.dataframe(df, use_container_width=True, hide_index=True)

    st.markdown("---")
    st.subheader(" Peace Score & Hidden Chaos Meter")
    col1, col2 = st.columns(2)
    col1.metric("Peace Score", st.session_state.peace_score)
    chaos_ratio = st.session_state.chaos_moves / max(1, len(st.session_state.turns))
    col2.metric("Chaos Moves (Hidden Instability)", f"{chaos_ratio:.2f}")

    st.subheader(" Peace vs Chaos Trend")
    fig, ax = plt.subplots()
    ax.plot(df['Turn'], df['Reward'].cumsum(), label='Cumulative Peace Score', color='green')
    ax2 = ax.twinx()
    ax2.plot(df['Turn'], [1 if i+1 in st.session_state.chaos_schedule else 0 for i in range(len(df))], 
             label='Chaos Moves', color='red', linestyle='dotted')
    ax.set_xlabel("Turn")
    ax.set_ylabel("Peace Score", color='green')
    ax2.set_ylabel("Chaos Moves (1=yes)", color='red')
    ax.legend(loc='upper left')
    ax2.legend(loc='upper right')
    st.pyplot(fig)

st.markdown("---")
if st.button(" Reset Simulation"):
    for key in st.session_state.keys():
        del st.session_state[key]
    st.experimental_rerun()
