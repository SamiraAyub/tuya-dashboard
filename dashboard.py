import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os

from streamlit_autorefresh import st_autorefresh

# -----------------------------------------------------------
# Streamlit Page Config
# -----------------------------------------------------------
st.set_page_config(page_title="Smart Plug Energy Dashboard", layout="wide")
CSV_FILE = "energy_log.csv"

# -----------------------------------------------------------
# Dashboard Header
# -----------------------------------------------------------
st.markdown(
    "<h1 style='text-align:center;color:#ff4b4b'>⚡ Smart Plug Energy Monitoring Dashboard ⚡</h1>",
    unsafe_allow_html=True,
)
st.markdown(
    "<h3 style='text-align:center;color:#008000'>Real-time visualization of voltage, current, power & energy usage</h3>",
    unsafe_allow_html=True,
)
st.markdown("<hr>", unsafe_allow_html=True)

# -----------------------------------------------------------
# Sidebar Controls
# -----------------------------------------------------------
st.sidebar.subheader("⏱️ Auto Refresh")

auto_refresh = st.sidebar.checkbox("Enable Auto-Refresh", value=True)

refresh_interval = st.sidebar.number_input(
    "Refresh Interval (seconds)",
    min_value=1,
    max_value=300,
    value=5,
    step=1,
)

# Use streamlit-autorefresh
if auto_refresh:
    st_autorefresh(interval=refresh_interval * 1000, key="dashboard_refresh")

st.sidebar.markdown("---")
st.sidebar.subheader("💰 Billing Configuration")

energy_cost = st.sidebar.number_input(
    "Energy Cost (BDT per kWh)",
    min_value=0.0,
    max_value=50.0,
    value=7.5,
    step=0.1,
)

# -----------------------------------------------------------
# Load Data (CLOUD SAFE - no loops)
# -----------------------------------------------------------
@st.cache_data
def load_data():
    if not os.path.exists(CSV_FILE):
        return pd.DataFrame(columns=[
            "Timestamp", "Voltage (V)", "Current (A)", "Power (W)", "Energy (kWh)", "Status"
        ])
    df = pd.read_csv(CSV_FILE)
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])
    return df

df = load_data()

# -----------------------------------------------------------
# Handle Empty Data
# -----------------------------------------------------------
if df.empty:
    st.info("Waiting for new data…")
    st.stop()

latest = df.iloc[-1]

# -----------------------------------------------------------
# Real-Time Gauges
# -----------------------------------------------------------
st.subheader("📟 Real-Time Electrical Metrics")

col1, col2, col3, col4 = st.columns(4)

def gauge(col, value, label, max_val):
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={"text": label},
        gauge={"axis": {"range": [0, max_val]}},
    ))
    col.plotly_chart(fig, width = 'stretch')

gauge(col1, latest["Voltage (V)"], "Voltage (V)", 300)
gauge(col2, latest["Current (A)"], "Current (A)", 15)
gauge(col3, latest["Power (W)"], "Power (W)", 500)
gauge(col4, latest["Energy (kWh)"], "Energy (kWh)", df["Energy (kWh)"].max() + 1)

# -----------------------------------------------------------
# Apparent Power & Power Factor
# -----------------------------------------------------------
df["Apparent Power (VA)"] = df["Voltage (V)"] * df["Current (A)"]
df["Power Factor"] = df["Power (W)"] / df["Apparent Power (VA)"].replace(0, 1)

st.subheader("⚙️ Electrical Efficiency Metrics")
m1, m2 = st.columns(2)
m1.metric("Apparent Power (VA)", f"{df['Apparent Power (VA)'].iloc[-1]:.1f}")
m2.metric("Power Factor", f"{df['Power Factor'].iloc[-1]:.3f}")

st.divider()

# -----------------------------------------------------------
# Main Power Chart
# -----------------------------------------------------------
st.plotly_chart(
    px.line(df, x="Timestamp", y="Power (W)", title="Power Consumption Over Time"),
    width = 'stretch'
)

vcol, ccol = st.columns(2)
vcol.plotly_chart(
    px.line(df, x="Timestamp", y="Voltage (V)", title="Voltage Trend"),
    width = 'stretch',
)
ccol.plotly_chart(
    px.line(df, x="Timestamp", y="Current (A)", title="Current Trend"),
    width = 'stretch',
)

# -----------------------------------------------------------
# Combined Power, Energy & Cost
# -----------------------------------------------------------
st.subheader("📈 Power, Energy & Estimated Cost Over Time")

df["Estimated Cost (BDT)"] = df["Energy (kWh)"] * energy_cost
fig = go.Figure()

fig.add_trace(go.Scatter(x=df["Timestamp"], y=df["Power (W)"], name="Power (W)"))
fig.add_trace(go.Scatter(x=df["Timestamp"], y=df["Energy (kWh)"], name="Energy (kWh)", yaxis="y2"))
fig.add_trace(go.Scatter(x=df["Timestamp"], y=df["Estimated Cost (BDT)"], name="Cost (BDT)", yaxis="y2"))

fig.update_layout(
    yaxis=dict(title="Power (W)"),
    yaxis2=dict(title="Energy (kWh) / Cost (BDT)", overlaying="y", side="right"),
)

st.plotly_chart(fig, width = 'stretch')

# -----------------------------------------------------------
# Totals
# -----------------------------------------------------------
total_energy = df["Energy (kWh)"].max()
est_cost = total_energy * energy_cost

t1, t2 = st.columns(2)
t1.metric("🔋 Total Energy Used", f"{total_energy:.3f} kWh")
t2.metric("💰 Estimated Cost", f"৳ {est_cost:.2f}")

st.divider()

# -----------------------------------------------------------
# Recent Data Log
# -----------------------------------------------------------
st.subheader("📘 Recent Data Log")
st.dataframe(df.tail(10), width = 'stretch', height=250)

# -----------------------------------------------------------
# Downloads
# -----------------------------------------------------------
st.subheader("📥 Download Reports")

csv_file = df.to_csv(index=False).encode("utf-8")
st.download_button("⬇ Download Full Data (CSV)", csv_file, "energy_data.csv")

summary_text = (
    f"Total Energy: {total_energy:.3f} kWh\n"
    f"Estimated Cost: ৳ {est_cost:.2f}\n"
    f"Peak Voltage: {df['Voltage (V)'].max():.1f} V\n"
    f"Peak Current: {df['Current (A)'].max():.3f} A\n"
    f"Peak Power: {df['Power (W)'].max():.1f} W\n"
)

st.download_button("⬇ Download Summary (TXT)", summary_text, "energy_summary.txt")
