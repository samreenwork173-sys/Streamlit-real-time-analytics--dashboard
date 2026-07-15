"""Real-Time Data Analytics Dashboard
--------------
---------------------
Simulates a live data stream (e.g. website traffic / sales events) and displays
auto-refreshing KPIs and charts. This is the standard, widely-accepted approach
for "real-time dashboard" academic/portfolio projects when a live external
data feed isn't required — see README.md for rationale.

Run with:  streamlit run app.py
"""

import time
import random
from datetime import datetime

import numpy as np
import pandas as pd
import streamlit as st

# ----------------------------------------------------------------------
# Page config
# ----------------------------------------------------------------------
st.set_page_config(
    page_title="Real-Time Analytics Dashboard",
    page_icon="📊",
    layout="wide",
)

REFRESH_INTERVAL_SECONDS = 5
MAX_POINTS = 50

# ----------------------------------------------------------------------
# Session state: holds the "live" data across refreshes
# ----------------------------------------------------------------------
if "history" not in st.session_state:
    st.session_state.history = pd.DataFrame(
        columns=["timestamp", "active_users", "orders", "revenue", "region"]
    )

REGIONS = ["North", "South", "East", "West", "Central"]


def generate_live_event():
    """Simulates one tick of incoming live data (e.g. from a streaming API)."""
    return {
        "timestamp": datetime.now(),
        "active_users": random.randint(80, 500),
        "orders": random.randint(0, 25),
        "revenue": round(random.uniform(0, 3000), 2),
        "region": random.choice(REGIONS),
    }


# ----------------------------------------------------------------------
# Header
# ----------------------------------------------------------------------
st.title("📊 Real-Time Data Analytics Dashboard")
st.caption(
    "Simulated live data stream — updates every "
    f"{REFRESH_INTERVAL_SECONDS} seconds. See README for data source notes."
)

col_a, col_b = st.columns([3, 1])
with col_b:
    auto_refresh = st.toggle("Auto-refresh", value=True)
    if st.button("➕ Add new data point now"):
        new_row = generate_live_event()
        st.session_state.history = pd.concat(
            [st.session_state.history, pd.DataFrame([new_row])], ignore_index=True
        )

# Append a new simulated event each run
new_row = generate_live_event()
st.session_state.history = pd.concat(
    [st.session_state.history, pd.DataFrame([new_row])], ignore_index=True
)
st.session_state.history = st.session_state.history.tail(MAX_POINTS).reset_index(drop=True)

df = st.session_state.history

# ----------------------------------------------------------------------
# KPI row
# ----------------------------------------------------------------------
if not df.empty:
    latest = df.iloc[-1]
    prev = df.iloc[-2] if len(df) > 1 else latest

    k1, k2, k3, k4 = st.columns(4)
    k1.metric("Active Users", int(latest["active_users"]),
              delta=int(latest["active_users"] - prev["active_users"]))
    k2.metric("Orders (this tick)", int(latest["orders"]),
              delta=int(latest["orders"] - prev["orders"]))
    k3.metric("Revenue (this tick)", f"${latest['revenue']:,.2f}",
              delta=f"${latest['revenue'] - prev['revenue']:,.2f}")
    k4.metric("Total Revenue (session)", f"${df['revenue'].sum():,.2f}")

    st.divider()

    # ------------------------------------------------------------------
    # Charts
    # ------------------------------------------------------------------
    c1, c2 = st.columns(2)

    with c1:
        st.subheader("Active Users Over Time")
        st.line_chart(df.set_index("timestamp")["active_users"])

    with c2:
        st.subheader("Revenue Per Tick")
        st.bar_chart(df.set_index("timestamp")["revenue"])

    st.subheader("Orders by Region (session total)")
    region_totals = df.groupby("region")["orders"].sum().sort_values(ascending=False)
    st.bar_chart(region_totals)

    st.subheader("Live Event Log (most recent 10)")
    st.dataframe(
        df.tail(10).sort_values("timestamp", ascending=False),
        use_container_width=True,
        hide_index=True,
    )
else:
    st.info("Waiting for first data point...")

# ----------------------------------------------------------------------
# Auto-refresh loop
# ----------------------------------------------------------------------
if auto_refresh:
    time.sleep(REFRESH_INTERVAL_SECONDS)
    st.rerun()
