import streamlit as st
import requests
import json

API_KEY = "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" 
MODEL = "anthropic/claude-3-haiku" 
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# === UI ===
st.set_page_config(page_title="Legal AI Assistant", layout="centered")
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
  "predicted_ruling": "Summary of what the court is most likely to decide",
  "article": "Relevant article or law",
  "cases": [
    {{
      "name": "Case name",
      "year": 2000,
      "ruling": "What the court decided in this case"
    }},
    {{
      "name": "...",
      "year": 2005,
      "ruling": "..."
    }},
    {{
      "name": "...",
      "year": 2017,
      "ruling": "..."
    }}
  ],
  "escalation_paths": ["...", "..."],
  "people_involved": {{
    "complainant": "...",
    "defendant": "...",
    "authority": "..."
  }},
  "suggested_actions": ["...", "..."]
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
                "temperature": 0.4
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

                # === NEW TOP SECTIONS ===
                st.subheader("Case Classification")
                st.code(data["classification"])

                st.subheader("Predicted Court Ruling")
                st.code(data["predicted_ruling"])

                # === Existing Sections ===
                st.subheader("Relevant Article or Law")
                st.code(data["article"])

                st.subheader(" Past Court Cases & Rulings")
                for case in data["cases"]:
                    st.markdown(f"**{case['name']}** ({case['year']})")
                    st.write(f"**Ruling:** {case['ruling']}")

                st.subheader("Escalation Paths")
                for path in data["escalation_paths"]:
                    st.markdown(f"- {path}")

                st.subheader("👥 People Involved")
                for role, person in data["people_involved"].items():
                    st.markdown(f"- **{role.title()}**: {person}")

                st.subheader("Suggested Actions")
                for step in data["suggested_actions"]:
                    st.markdown(f"- {step}")

            except Exception as e:
                st.error(f"Something went wrong: {e}")














