# LILA BLACK – Player Telemetry Dashboard

## What is this?

An interactive web dashboard that visualizes **player behavior** in LILA BLACK (a battle-royale style game) using **5 days of real production gameplay data** (Feb 10–14, 2026).

Built for Level Designers to explore how players move, fight, and die across 3 maps.

---

## Live multiple player Telemetry dasboard

🔗 [View Dashboard](https://lila-blacktelemetrydashboard-miqwtowrayof47w7wdrqou.streamlit.app/)

---
## Deployment Notes (Important)

The full dashboard is deployed using the free version of Streamlit Cloud.

Since the dataset is relatively large (~89,000 rows across 1,243 files), some infrastructure-related limitations may occur.

---

## 1. App Sleep / Initial Loading Delay

If the dashboard is opened after some inactivity:

- It may take time to load  
- It may appear temporarily unresponsive  

This happens because the free cloud environment automatically goes to sleep when not in use.

Additionally, loading large telemetry datasets requires significant RAM usage.

If the app does not respond:

    Wait for the initial load
    OR  
    Refresh the page

If the issue persists:

- Clone/download the repository

- Run locally using:
    - streamlit run app_all_days.py

Running locally does not produce these issues, as local system RAM resources are available.

---
## 2. Timeline Filter Usage Recommendation

While using the timeline slider:

- Adjust time in small increments (5–10 seconds)

- Avoid jumping across large time ranges at once

- Large jumps increase memory usage in the free cloud environment and may cause a temporary crash.

This issue does not occur when running locally.

---
## 3. Occasional Match Loading Issue

- Due to the large number of files and event rows:

- A selected match may occasionally fail to load

- The visualization may not render properly

- If This Happens

      Refresh the page 
      OR
      Select another match
      OR
      Switch to a different day

This is related to cloud resource limitations, not the processing logic.

---
## Why These Notes Are Mentioned

As a student developer, I believe it is important to clearly communicate deployment constraints along with technical implementation.

The analytical pipeline works as expected.
The mentioned limitations are related to free-tier cloud infrastructure.

---

## Dataset Overview

| Metric | Value |
|--------|-------|
| Date Range | February 10–14, 2026 |
| Total Files | 1,243 |
| Total Event Rows | ~89,000 |
| Unique Players | 339 |
| Unique Matches | 796 |
| Maps | AmbroseValley, GrandRift, Lockdown |

> Note: February 14 is a partial day.

---

## Features

- 🗺️ **Player Journey Map** — Track player movement on the minimap with kills, deaths, loot, and storm events
- 🔥 **Heatmaps** — Player traffic, kill zones, and death zones overlaid on the map
- 🎮 **Filters** — Filter by date, match, and map
- ⏯️ **Timeline Slider** — Watch a match unfold step by step

---

## How It Works

1. Load all 5 days of parquet data
2. Filter by date → match → map
3. Convert world coordinates → minimap pixel coordinates
4. Separate events (Position, Kill, Death, Loot, Storm)
5. Visualize on minimap with timeline control

---

## Map Coordinate Settings

| Map | Scale | Origin X | Origin Z |
|-----|-------|----------|----------|
| AmbroseValley | 900 | -370 | -473 |
| GrandRift | 581 | -290 | -290 |
| Lockdown | 1000 | -500 | -500 |

---

## Tech Stack

- **Python** — Data processing
- **PyArrow + Pandas** — Parquet file handling
- **Matplotlib + Seaborn** — Visualization
- **Streamlit** — Interactive dashboard

---

## Project Structure

```
LILA-Black_Telemetry_dashboard/
│
├── app_all_days.py              ← Streamlit app
├── playeranalysis_all_days.py   ← Data pipeline
├── requirements.txt             ← Dependencies
│
├── minimaps/
│   ├── AmbroseValley_Minimap.png
│   ├── GrandRift_Minimap.png
│   └── Lockdown_Minimap.jpg
│
└── player_data/
    ├── February_10/
    ├── February_11/
    ├── February_12/
    ├── February_13/
    └── February_14/
```

---
