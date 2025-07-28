# monitor_nba_data.py
import pandas as pd
import time
import os
from datetime import datetime

# --- Configuration ---
FEED_A_PATH = "feed_A.csv"
FEED_B_PATH = "feed_B.csv"
DASHBOARD_DATA_PATH = "live_dashboard_data.csv"
DISCREPANCY_LOG_PATH = "discrepancy_log.csv"
MONITOR_INTERVAL_SECONDS = 2 # How often to check the feeds

def initialize_log_file():
    """Creates the discrepancy log file with headers if it doesn't exist."""
    if not os.path.exists(DISCREPANCY_LOG_PATH):
        log_df = pd.DataFrame(columns=[
            "log_timestamp", "player_name", "stat", 
            "feed_a_value", "feed_b_value", "discrepancy_amount"
        ])
        log_df.to_csv(DISCREPANCY_LOG_PATH, index=False)

def log_discrepancy(player, stat, val_a, val_b):
    """Appends a new discrepancy to the log file."""
    discrepancy_amount = val_b - val_a
    new_log_entry = pd.DataFrame([{
        "log_timestamp": datetime.now().isoformat(),
        "player_name": player,
        "stat": stat,
        "feed_a_value": val_a,
        "feed_b_value": val_b,
        "discrepancy_amount": discrepancy_amount
    }])
    new_log_entry.to_csv(DISCREPANCY_LOG_PATH, mode='a', header=False, index=False)
    print(f"  🚨 DISCREPANCY LOGGED: {player} | {stat} | Feed A: {val_a}, Feed B: {val_b}")

def cross_verify_feeds():
    """
    Reads data from both feeds, compares them, logs discrepancies,
    and outputs a unified dataset for the dashboard.
    """
    try:
        feed_a = pd.read_csv(FEED_A_PATH)
        feed_b = pd.read_csv(FEED_B_PATH)
    except FileNotFoundError:
        print("Waiting for data feeds to be generated...")
        return # Skip this cycle if files don't exist yet

    # Merge the two feeds on player_name to compare stats side-by-side
    comparison_df = pd.merge(
        feed_a, feed_b, 
        on="player_name", 
        suffixes=('_a', '_b')
    )

    dashboard_data = feed_a.copy()
    dashboard_data['discrepancy_flag'] = False
    dashboard_data['discrepancy_details'] = ""

    discrepancies_found = False
    for _, row in comparison_df.iterrows():
        player = row['player_name']
        details = []
        
        # Compare points
        if row['points_a'] != row['points_b']:
            log_discrepancy(player, 'points', row['points_a'], row['points_b'])
            details.append(f"Points ({row['points_a']} vs {row['points_b']})")
            discrepancies_found = True

        # Compare rebounds
        if row['rebounds_a'] != row['rebounds_b']:
            log_discrepancy(player, 'rebounds', row['rebounds_a'], row['rebounds_b'])
            details.append(f"Rebounds ({row['rebounds_a']} vs {row['rebounds_b']})")
            discrepancies_found = True

        # Compare assists
        if row['assists_a'] != row['assists_b']:
            log_discrepancy(player, 'assists', row['assists_a'], row['assists_b'])
            details.append(f"Assists ({row['assists_a']} vs {row['assists_b']})")
            discrepancies_found = True
            
        if details:
            dashboard_data.loc[dashboard_data['player_name'] == player, 'discrepancy_flag'] = True
            dashboard_data.loc[dashboard_data['player_name'] == player, 'discrepancy_details'] = "; ".join(details)

    if not discrepancies_found:
        print("Feeds are consistent. No discrepancies found.")

    # Save the unified data for the Excel dashboard
    # This uses Feed A as the "source of truth" and adds flags
    dashboard_data.to_csv(DASHBOARD_DATA_PATH, index=False)

def main():
    """Main function to run the monitoring loop."""
    print("--- Starting Live NBA Data Monitoring and Verification ---")
    initialize_log_file()
    
    while True:
        print(f"\nChecking feeds at {datetime.now().strftime('%H:%M:%S')}...")
        cross_verify_feeds()
        time.sleep(MONITOR_INTERVAL_SECONDS)

if __name__ == "__main__":
    main()
