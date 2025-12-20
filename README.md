# Sentinel-LoL: ML-Based "Living off the Land" Detection Engine

1. Project Overview
**Sentinel-LoL** is a behavioral security tool designed to detect **Living off the Land (LotL)** attacks—a technique where attackers use legitimate system tools (like PowerShell, Certutil, or WMI) to perform malicious actions. 

Since these tools are "trusted," traditional antivirus often misses them. This project uses **Unsupervised Machine Learning** to identify anomalies in command-line behavior that indicate a potential breach.

2. Key Features
* **Behavioral Anomaly Detection:** Uses an **Isolation Forest** model to find "weird" commands based on pattern rather than just signatures.
* **Entropy Analysis:** Calculates **Shannon Entropy** to detect obfuscated or Base64-encoded payloads commonly used in fileless malware.
* **Feature Engineering:** Extracts text-based features (length, special character density, and keyword flags) to feed the ML pipeline.
* **Safe Execution:** Built and tested in a **containerized GitHub Codespaces environment** to ensure system isolation.

3. The Architecture


1.  **Data Ingestion:** Reads process logs containing `command_line` strings.
2.  **Feature Extraction:** Converts raw text into numerical data (Entropy, Length, Keyword weight).
3.  **ML Inference:** The **Isolation Forest** algorithm isolates anomalies that deviate from the "normal" training set.
4.  **Triage:** Outputs a "Threat" or "Normal" status for each process event.

4. Tech Stack
* **Language:** Python 3.x
* **AI/ML:** Scikit-learn (Isolation Forest), NumPy
* **Data Analysis:** Pandas
* **Environment:** GitHub Codespaces / Docker

5. How to Run
a. **Clone the repository:**
   ```bash
   git clone [https://github.com/YOUR_USERNAME/Sentinel-LoL.git](https://github.com/YOUR_USERNAME/Sentinel-LoL.git)
   cd Sentinel-LoL
b. Install Dependencies: pip install pandas scikit-learn numpy
c. Run the Detector: python src/detector.py
