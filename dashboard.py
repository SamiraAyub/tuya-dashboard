import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import glob
import os
import time
from streamlit_autorefresh import st_autorefresh

# ---------------------------------------------------------
# Configuration
# ---------------------------------------------------------
st.set_page_config(page_title="IoT Multi-Device Dashboard", layout="wide")

DEVICE_DIR = "data/"  # folder containing device CSV files

# Load all device files
device_files = sorted(glob.glob(os.path.join(DEVICE_DIR, "*.csv")))
device_list = [os.path.basename(f).replace(".csv", "") for f in device_files]

# Session state for selected device
if "selected_device" not in st.session_state:
    st.session_state["selected_device"] = None


# ---------------------------------------------------------
# Dashboard function for a single device
# ---------------------------------------------------------
def show_device_dashboard(df, device_name):

    st.markdown(f"<h2 style='text-align:center;'>📊 Device Dashboard: {device_name}</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)

    # Auto Refresh
    st.sidebar.subheader("⏱️ Auto Refresh")
    auto_refresh = st.sidebar.checkbox("Enable Auto-Refresh", value=True)

    refresh_interval = st.sidebar.number_input(
        "Refresh Interval (seconds)", min_value=1, max_value=300, value=5
    )

    if auto_refresh:
        st_autorefresh(interval=refresh_interval * 1000, key="refresh_key")

    # Smooth energy cost config
    st.sidebar.subheader("💰 Billing")
    energy_cost = st.sidebar.number_input("BDT per kWh", 0.0, 50.0, 7.5, 0.1)

    # ----------------------------------------------------
    # Real-time metrics
    # ----------------------------------------------------
    latest = df.iloc[-1]

    st.subheader("📟 Real-Time Electrical Metrics")

    col1, col2, col3, col4 = st.columns(4)

    def gauge(col, value, label, max_val):
        fig = go.Figure(go.Indicator(
            mode="gauge+number",
            value=value,
            title={"text": label},
            gauge={"axis": {"range": [0, max_val]}}
        ))
        col.plotly_chart(fig, width = 'stretch')

    gauge(col1, latest["Voltage (V)"], "Voltage (V)", 300)
    gauge(col2, latest["Current (A)"], "Current (A)", 15)
    gauge(col3, latest["Power (W)"], "Power (W)", 500)
    gauge(col4, latest["Energy (kWh)"], "Energy (kWh)", df["Energy (kWh)"].max() + 1)

    # ----------------------------------------------------
    # Power Factor + Apparent Power
    # ----------------------------------------------------
    df["Apparent Power (VA)"] = df["Voltage (V)"] * df["Current (A)"]
    df["Power Factor"] = df.apply(
        lambda r: 0 if r["Apparent Power (VA)"] == 0 else r["Power (W)"] / r["Apparent Power (VA)"],
        axis=1
    )

    st.subheader("⚙️ Electrical Efficiency")
    m1, m2 = st.columns(2)
    m1.metric("Apparent Power (VA)", f"{df['Apparent Power (VA)'].iloc[-1]:.1f}")
    m2.metric("Power Factor", f"{df['Power Factor'].iloc[-1]:.3f}")

    st.divider()

    # ----------------------------------------------------
    # Time Series Charts
    # ----------------------------------------------------
    st.subheader("📈 Power Consumption Over Time")
    st.plotly_chart(px.line(df, x="Timestamp", y="Power (W)", title="Power (W) vs Time"), width = 'stretch')

    vcol, ccol = st.columns(2)
    vcol.plotly_chart(px.line(df, x="Timestamp", y="Voltage (V)", title="Voltage Trend"), width = 'stretch')
    ccol.plotly_chart(px.line(df, x="Timestamp", y="Current (A)", title="Current Trend"), width = 'stretch')

    # Combined power & cost
    df["Estimated Cost (BDT)"] = df["Energy (kWh)"] * energy_cost

    st.subheader("📊 Power, Energy & Cost Over Time")
    fig = go.Figure()
    fig.add_trace(go.Scatter(x=df["Timestamp"], y=df["Power (W)"], name="Power (W)"))
    fig.add_trace(go.Scatter(x=df["Timestamp"], y=df["Energy (kWh)"], name="Energy (kWh)", yaxis="y2"))
    fig.add_trace(go.Scatter(x=df["Timestamp"], y=df["Estimated Cost (BDT)"], name="Cost (BDT)", yaxis="y2"))

    fig.update_layout(
        yaxis=dict(title="Power (W)"),
        yaxis2=dict(title="Energy (kWh) / Cost (BDT)", overlaying="y", side="right")
    )

    st.plotly_chart(fig, width = 'stretch')

    # ----------------------------------------------------
    # Totals
    # ----------------------------------------------------
    total_energy = df["Energy (kWh)"].max()
    total_cost = total_energy * energy_cost

    t1, t2 = st.columns(2)
    t1.metric("🔋 Total Energy Used", f"{total_energy:.3f} kWh")
    t2.metric("💰 Estimated Cost", f"৳ {total_cost:.2f}")

    st.divider()

    # ----------------------------------------------------
    # Recent Logs
    # ----------------------------------------------------
    st.subheader("📘 Recent Records")
    st.dataframe(df.tail(10), width = 'stretch')

    # ----------------------------------------------------
    # Downloads
    # ----------------------------------------------------
    st.subheader("📥 Download Data")
    st.download_button("⬇ Download CSV", df.to_csv(index=False), f"{device_name}.csv")


# ---------------------------------------------------------
# FRONT PAGE — Device Tiles
# ---------------------------------------------------------
st.title("🔌 IoT Device Monitoring Portal")
st.markdown("Select a device to view its live dashboard.")

cols = st.columns(5)

for idx, device in enumerate(device_list):
    with cols[idx % 5]:
        if st.button(f"📟 {device}", width = 'stretch'):
            st.session_state["selected_device"] = device


st.markdown("---")

# ---------------------------------------------------------
# LOAD SELECTED DEVICE DASHBOARD
# ---------------------------------------------------------
if st.session_state["selected_device"]:
    device_name = st.session_state["selected_device"]
    df = pd.read_csv(os.path.join(DEVICE_DIR, f"{device_name}.csv"))
    df["Timestamp"] = pd.to_datetime(df["Timestamp"])

    show_device_dashboard(df, device_name)
