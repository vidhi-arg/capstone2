import streamlit as st
import requests

st.set_page_config(page_title="NetrSim: Peace Strategy Trainer", layout="centered")

st.title("NetrSim - Peace Strategy Trainer")
st.write("Simulate a strategic scenario between groups or nations.")

# 🔐 Read the API key from secrets
try:
    OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]
except Exception as e:
    st.error("API key not found. Please add it in Streamlit secrets.")
    st.stop()

# UI to enter a prompt
user_prompt = st.text_area("Enter a simple conflict scenario:", "Generate a very simple conflict.")

if st.button("Simulate"):
    headers = {
        "Authorization": f"Bearer {OPENROUTER_API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mixtral-8x7b-instruct",
        "messages": [{"role": "user", "content": user_prompt}]
    }

    response = requests.post(
        "https://openrouter.ai/api/v1/chat/completions",
        headers=headers,
        json=data
    )

    if response.status_code == 200:
        result = response.json()
        st.markdown("### AI Response")
        st.write(result["choices"][0]["message"]["content"])
    else:
        st.error(f"Failed to get a response. Status code: {response.status_code}")
        st.code(response.text)




