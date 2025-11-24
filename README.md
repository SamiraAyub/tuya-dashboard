⚡ IoT-Based Real-Time Energy Monitoring Dashboard ⚡
Built with Streamlit • Plotly • Python

📌 Overview

This project is an IoT-based real-time energy monitoring system that reads Voltage, Current, Power, and Energy (kWh) from a smart plug/sensor and visualises it on a dynamic web dashboard built using Streamlit.

It provides:

📟 Real-time electrical gauges

📈 Trend graphs for voltage, current, and power

🧮 Cost estimation (BDT/kWh)

⏱️ Auto-refreshing dashboard

📥 Downloadable CSV & summary reports

📘 Recent data logs

⚙️ Power factor & apparent power calculation

The project is ideal for Green Computing, IoT analytics, smart home systems, and energy optimisation.

🚀 Features
🔴 Real-Time Monitoring

- Voltage (V)

- Current (A)

- Power (W)

- Energy consumption (kWh)

📊 Charts

- Power over time

- Voltage trend

- Current trend

- Energy + Cost + Power combined graph

🧠 Advanced Metrics

- Apparent Power (VA)

- Power Factor

- Estimated cost per kWh

🛠️ Tools

- Streamlit frontend

- Plotly for graphs

- Pandas for processing

- Auto-refresh without infinite loops

- CSV-based data storage

📂 Project Structure
📁 IoT-Energy-Dashboard/
│
├── dashboard.py          # Main Streamlit app
├── energy_log.csv        # Real-time data log (sensor data)
├── README.md             # Documentation
└── requirements.txt      # Python dependencies

🧰 Installation & Setup
1️⃣ Clone the Repository
git clone https://github.com/yourusername/IoT-Energy-Dashboard.git
cd IoT-Energy-Dashboard

2️⃣ Create Virtual Environment (Recommended)
python -m venv venv


Activate:

Windows:

venv\Scripts\activate


Mac/Linux:

source venv/bin/activate

3️⃣ Install Dependencies
pip install -r requirements.txt


Required packages:

streamlit
pandas
plotly
streamlit-autorefresh

4️⃣ Run the Dashboard Locally
streamlit run dashboard.py


Then open:

http://localhost:8501

📡 Deploy on Streamlit Cloud

Upload your code to GitHub

Go to: https://share.streamlit.io

Create a new app

Select your repo + dashboard.py

Deploy 🚀

Make sure your repo includes:

requirements.txt

energy_log.csv (or a placeholder file)

📑 Data Format

The dashboard expects a CSV file with the following columns:

Column	Description
Timestamp	Date & time of reading
Voltage (V)	Voltage measurement
Current (A)	Current measurement
Power (W)	Power consumption
Energy (kWh)	Cumulative energy usage
Status	On/Off state (optional)

Example:

Timestamp,Voltage (V),Current (A),Power (W),Energy (kWh),Status
2025-11-17 10:00:01,220,0.45,99.0,0.032,ON

⚙️ How Auto-Refresh Works

Streamlit Cloud does not support infinite loops, so we use:

from streamlit_autorefresh import st_autorefresh

st_autorefresh(interval=5000, key="refresh")


This keeps the dashboard updated in the cloud safely.

📥 Downloadable Reports

The dashboard provides:

- Full dataset (CSV)

- Summary report (TXT)

- Total energy

- Cost estimation

- Peak voltage/current/power

🛡️ Safety Notes

- Ensure smart plug is properly insulated

- Use rated extension cables

- Do not exceed load current of the plug

- Avoid open wiring

🧩 Future Improvements

- MQTT live streaming instead of CSV

- Multi-device analytics

- Mobile PWA version

- AI-based anomaly detection

- Appliance auto-control (ON/OFF automation)



👤 Author
Afia Ayub Samirah
Email: afia.a.samirah@gmail.com
