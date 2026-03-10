import streamlit as st
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from playeranalysis_all_days import (
    load_day_data,
    apply_timeline,
    convert_coordinates,
    separate_events,
    plot_journey,
    plot_heatmaps
)

# Page Title
st.title("🎮 LILA BLACK - Player Telemetry Dashboard")

# Cache Data Loader
@st.cache_data
def get_data(selected_date):
    return load_day_data(selected_date)

# ---------------- SIDEBAR ----------------
st.sidebar.header("Filters")

# Date Selection
selected_date = st.sidebar.selectbox(
    "Select Date",
    ["February_10", "February_11", "February_12", "February_13", "February_14"]
)

# Load Data
df = get_data(selected_date)

# Safety check
if df is None or df.empty:
    st.warning("⚠️ No data found for this date")
    st.stop()

st.write("Rows:", len(df))

# Match Selection
matches = sorted(df["match_id"].unique())

if len(matches) == 0:
    st.warning("⚠️ No matches available")
    st.stop()

selected_match = st.sidebar.selectbox("Select Match", matches)

# Match Data
match_df = df[df["match_id"] == selected_match]

if match_df.empty:
    st.warning("⚠️ Match data not found")
    st.stop()

# Map Detection
selected_map = match_df["map_id"].iloc[0]
st.sidebar.write("🗺️ Map:", selected_map)

# Timeline Slider
timeline_seconds = st.sidebar.slider(
    "Timeline (seconds)",
    min_value=5,
    max_value=300,
    value=150
)

# ---------------- PIPELINE ----------------

filtered_df = match_df.copy()

filtered_df = apply_timeline(filtered_df, seconds=timeline_seconds)
filtered_df = convert_coordinates(filtered_df, selected_map)

(
    human_df,
    bot_df,
    kill_df,
    death_df,
    botkill_df,
    botdeath_df,
    loot_df,
    storm_df
) = separate_events(filtered_df)

# Player Data Check
if human_df.empty:
    st.warning("⚠️ No player data. Try increasing timeline!")
    st.stop()

# ---------------- PLAYER JOURNEY ----------------

plt.close("all")
st.subheader("🗺️ Player Journey")

fig = plot_journey(
    human_df,
    bot_df,
    kill_df,
    death_df,
    botkill_df,
    botdeath_df,
    loot_df,
    storm_df,
    selected_map
)

st.pyplot(fig)
plt.close(fig)

# ---------------- HEATMAPS ----------------

st.subheader("🔥 Heatmaps")

fig1, fig2 = plot_heatmaps(
    human_df,
    kill_df,
    botkill_df,
    death_df,
    botdeath_df,
    selected_map
)

col1, col2 = st.columns(2)

with col1:
    st.pyplot(fig1)
    plt.close(fig1)

with col2:
    st.pyplot(fig2)
    plt.close(fig2)

