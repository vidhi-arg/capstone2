import streamlit as st
import requests
import json

# Config
API_KEY = st.secrets["OPENROUTER_API_KEY"]
MODEL = "mistralai/mistral-7b-instruct"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

st.set_page_config(page_title="Legal AI Assistant")
st.title(" Legal AI Assistant (OpenRouter)")
st.markdown("Get legal insight for village or small-town conflicts based on your country’s constitution and court history.")

# Input form
with st.form("input_form"):
    country = st.selectbox("Select Country", ["India", "USA", "Canada", "UK"])
    issue = st.text_area("Describe the conflict in detail")
    submit = st.form_submit_button("Analyze")

# Handle submit
if submit:
    if not issue.strip():
        st.error("Please describe the issue.")
    else:
        with st.spinner("Thinking like a lawyer..."):
            prompt = f"""
You are a legal AI.

Based on:
Country: {country}
Issue: {issue}

Return ONLY valid JSON in this format:
{{
  "article": "Relevant article/law here",
  "cases": [{{"name": "...", "year": 2020}}, {{...}}, {{...}}],
  "escalation_paths": ["...", "..."],
  "people_involved": {{
    "complainant": "...",
    "defendant": "...",
    "authority": "..."
  }},
  "suggested_actions": ["...", "..."]
}}
No extra text. No markdown. Just valid JSON.
"""

            headers = {
                "Authorization": f"Bearer {API_KEY}",
                "Content-Type": "application/json"
            }

            payload = {
                "model": MODEL,
                "messages": [{"role": "user", "content": prompt}],
                "temperature": 0.4
            }

            try:
                res = requests.post(API_URL, headers=headers, json=payload)
                res_json = res.json()

                if "choices" not in res_json:
                    st.error("API Error:")
                    st.json(res_json)
                else:
                    content = res_json["choices"][0]["message"]["content"]
                    try:
                        data = json.loads(content)
                    except:
                        st.error("The model did not return valid JSON.")
                        st.code(content)
                        st.stop()

                    st.subheader(" Relevant Article")
                    st.code(data["article"])

                    st.subheader(" Past Cases")
                    for case in data["cases"]:
                        st.markdown(f"- **{case['name']}** ({case['year']})")

                    st.subheader(" Escalation Paths")
                    for path in data["escalation_paths"]:
                        st.markdown(f"- {path}")

                    st.subheader(" People Involved")
                    for role, name in data["people_involved"].items():
                        st.markdown(f"- **{role.title()}**: {name}")

                    st.subheader(" Suggested Actions")
                    for step in data["suggested_actions"]:
                        st.markdown(f"- {step}")
            except Exception as e:
                st.error(f"Something went wrong: {e}")
















