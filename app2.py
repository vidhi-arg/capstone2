import streamlit as st
import requests

st.set_page_config(page_title="NetrSim", layout="centered")

# Load API Key
OPENROUTER_API_KEY = st.secrets["openrouter"]["api_key"]

# Endpoint and headers
API_URL = "https://openrouter.ai/api/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {OPENROUTER_API_KEY}",
    "Content-Type": "application/json"
}

def query_openrouter(prompt):
    payload = {
        "model": "meta-llama/llama-3-tuned:free",
        "messages": [
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.7,
        "max_tokens": 250
    }

    try:
        response = requests.post(API_URL, headers=headers, json=payload)
    except Exception as e:
        st.error(f"Request failed: {e}")
        return None

    st.write(f"Status Code: {response.status_code}")  # Show status code

    if response.status_code != 200:
        st.error(f"Failed to fetch response: {response.text}")
        return None

    try:
        result = response.json()
        return result['choices'][0]['message']['content']
    except Exception as e:
        st.error(f"JSON Decode Failed: {e}")
        st.text("Raw response:")
        st.text(response.text)
        return None

# Streamlit UI
st.title("🧠 NetrSim: Conflict Scenario Generator")
st.markdown("Generate a **simple Indian Constitution-based conflict** for simulation.")

if st.button("🎯 Generate Conflict"):
    prompt = (
        "Generate a very simple conflict scenario based on the Indian Constitution. "
        "It should involve a disagreement about fundamental rights or duties between two citizens or a citizen and a local authority. "
        "Keep it suitable for a school-level simulation. No violence or politics."
    )
    conflict = query_openrouter(prompt)
    if conflict:
        st.subheader("🧩 Conflict Scenario:")
        st.write(conflict)
