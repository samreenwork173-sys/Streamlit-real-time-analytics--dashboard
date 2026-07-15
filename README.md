# Real-Time Data Analytics Dashboard

A live-updating analytics dashboard built with Streamlit, displaying KPIs and
charts that refresh automatically as new data arrives.

## Data Source Note
This dashboard uses a **simulated live data stream** (new random events
generated every few seconds) rather than a live external API. This is a
standard, widely-used approach for real-time dashboard projects when the goal
is to demonstrate real-time *architecture* (auto-refresh, live state,
streaming visualization) rather than integrate a specific paid data feed.
Swapping in a real API (e.g. a stock price feed, IoT sensor feed, or website
analytics API) only requires replacing the `generate_live_event()` function
in `app/app.py` with a real API call.

## Project Structure
```
project3-realtime-dashboard/
├── app/
│   └── app.py           # Streamlit dashboard
├── requirements.txt
└── README.md
```

## How to Run
```bash
pip install -r requirements.txt
cd app
streamlit run app.py
```
This opens the dashboard in your browser (usually `http://localhost:8501`).
It updates automatically every 3 seconds. Toggle "Auto-refresh" off to pause,
or click "Add new data point now" to manually inject an event.

## Features
- **Live KPIs**: active users, orders, revenue per tick, session total revenue
  — each with a delta vs. the previous tick.
- **Live line/bar charts**: active users over time, revenue per tick.
- **Regional breakdown**: orders by region, aggregated across the session.
- **Live event log**: most recent 10 raw events in a table.
- **Manual + auto refresh modes.**

## Tech Stack
Python, Streamlit, Pandas, NumPy

## Possible Extensions
- Replace the simulated feed with a real API (weather, stock prices, etc.)
- Add alert thresholds (e.g. flag when active users drop below X)
- Persist history to a database instead of in-memory session state
