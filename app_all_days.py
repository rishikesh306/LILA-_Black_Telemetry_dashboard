import streamlit as st
import matplotlib.pyplot as plt
from playeranalysis_all_days import (
    load_all_data,
    apply_filters,
    apply_timeline,
    convert_coordinates,
    separate_events,
    plot_journey,
    plot_heatmaps
)

# st.set_page_config(layout="wide")
st.title("🎮 LILA BLACK - Player Telemetry Dashboard")

# load all data
# @st.cache_data  # ← data once load pannurom, again reload pannatu
@st.cache_data(max_entries=1, ttl=3600)  # ← cache limit add pannurom
def get_data():
    return load_all_data()
def get_data():
    return load_all_data()

df = get_data()

# SIDEBAR FILTERS
st.sidebar.header("Filters")

# date filter
selected_date = st.sidebar.selectbox(
    "Select Date",
    ["February_10", "February_11", "February_12", "February_13", "February_14"]
)

# SIDEBAR FILTERS
st.sidebar.header("Filters")

# match filter - selected date la irukka matches மட்டும் show aagum
date_df = df[df["date"] == selected_date]
matches = date_df["match_id"].unique()

selected_match = st.sidebar.selectbox("Select Match", matches)

# map - auto detect pannurom
selected_map = df[df["match_id"] == selected_match]["map_id"].iloc[0]
st.sidebar.write("🗺️ Map:", selected_map)  # map name show pannurom

# timeline slider
timeline_seconds = st.sidebar.slider("Timeline (seconds)", 5, 300, 150)

# APPLY PIPELINE
filtered_df = apply_filters(df, selected_date, selected_match)
filtered_df = apply_timeline(filtered_df, seconds=timeline_seconds)
filtered_df = convert_coordinates(filtered_df, selected_map)

human_df, bot_df, kill_df, death_df, botkill_df, botdeath_df, loot_df, storm_df = separate_events(filtered_df)

# no data check
if len(human_df) == 0:
    st.warning("⚠️ No player data. Try increasing timeline!")
    st.stop()

# PLAYER JOURNEY
st.subheader("🗺️ Player Journey")

fig = plot_journey(human_df, bot_df, kill_df, death_df, botkill_df, botdeath_df, loot_df, storm_df, selected_map)
st.pyplot(fig)
plt.close()

# HEATMAPS
st.subheader("🔥 Heatmaps")

fig1, fig2, fig3 = plot_heatmaps(human_df, kill_df, botkill_df, death_df, botdeath_df, selected_map)

col1, col2, col3 = st.columns(3)

with col1:
    st.pyplot(fig1)
    plt.close()

with col2:
    st.pyplot(fig2)
    plt.close()

with col3:
    st.pyplot(fig3)
    plt.close()

