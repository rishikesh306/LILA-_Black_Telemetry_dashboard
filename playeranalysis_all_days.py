import pyarrow.parquet as pq
import os
import pandas as pd

def load_all_data():

    base_path = "player_data"  # main folder

    folders = [
        "February_10",  # day 1
        "February_11",  # day 2
        "February_12",  # day 3
        "February_13",  # day 4
        "February_14"   # day 5
    ]

    all_data = []  # empty list - all files data inga store aagum

    for folder in folders:  # each folder oru by oru loop pannurom
        folder_path = os.path.join(base_path, folder)  # folder path join pannurom
        files = os.listdir(folder_path)  # folder la iruka all files list pannurom

        for file in files:  # each file oru by oru open pannurom
            file_path = os.path.join(folder_path, file)  # file full path
            table = pq.read_table(file_path)  # parquet file read pannurom
            df = table.to_pandas()  # dataframe aa convert pannurom
            df["date"] = folder  # which folder file nu mark pannurom
            all_data.append(df)  # list la add pannurom

    combined_df = pd.concat(all_data, ignore_index=True)  # all files oru dataframe aa combine pannurom

    # event column bytes → string convert pannurom
    combined_df["event"] = combined_df["event"].apply(
        lambda x: x.decode("utf-8") if isinstance(x, bytes) else x
    )

    print("Total rows:", len(combined_df))  # total data count
    print("Dates:", combined_df["date"].unique())  # 5 dates show aagum
    
    return combined_df  # data return pannurom



# filter section

def apply_filters(combined_df, selected_date, selected_match):

    # date filter
    df = combined_df[combined_df["date"] == selected_date]

    # match filter
    df = df[df["match_id"] == selected_match]

    return df

def apply_timeline(df, seconds=10):

    total_rows = len(df)  # total rows count
    ratio = seconds / 300  # slider ratio calculate pannurom
    cutoff = int(total_rows * ratio)  # cutoff point

    return df.iloc[:cutoff]  # cutoff vara data return pannurom

def convert_coordinates(df, map_id):

    map_settings = {
    "AmbroseValley": {"origin_x": -370, "origin_z": -473, "scale": 900,  "map_size": 4320},
    "GrandRift":     {"origin_x": -290, "origin_z": -290, "scale": 581,  "map_size": 2160},
    "Lockdown":      {"origin_x": -500, "origin_z": -500, "scale": 1000, "map_size": 9000},
}
    settings = map_settings[map_id]
    origin_x = settings["origin_x"]
    origin_z = settings["origin_z"]
    scale = settings["scale"]
    map_size = settings["map_size"]  # each map ku correct size!

    df["map_x"] = ((df["x"] - origin_x) / scale) * map_size
    df["map_y"] = (1 - ((df["z"] - origin_z) / scale)) * map_size

    return df

def separate_events(df):

    human_df = df[df["event"] == "Position"].sort_values("ts")  # human movement
    bot_df = df[df["event"] == "BotPosition"].sort_values("ts")  # bot movement

    kill_df = df[df["event"] == "Kill"]          # human kills
    death_df = df[df["event"] == "Killed"]        # human deaths
    botkill_df = df[df["event"] == "BotKill"]    # bot kills
    botdeath_df = df[df["event"] == "BotKilled"] # bot deaths
    loot_df = df[df["event"] == "Loot"]          # loot events
    storm_df = df[df["event"] == "KilledByStorm"] # storm deaths

    return human_df, bot_df, kill_df, death_df, botkill_df, botdeath_df, loot_df, storm_df

import matplotlib.image as mpimg  # map image load pannurom

BASE_DIR = os.path.dirname(__file__)  # current file location

def get_map_image(map_id):

    map_images = {
        "AmbroseValley": "AmbroseValley_Minimap.png",
        "GrandRift":     "GrandRift_Minimap.png",
        "Lockdown":      "Lockdown_Minimap.jpg",
    }

    image_file = map_images[map_id]  # correct map image select pannurom
    return mpimg.imread(os.path.join(BASE_DIR, "minimaps", image_file))  # image load pannurom

