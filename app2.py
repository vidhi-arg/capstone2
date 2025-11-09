import streamlit as st
import requests
import json

API_KEY = "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"
MODEL = "anthropic/claude-3-haiku"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# === UI ===
st.set_page_config(page_title="Case Decoder", layout="centered")
st.title(" Case Decoder")

# === Input Form ===
with st.form("legal_form"):
    country = st.selectbox("Select Country", ["India", "USA", "UK", "Canada"])
    issue = st.text_area("Describe the conflict (e.g. loudspeaker in village temple)")
    submitted = st.form_submit_button("Analyze")

# === On Submit ===
if submitted:
    if not issue.strip():
        st.error("Please describe the conflict.")
    else:
        with st.spinner("Analyzing the dispute..."):

            prompt = f"""
You are a legal AI assistant. Given a conflict and the country it occurred in, return only valid JSON.

Country: {country}
Conflict: {issue}

Return ONLY JSON in this format:
{{
  "classification": "Civil / Criminal / Constitutional / Cyber / Property / etc.",
  "predicted_ruling": "Summary of what the court is most likely to decide"
}}

Do not explain. Do not add commentary. Return only valid JSON. No markdown.
"""

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.3
            }

            try:
                res = requests.post(API_URL, headers=headers, json=payload)
                res_json = res.json()

                if "choices" not in res_json:
                    st.error("API Error:")
                    st.json(res_json)
                    st.stop()

                content = res_json["choices"][0]["message"]["content"]

                try:
                    data = json.loads(content)
                except json.JSONDecodeError:
                    st.error("Invalid JSON from model:")
                    st.code(content)
                    st.stop()

                # === DISPLAY ===
                st.text_input("Case Classification", value=data["classification"])
                st.text_area("Predicted Court Ruling", value=data["predicted_ruling"], height=150)

            except Exception as e:
                st.error(f"Something went wrong: {e}")















