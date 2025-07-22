import streamlit as st
import requests
import json

# === OpenRouter API config ===
API_KEY = "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"
MODEL = "mistralai/mistral-7b-instruct"

headers = {
    "Authorization": f"Bearer {API_KEY}",
    "Content-Type": "application/json"
}

# === UI ===
st.set_page_config(page_title="Legal AI Assistant", layout="centered")
st.title("🧾 Legal AI Assistant (with Rulings)")
st.markdown("Enter a conflict and receive relevant laws, past rulings, escalation steps, and legal advice.")

# === Input Form ===
with st.form("legal_form"):
    country = st.selectbox("Select Country", ["India", "USA", "Canada", "UK"])
    issue = st.text_area("Describe the conflict in detail (e.g. land dispute, loudspeaker, etc)")
    submitted = st.form_submit_button("Analyze")

# === Submit handler ===
if submitted:
    if not issue.strip():
        st.error("Please enter a valid description of the conflict.")
    else:
        with st.spinner("Contacting legal AI..."):

            # Prompt
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

No extra commentary. No markdown. Only return valid JSON.
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
                response = requests.post(API_URL, headers=headers, json=payload)

                if response.status_code != 200:
                    st.error("OpenRouter API Error:")
                    st.json(response.json())
                    st.stop()

                response_json = response.json()
                content = response_json["choices"][0]["message"]["content"]

                try:
                    data = json.loads(content)
                except json.JSONDecodeError:
                    st.error("Model output is not valid JSON. Here's what it returned:")
                    st.code(content)
                    st.stop()

                # === Display results ===
                st.subheader("📜 Relevant Article")
                st.code(data["article"])

                st.subheader("📁 Past Court Cases & Rulings")
                for case in data["cases"]:
                    st.markdown(f"**{case['name']}** ({case['year']})")
                    st.write(f"**Ruling:** {case['ruling']}")

                st.subheader("⚠️ Escalation Paths")
                for step in data["escalation_paths"]:
                    st.markdown(f"- {step}")

                st.subheader("👥 People Involved")
                for role, person in data["people_involved"].items():
                    st.markdown(f"- **{role.title()}**: {person}")

                st.subheader("✅ Suggested Actions")
                for action in data["suggested_actions"]:
                    st.markdown(f"- {action}")

            except Exception as e:
                st.error(f"Request failed: {e}")


