import matplotlib.pyplot as plt
def plot_journey(human_df, bot_df, kill_df, death_df, botkill_df, botdeath_df, loot_df, storm_df, map_id):

    map_img = get_map_image(map_id)  # correct map image load pannurom

    fig, ax = plt.subplots(figsize=(10, 8))
    ax.imshow(map_img)
    map_size = map_img.shape[1]
    ax.set_xlim(0, map_size)
    ax.set_ylim(map_size, 0)

    if len(human_df) > 0:
        ax.scatter(human_df["map_x"].iloc[0], human_df["map_y"].iloc[0], color="green", s=100, label="Start")
        ax.scatter(human_df["map_x"].iloc[-1], human_df["map_y"].iloc[-1], color="red", s=100, label="End")
        ax.plot(human_df["map_x"], human_df["map_y"], linewidth=2, label="Human Movement")

    if len(bot_df) > 0:
        ax.plot(bot_df["map_x"], bot_df["map_y"], linewidth=2, color="orange", label="Bot Movement")

    if len(loot_df) > 0:
        ax.scatter(loot_df["map_x"], loot_df["map_y"], color="yellow", label="Loot")

    if len(kill_df) > 0:
        ax.scatter(kill_df["map_x"], kill_df["map_y"], color="green", marker="*", s=120, label="Kill")

    if len(death_df) > 0:
        ax.scatter(death_df["map_x"], death_df["map_y"], color="red", marker="x", s=120, label="Death")

    if len(botkill_df) > 0:
        ax.scatter(botkill_df["map_x"], botkill_df["map_y"], color="lime", marker="*", s=120, label="Bot Kill")

    if len(botdeath_df) > 0:
        ax.scatter(botdeath_df["map_x"], botdeath_df["map_y"], color="darkred", marker="x", s=120, label="Bot Death")

    if len(storm_df) > 0:
        ax.scatter(storm_df["map_x"], storm_df["map_y"], color="purple", marker="X", s=120, label="Storm Death")

    ax.set_title("Player Journey with Game Events")
    ax.legend()
    return fig

import seaborn as sns  # heatmap pannurom

def plot_heatmaps(human_df, kill_df, botkill_df, death_df, botdeath_df, map_id):

    map_img = get_map_image(map_id)  # correct map image load pannurom

    # PLAYER TRAFFIC
    fig1, ax1 = plt.subplots(figsize=(6, 5))
    ax1.imshow(map_img)
    map_size = map_img.shape[1]
    ax1.set_xlim(0, map_size)
    ax1.set_ylim(map_size, 0)
    if len(human_df) > 1:
        sns.kdeplot(x=human_df["map_x"], y=human_df["map_y"],
                    cmap="Reds", fill=True, thresh=0.05,
                    warn_singular=False, ax=ax1)
    ax1.set_title("Player Traffic")

   
    # KILL ZONES
    all_kills = pd.concat([kill_df, botkill_df])
    fig2, ax2 = plt.subplots(figsize=(6, 5))
    ax2.imshow(map_img)  # ← map always show pannurom
    map_size = map_img.shape[1]
    ax2.set_xlim(0, map_size)
    ax2.set_ylim(map_size, 0)
    if len(all_kills) > 1:
        sns.kdeplot(x=all_kills["map_x"], y=all_kills["map_y"],
                cmap="Greens", fill=True, thresh=0.05,
                warn_singular=False, ax=ax2)
    else:
    # kills kam-a irundha scatter show pannurom
        if len(all_kills) > 0:
            ax2.scatter(all_kills["map_x"], all_kills["map_y"], 
                   color="lime", s=100, label="Kill")
    ax2.set_title("Kill Zones")
    
    # DEATH ZONES
    all_deaths = pd.concat([death_df, botdeath_df])
    fig3, ax3 = plt.subplots(figsize=(6, 5))
    ax3.imshow(map_img)
    map_size = map_img.shape[1]
    ax3.set_xlim(0, map_size)
    ax3.set_ylim(map_size, 0)
    if len(all_deaths) > 1:
        sns.kdeplot(x=all_deaths["map_x"], y=all_deaths["map_y"],
                    cmap="Blues", fill=True, thresh=0.05,
                    warn_singular=False, ax=ax3)
    ax3.set_title("Death Zones")

    return fig1, fig2, fig3

def main():

    # 1 load all data
    df = load_all_data()

    # 2 test - first date and match select pannurom
    selected_date = "February_10"
    selected_match = df[df["date"] == selected_date]["match_id"].iloc[0]
    selected_map = df[df["match_id"] == selected_match]["map_id"].iloc[0]

    print("Testing with:")
    print("Date:", selected_date)
    print("Match:", selected_match)
    print("Map:", selected_map)

    # 3 filter
    filtered_df = apply_filters(df, selected_date, selected_match)

    # 4 timeline
    filtered_df = apply_timeline(filtered_df, seconds=300)

    # 5 convert coordinates
    filtered_df = convert_coordinates(filtered_df, selected_map)

    # 6 separate events
    human_df, bot_df, kill_df, death_df, botkill_df, botdeath_df, loot_df, storm_df = separate_events(filtered_df)

    # 7 plot journey
    plot_journey(human_df, bot_df, kill_df, death_df, botkill_df, botdeath_df, loot_df, storm_df, selected_map)
    plt.show()

    # 8 plot heatmaps
    fig1, fig2, fig3 = plot_heatmaps(human_df, kill_df, botkill_df, death_df, botdeath_df, selected_map)
    plt.show()


if __name__ == "__main__":
    main()