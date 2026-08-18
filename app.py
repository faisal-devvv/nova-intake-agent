import streamlit as st
from google import genai
from google.genai import types

# --- Page Configuration ---
st.set_page_config(page_title="NOVA Intake Governance Agent", layout="wide")

st.title("🚀 NOVA AI Intake & Risk Governance Portal")
st.markdown("Automated Technical Read, Compliance Screening, and KPI Tracking for Enterprise AI Proposals.")

# --- Secure API Key Initialization ---
try:
    if "GEMINI_API_KEY" in st.secrets:
        API_KEY = st.secrets["GEMINI_API_KEY"]
    else:
        API_KEY = "YOUR_LOCAL_API_KEY_HERE"  # Change this only if testing locally on your PC

    client = genai.Client(api_key=API_KEY)
except Exception as e:
    st.error(f"Failed to initialize Gemini Client: {e}")

# --- Compliance Policy Rule Table ---
COMPLIANCE_RULES = {
    "patient data": "CRITICAL RISK: PHI/Patient data must be encrypted at rest and in transit. Strict GDPR/HIPAA compliance required.",
    "phi": "CRITICAL RISK: PHI/Patient data must be encrypted at rest and in transit. Strict GDPR/HIPAA compliance required.",
    "clinical trial": "CRITICAL RISK: Clinical trial data is regulated PHI. Requires encryption, audit trail, and IRB-aligned access controls.",
    "financial data": "MODERATE RISK: Financial models require dual-authorization and audit logging.",
    "payment": "MODERATE RISK: Payment data falls under PCI-DSS; requires tokenization and restricted access.",
    "ai automation": "POLICY: Automated workflows must maintain human-in-the-loop review gates before execution.",
    "external dashboard": "CRITICAL RISK: External-facing dashboards handling regulated data must not be unencrypted; requires access-control review.",
    "employee data": "MODERATE RISK: HR/employee data requires role-based access and regional data-residency checks.",
}

def check_compliance_database(policy_topic: str) -> str:
    """Checks internal corporate policy and compliance risk rules for a given data-privacy topic."""
    topic = policy_topic.lower()
    for key, rule in COMPLIANCE_RULES.items():
        if key in topic or topic in key:
            return rule
    return "Standard enterprise policy applies: Ensure data privacy and logging."

# --- KPI Scoring Engine (computed from real proposal inputs) ---
def calculate_nova_kpis(project_complexity: str, manual_hours_per_week: float, team_size: int, avg_hourly_cost: float) -> str:
    """Calculates the six NOVA KPIs from user-supplied project parameters instead of static lookups."""
    complexity = project_complexity.lower()

    adoption_pct = 90 - (15 if complexity == "high" else 0)
    productivity_gain_hrs = manual_hours_per_week * team_size
    output_quality = "High" if complexity != "high" else "Moderate (needs pilot validation)"
    business_value = productivity_gain_hrs * avg_hourly_cost * 52  # annualized
    build_cost_estimate = 40000 if complexity == "high" else 15000
    return_ratio = round(business_value / build_cost_estimate, 2) if build_cost_estimate else 0
    stage_velocity_days = 14 if complexity == "high" else 7

    return (
        f"Adoption: {adoption_pct}% | "
        f"Productivity Gain: {productivity_gain_hrs:.0f} hrs/wk | "
        f"Output Quality: {output_quality} | "
        f"Business Value: ${business_value:,.0f}/yr | "
        f"Return Ratio: {return_ratio}x | "
        f"Stage Velocity: {stage_velocity_days} Days"
    )

enterprise_tools = [check_compliance_database, calculate_nova_kpis]

# --- User Input Section on the Web Page ---
st.subheader("📝 Submit a Business Proposal for Intake Screening")
proposal_input = st.text_area(
    "Enter project description or paste intake notes:",
    value="We want to build an automated python script that reads incoming clinical trial feedback PDFs, extracts patient names and reported side effects, and syncs them instantly to an unencrypted external dashboard used by our regional sales teams."
)

col1, col2, col3 = st.columns(3)
with col1:
    complexity_choice = st.selectbox("Project Complexity Estimate:", ["Medium", "High"])
with col2:
    manual_hours = st.number_input("Manual hours/week this replaces:", min_value=1.0, value=10.0, step=1.0)
with col3:
    team_size = st.number_input("Team size affected:", min_value=1, value=4, step=1)

avg_hourly_cost = st.slider("Avg loaded hourly cost ($):", min_value=20, max_value=150, value=60)

if st.button("Run AI Intake Committee Review"):
    if API_KEY == "YOUR_LOCAL_API_KEY_HERE" and "GEMINI_API_KEY" not in st.secrets:
        st.error("API Key not found! Please configure GEMINI_API_KEY in Streamlit Secrets or update your local fallback key.")
    else:
        with st.spinner("🧠 NOVA AI Agent is analyzing technical feasibility, compliance risks, and KPIs..."):
            try:
                # Create chat session with tools enabled using the flash model
                chat = client.chats.create(
                    model='gemini-3.6-flash',
                    config=types.GenerateContentConfig(
                        tools=enterprise_tools,
                        system_instruction=(
                            "You are the Lead Technical Architect for the NOVA AI Program. "
                            "When reviewing an intake proposal, you must always use your tools to check compliance risks "
                            "and calculate NOVA KPIs using the exact numeric inputs provided. Output a structured technical read containing: "
                            "1. Technical Feasibility, 2. Required Systems/APIs, 3. Compliance & Risk Flags, and 4. NOVA KPI Scorecard."
                        )
                    )
                )

                # Send proposal into the agent loop
                full_query = (
                    f"Proposal: {proposal_input} | Complexity Level: {complexity_choice} | "
                    f"Manual Hours/Week: {manual_hours} | Team Size: {team_size} | Avg Hourly Cost: ${avg_hourly_cost}"
                )
                response = chat.send_message(full_query)

                st.success("Review Complete!")
                st.markdown("### 📋 NOVA Intake Committee Report")
                st.markdown(response.text)

            except Exception as e:
                st.error(f"An error occurred: {e}")
