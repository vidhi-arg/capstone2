import streamlit as st
import requests
import json

# === OpenRouter API config ===
API_KEY = "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"
MODEL = "mistralai/mistral-7b-instruct"
API_URL = "https://openrouter.ai/api/v1/chat/completions"

# === UI ===
st.set_page_config(page_title="Legal AI Assistant")
st.title("🧾 Legal AI Assistant (with Rulings)")
st.markdown("Get relevant constitutional laws, court cases, rulings, and legal advice for small-town conflicts.")

# === Input Form ===
with st.form("legal_form"):
    country = st.selectbox("Select Country", ["India", "USA", "Canada", "UK"])
    issue = st.text_area("Describe the conflict in detail")
    submit = st.form_submit_button("Analyze")

# === On Submit ===
if submit:
    if not issue.strip():
        st.error("Please describe the issue.")
    else:
        with st.spinner("Analyzing..."):

            # === Updated Prompt ===
            prompt = f"""
You are a legal AI.

Given:
Country: {country}
Issue: {issue}

Return ONLY valid JSON in this exact format:
{{
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

NO extra commentary. NO markdown. Just valid JSON.
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

                    st.subheader("📜 Relevant Article")
                    st.code(data["article"])

                    st.subheader("📁 Past Court Cases & Rulings")
                    for case in data["cases"]:
                        st.markdown(f"**{case['name']}** ({case['year']})")
                        st.write(f"**Ruling:** {case['ruling']}")

                    st.subheader("⚠️ Escalation Paths")
                    for path in data["escalation_paths"]:
                        st.markdown(f"- {path}")

                    st.subheader("👥 People Involved")
                    for role, name in data["people_involved"].items():
                        st.markdown(f"- **{role.title()}**: {name}")

                    st.subheader("✅ Suggested Actions")
                    for step in data["suggested_actions"]:
                        st.markdown(f"- {step}")

            except Exception as e:
                st.error(f"Something went wrong: {e}")

















