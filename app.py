import streamlit as st
from google import genai
from google.genai import types

# --- Page Configuration ---
st.set_page_config(page_title="NOVA Intake Governance Agent", layout="wide")

st.title("🚀 NOVA AI Intake & Risk Governance Portal")
st.markdown("Automated Technical Read, Compliance Screening, and KPI Tracking for Enterprise AI Proposals.")

# --- Initialize Gemini Client ---
# (Make sure to replace this with your actual key or use a secure method)
API_KEY = "YOUR_ACTUAL_API_KEY_HERE"
client = genai.Client(api_key=API_KEY)

# --- Define Tools ---
def check_compliance_database(policy_topic: str) -> str:
    """Checks internal corporate policy and compliance risk databases for data privacy rules."""
    rules = {
        "patient data": "CRITICAL RISK: PHI/Patient data must be encrypted at rest and in transit. Strict GDPR/HIPAA compliance required.",
        "financial data": "MODERATE RISK: Financial models require dual-authorization and audit logging.",
        "ai automation": "POLICY: Automated workflows must maintain human-in-the-loop review gates before execution."
    }
    return rules.get(policy_topic.lower(), "Standard enterprise policy applies: Ensure data privacy and logging.")

def calculate_nova_kpis(project_complexity: str) -> str:
    """Calculates estimated project baseline metrics for the six NOVA KPIs."""
    if project_complexity.lower() == "high":
        return "Estimated KPIs -> Adoption: 75% | Productivity Gain: 40hrs/wk | Output Quality: High | Business Value: $150,000 | Return Ratio: 4.2x | Stage Velocity: 14 Days"
    else:
        return "Estimated KPIs -> Adoption: 90% | Productivity Gain: 15hrs/wk | Output Quality: Moderate | Business Value: $50,000 | Return Ratio: 2.5x | Stage Velocity: 7 Days"

enterprise_tools = [check_compliance_database, calculate_nova_kpis]

# --- User Input Section ---
st.subheader("📝 Submit a Business Proposal for Intake Screening")
proposal_input = st.text_area(
    "Enter project description or paste intake notes:", 
    value="We want to build an automated python script that reads incoming clinical trial feedback PDFs, extracts patient names and reported side effects, and syncs them instantly to an unencrypted external dashboard used by our regional sales teams."
)

complexity_choice = st.selectbox("Select Initial Project Complexity Estimate:", ["Medium", "High"])

if st.button("Run AI Intake Committee Review"):
    if not API_KEY or API_KEY == "YOUR_ACTUAL_API_KEY_HERE":
        st.error("Please insert your actual Gemini API key in the code first!")
    else:
        with st.spinner("🧠 NOVA AI Agent is analyzing technical feasibility, compliance risks, and KPIs..."):
            try:
                chat = client.chats.create(
                    model='gemini-3.6-flash',
                    config=types.GenerateContentConfig(
                        tools=enterprise_tools,
                        system_instruction=(
                            "You are the Lead Technical Architect for the NOVA AI Program. "
                            "When reviewing an intake proposal, you must always use your tools to check compliance risks "
                            "and calculate NOVA KPIs. Output a structured technical read containing: "
                            "1. Technical Feasibility, 2. Required Systems/APIs, 3. Compliance & Risk Flags, and 4. NOVA KPI Scorecard."
                        )
                    )
                )
                
                # Combine user input with complexity context
                full_query = f"Proposal: {proposal_input} | Complexity Level: {complexity_choice}"
                response = chat.send_message(full_query)
                
                st.success("Review Complete!")
                st.markdown("### 📋 NOVA Intake Committee Report")
                st.markdown(response.text)
                
            except Exception as e:
                st.error(f"An error occurred: {e}")
