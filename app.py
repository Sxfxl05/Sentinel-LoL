import streamlit as st
import requests
import json

# Page configuration
st.set_page_config(
    page_title="Sentinel-LotL | Threat Engine UI",
    page_icon="🛡️",
    layout="wide"
)

# Replace this with your actual Render API base URL
# Change this line in app.py:
API_URL = "https://sentinel-lotl-api.onrender.com"

# Custom CSS for dark cybersecurity theme
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
    }
    .stButton>button {
        width: 100%;
        background-color: #00e676;
        color: #000;
        font-weight: bold;
        border-radius: 6px;
    }
    .stButton>button:hover {
        background-color: #00c853;
        color: #fff;
    }
    </style>
""", unsafe_allow_html=True)

# Header Section
st.title("🛡️ Sentinel-LotL Threat Detection Engine")
st.caption("AI-Powered Living-off-the-Land (LotL) Fileless Malware Analyzer")
st.markdown("---")

# Sidebar for System Status & Config
with st.sidebar:
    st.header("⚙️ Engine Status")
    
    # Live Health Check Call
    try:
        health_resp = requests.get(f"{API_URL}/", timeout=5)
        if health_resp.status_code == 200:
            st.success("API Status: Connected & Online 🟢")
            st.json(health_resp.json())
        else:
            st.warning(f"API Status: Responded with HTTP {health_resp.status_code}")
    except Exception as e:
        st.error("API Status: Disconnected 🔴")
        st.caption("Ensure your Render FastAPI service is running.")

    st.markdown("---")
    st.markdown("### Model Details")
    st.write("**Architecture:** Isolation Forest + Shannon Entropy")
    st.write("**Target:** Obfuscated PowerShell / Cmd Logs")

# Main Content Layout
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🔍 Analyze Suspicious Telemetry / Logs")
    
    # Preset sample logs for rapid testing during interviews
    preset = st.selectbox(
        "Select a Test Preset (or type custom below):",
        [
            "Custom Input",
            "Benign: Get-Process | Where-Object {$_.CPU -gt 10}",
            "Malicious LotL: powershell -e aQBlAHgAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApA=="
        ]
    )

    if preset == "Benign: Get-Process | Where-Object {$_.CPU -gt 10}":
        default_log = "Get-Process | Where-Object {$_.CPU -gt 10}"
    elif preset.startswith("Malicious LotL"):
        default_log = "powershell -e aQBlAHgAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApA=="
    else:
        default_log = ""

    log_input = st.text_area("PowerShell / Command Execution Log:", value=default_log, height=120, placeholder="Paste PowerShell execution logs here...")

    analyze_btn = st.button("Run Threat Analysis")

with col2:
    st.subheader("📊 Detection Results")
    
    if analyze_btn:
        if not log_input.strip():
            st.warning("Please enter a log or command to analyze.")
        else:
            with st.spinner("Evaluating via Isolation Forest model..."):
                try:
                    # Send payload to your Render REST API endpoint
                    response = requests.post(
                        f"{API_URL}/predict",
                        json={"log_event": log_input},
                        headers={"Content-Type": "application/json"},
                        timeout=10
                    )
                    
                    if response.status_code == 200:
                        result = response.json()
                        is_anomaly = result.get("is_anomaly", False)
                        confidence = result.get("confidence_score", 0.0)

                        st.metric("Threat Confidence", f"{confidence * 100:.1f}%")

                        if is_anomaly:
                            st.error("🚨 **ALERT: Anomaly / LotL Execution Detected!**")
                            st.markdown("""
                            * **Action Recommended:** Quarantine Endpoint / Review Parent Process
                            * **Flag:** Base64 Obfuscation / High Shannon Entropy
                            """)
                        else:
                            st.success("✅ **CLEAN: Normal System Execution**")

                        with st.expander("Raw API JSON Payload"):
                            st.json(result)

                    else:
                        st.error(f"Error from API (HTTP {response.status_code}):")
                        st.text(response.text)

                except Exception as ex:
                    st.error(f"Failed to reach FastAPI backend: {ex}")
    else:
        st.info("Paste a log on the left and click **Run Threat Analysis** to evaluate.")
