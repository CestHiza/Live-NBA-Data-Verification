# generate_nba_feeds.py
import pandas as pd
import numpy as np
import time
import random
import os

# --- Game Setup ---
PLAYERS = {
    "Team A": ["Player A1", "Player A2", "Player A3", "Player A4", "Player A5"],
    "Team B": ["Player B1", "Player B2", "Player B3", "Player B4", "Player B5"]
}
GAME_DURATION_SECONDS = 300 # Simulate a 5-minute game for demonstration
EVENT_INTERVAL_SECONDS = 3 # Time between game events

def initialize_box_score():
    """Creates an empty box score DataFrame."""
    players_list = PLAYERS["Team A"] + PLAYERS["Team B"]
    box_score = pd.DataFrame({
        "player_name": players_list,
        "points": 0,
        "rebounds": 0,
        "assists": 0
    })
    return box_score

def simulate_game_event(box_score):
    """Simulates a single random game event and updates the box score."""
    team = random.choice(["Team A", "Team B"])
    player = random.choice(PLAYERS[team])
    
    # Probabilities for different events
    event_type = random.choices(
        ["2pt_made", "3pt_made", "miss_with_rebound", "assist"],
        weights=[0.45, 0.20, 0.30, 0.25], # Note: assist can happen with a made shot
        k=1
    )[0]

    event_log = f"Event: {player}"
    
    if event_type == "2pt_made":
        box_score.loc[box_score["player_name"] == player, "points"] += 2
        event_log += " made a 2-point shot."
        # Check for an assist
        if random.random() < 0.5: # 50% chance of an assist on a made shot
            assisting_player = random.choice([p for p in PLAYERS[team] if p != player])
            box_score.loc[box_score["player_name"] == assisting_player, "assists"] += 1
            event_log += f" Assist by {assisting_player}."
            
    elif event_type == "3pt_made":
        box_score.loc[box_score["player_name"] == player, "points"] += 3
        event_log += " made a 3-point shot."
        # Check for an assist
        if random.random() < 0.5:
            assisting_player = random.choice([p for p in PLAYERS[team] if p != player])
            box_score.loc[box_score["player_name"] == assisting_player, "assists"] += 1
            event_log += f" Assist by {assisting_player}."

    elif event_type == "miss_with_rebound":
        rebounding_team = random.choice(["Team A", "Team B"])
        rebounding_player = random.choice(PLAYERS[rebounding_team])
        box_score.loc[box_score["player_name"] == rebounding_player, "rebounds"] += 1
        event_log += f" missed a shot. Rebound by {rebounding_player}."
        
    elif event_type == "assist": # This handles assists that might not be caught by the made shot logic
        # This event is redundant if assist is handled above, but simulates a feed that only sends assist events
        made_shot_player = random.choice([p for p in PLAYERS[team] if p != player])
        box_score.loc[box_score["player_name"] == player, "assists"] += 1
        event_log += f" assists a shot by {made_shot_player}."

    return box_score, event_log

def introduce_discrepancy(box_score_df):
    """Randomly introduces a small error into a box score DataFrame."""
    df_copy = box_score_df.copy()
    if random.random() < 0.15: # 15% chance to introduce an error
        player_to_change = random.choice(df_copy["player_name"])
        stat_to_change = random.choice(["points", "rebounds", "assists"])
        # Add or subtract one from the stat
        change = random.choice([-1, 1])
        df_copy.loc[df_copy["player_name"] == player_to_change, stat_to_change] += change
        # Ensure stats don't go below zero
        df_copy.loc[df_copy["player_name"] == player_to_change, stat_to_change] = \
            df_copy.loc[df_copy["player_name"] == player_to_change, stat_to_change].clip(lower=0)
        print(f"    -> DISCREPANCY INTRODUCED for {player_to_change} in {stat_to_change}")
    return df_copy

def main():
    """Main function to run the live feed simulation."""
    print("--- Starting Live NBA Data Feed Simulation ---")
    print(f"Simulating a {GAME_DURATION_SECONDS}-second game period.")
    
    box_score = initialize_box_score()
    start_time = time.time()
    
    while time.time() - start_time < GAME_DURATION_SECONDS:
        box_score, event_log = simulate_game_event(box_score)
        print(f"\nSimulating game event... {event_log}")

        # Create two versions of the feed
        feed_a_box = box_score.copy()
        feed_b_box = box_score.copy()

        # Introduce potential discrepancies and delays
        # Feed B is slightly delayed and more prone to errors
        if random.random() < 0.4: # 40% chance Feed B has an error
            feed_b_box = introduce_discrepancy(feed_b_box)
        
        # Write to Feed A (the more reliable feed)
        feed_a_box['timestamp'] = datetime.now().isoformat()
        feed_a_box.to_csv("feed_A.csv", index=False)
        print("  - Feed A updated.")
        
        # Simulate a slight delay for Feed B
        time.sleep(random.uniform(0.5, 2.0))
        
        # Write to Feed B
        feed_b_box['timestamp'] = datetime.now().isoformat()
        feed_b_box.to_csv("feed_B.csv", index=False)
        print("  - Feed B updated.")

        time.sleep(EVENT_INTERVAL_SECONDS)

    print("\n--- Game Simulation Finished ---")

if __name__ == "__main__":
    from datetime import datetime
    main()