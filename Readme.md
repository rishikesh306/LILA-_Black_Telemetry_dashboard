# LILA BLACK – Player Telemetry Dashboard

## What is this?

An interactive web dashboard that visualizes **player behavior** in LILA BLACK (a battle-royale style game) using **5 days of real production gameplay data** (Feb 10–14, 2026).

Built for Level Designers to explore how players move, fight, and die across 3 maps.

---

## Live Demo

🔗 [View Dashboard](https://your-streamlit-url.streamlit.app)

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
