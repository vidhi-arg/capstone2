import streamlit as st
import requests

# Set Streamlit page config
st.set_page_config(page_title="NetrSim: Peace Strategy Trainer", layout="centered")

st.title("NetrSim - Peace Strategy Trainer")
st.write("Simulating strategic decision-making for peace and conflict scenarios.")

# Get the API key from secrets
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]

# Prompt input
user_prompt = st.text_area("Enter your scenario prompt:", "Generate a very simple conflict.")

if st.button("Simulate"):
    if not OPENROUTER_API_KEY:
        st.error("API key not found. Please check your Streamlit secrets.")
    else:
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }

        data = {
            "model": "mistralai/mixtral-8x7b-instruct",  # or other OpenRouter-supported model
            "messages": [
                {"role": "user", "content": user_prompt}
            ]
        }

        response = requests.post(
            "https://openrouter.ai/api/v1/chat/completions",
            headers=headers,
            json=data
        )

        if response.status_code == 200:
            result = response.json()
            st.markdown("### Response")
            st.write(result['choices'][0]['message']['content'])
        else:
            st.error(f"Failed to get a response. Status code: {response.status_code}")
            st.code(response.text)




