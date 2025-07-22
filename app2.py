import streamlit as st
import requests
import os
import json

# === SETUP ===
API_KEY = "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"
MODEL = "openrouter/mistral-7b-instruct"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# === UI ===
st.set_page_config(page_title="Legal AI", layout="centered")
st.title(" Local Conflict → Legal Insight")

country = st.selectbox("Your Country", ["India", "USA", "Canada", "UK"])
issue = st.text_area("Describe the conflict ")
submit = st.button("Get Legal Breakdown")

# === PROCESS ===
if submit:
    if not issue.strip():
        st.error("Describe the issue.")
    else:
        with st.spinner("Contacting legal AI..."):
            prompt = f"""
You are a legal AI.

Given the following:
Country: {country}
Issue: {issue}

Return only valid JSON with:
{{
  "article": "Relevant law",
  "cases": [{{"name": "...", "year": 2000}}, {{...}}, {{...}}],
  "escalation_paths": ["...", "..."],
  "people_involved": {{
    "complainant": "...",
    "defendant": "...",
    "authority": "..."
  }},
  "suggested_actions": ["...", "..."]
}}
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
                out = res.json()
                msg = out["choices"][0]["message"]["content"]
                data = json.loads(msg)

                st.subheader("Relevant Article")
                st.code(data["article"])

                st.subheader("Cases")
                for c in data["cases"]:
                    st.markdown(f"- **{c['name']}** ({c['year']})")

                st.subheader("Escalation Paths")
                for step in data["escalation_paths"]:
                    st.markdown(f"- {step}")

                st.subheader("People Involved")
                for role, person in data["people_involved"].items():
                    st.markdown(f"- **{role.title()}**: {person}")

                st.subheader("Suggested Actions")
                for act in data["suggested_actions"]:
                    st.markdown(f"- {act}")

            except Exception as e:
                st.error(f"Something went wrong: {e}")

















