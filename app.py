import streamlit as st
import requests

# Page setup
st.set_page_config(
    page_title="Sentinel-LotL Engine",
    page_icon="🛡️",
    layout="wide"
)

# Render API Base URL (NO trailing slash)
API_URL = "https://sentinel-lotl-api.onrender.com"

st.title("🛡️ Sentinel-LotL Threat Detection Engine")
st.caption("AI-Powered Living-off-the-Land Fileless Malware Analyzer")
st.markdown("---")

# Sidebar Status
with st.sidebar:
    st.header("⚙️ Engine Status")
    try:
        health_resp = requests.get(f"{API_URL}/", timeout=5)
        if health_resp.status_code == 200:
            st.success("API Status: Connected 🟢")
            st.json(health_resp.json())
        else:
            st.warning(f"HTTP {health_resp.status_code}")
    except Exception as e:
        st.error("API Offline 🔴")

# Main Interface
col1, col2 = st.columns([3, 2])

with col1:
    st.subheader("🔍 Analyze Telemetry Logs")
    preset = st.selectbox(
        "Select Test Sample:",
        [
            "Custom Input",
            "Benign: Get-Process | Where-Object {$_.CPU -gt 10}",
            "Malicious: powershell -e aQBlAHgAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApA=="
        ]
    )

    if preset == "Benign: Get-Process | Where-Object {$_.CPU -gt 10}":
        default_log = "Get-Process | Where-Object {$_.CPU -gt 10}"
    elif preset.startswith("Malicious"):
        default_log = "powershell -e aQBlAHgAKABOAGUAdwAtAE8AYgBqAGUAYwB0ACAATgBlAHQALgBXAGUAYgBDAGwAaQBlAG4AdAApA=="
    else:
        default_log = ""

    log_input = st.text_area("Command Execution Log:", value=default_log, height=120)
    analyze_btn = st.button("Run Threat Analysis")

with col2:
    st.subheader("📊 Results")
    if analyze_btn:
        if not log_input.strip():
            st.warning("Please enter a log string.")
        else:
            with st.spinner("Analyzing log..."):
                try:
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

                        st.metric("Threat Score", f"{confidence * 100:.1f}%")

                        if is_anomaly:
                            st.error("🚨 ALERT: Anomaly / LotL Execution Detected!")
                        else:
                            st.success("✅ CLEAN: Normal Execution")

                        with st.expander("Raw API Response"):
                            st.json(result)
                    else:
                        st.error(f"API Error (HTTP {response.status_code})")

                except Exception as ex:
                    st.error(f"Connection failed: {ex}")
