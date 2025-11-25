
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
        with st.spinner("Analyzing..."):

            prompt = f"""
You are a legal AI assistant. Given a conflict and the country it occurred in, return only valid JSON.

Country: {country}
Conflict: {issue}

Return ONLY JSON in this format:
{{
  "classification": "Civil / Criminal / Constitutional / Cyber / Property / etc.",
  "article_or_section": "Relevant article or law name",
  "predicted_judgment": "What the court is most likely to decide",
  "punishment": "Expected punishment or fine if guilty"
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
                    st.error(" The model did NOT return valid JSON.")
                    st.code(content)
                    st.stop()

                # === Final Output (text boxes) ===
                st.subheader("Case Classification")
                st.text_area("", data["classification"], height=40)

                st.subheader("Relevant Article / Section")
                st.text_area("", data["article_or_section"], height=40)

                st.subheader("Predicted Judgment")
                st.text_area("", data["predicted_judgment"], height=70)

                st.subheader("Possible Punishment")
                st.text_area("", data["punishment"], height=60)

            except Exception as e:
                st.error(f"Something went wrong: {e}")
















