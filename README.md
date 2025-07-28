# Live NBA Game Data Verification System

This project is a simulation of a real-time data verification workflow for live NBA games, designed to showcase the key skills and mindset required for a **Data Coordinator Associate** role at a company like DraftKings.

The system uses Python to generate two distinct, "live" data feeds for a mock NBA game. A second Python script continuously monitors these feeds, cross-verifies player stats, and logs any discrepancies. This data is then fed into a custom Excel dashboard that provides a live, color-coded view of the game's data integrity.

## Core Skills Demonstrated

* **Real-Time Data Monitoring:** The project directly simulates the primary responsibility of monitoring and verifying live data feeds during a high-intensity game scenario.
* **Exceptional Attention to Detail:** The core logic of the `monitor_nba_data.py` script is built around identifying and flagging even minor discrepancies in points, rebounds, and assists between sources.
* **Data Discrepancy Resolution:** The system not only identifies issues but also logs them in `discrepancy_log.csv`, providing a clear, timestamped record for analysis and resolution.
* **Process Improvement & Streamlining:** The project includes a `Data Discrepancy Log & Analysis` template, demonstrating the ability to analyze logged issues, identify patterns (e.g., one feed is consistently slow), and recommend process improvements to internal teams.
* **Experience with Spreadsheets and Data Tools:** A custom Excel dashboard is built using Power Query for automated data refreshing and conditional formatting to provide an intuitive, at-a-glance view of data health.
* **Understanding of Sports Data Feeds:** The project simulates the behavior of real-world data feeds, including latency and potential for error, showing a practical understanding of the challenges in live event tracking.
* **Deep NBA Knowledge:** The underlying data model and simulated events (2-pointers, 3-pointers, assists, rebounds) are based on the fundamental mechanics of an NBA game.

## Project Workflow

1.  **`generate_nba_feeds.py`:** This script runs in a dedicated terminal and acts as the "live game engine." It generates game events every few seconds and updates two separate data feeds (`feed_A.csv` and `feed_B.csv`), intentionally introducing slight delays and occasional errors to `feed_B.csv` to create a realistic verification challenge.
2.  **`monitor_nba_data.py`:** This script runs in a second terminal, acting as the "Data Coordinator." It continuously reads both feeds, compares them line-by-line, and produces two outputs:
    * `live_dashboard_data.csv`: A clean, unified data source for the dashboard, with flags for any discrepancies.
    * `discrepancy_log.csv`: A persistent log of every mismatch found.
3.  **`Live_NBA_Dashboard.xlsx`:** This Excel file connects to `live_dashboard_data.csv`. It uses Power Query to refresh automatically every minute and uses conditional formatting to highlight players with data discrepancies in real-time.

## How to Run This Project

### Prerequisites

* Python 3.9+
* Microsoft Excel (2016 or newer / Microsoft 365)

### Setup and Installation

1.  **Clone the repository:**
    ```bash
    git clone [https://github.com/YOUR_USERNAME/Live-NBA-Data-Verification.git](https://github.com/YOUR_USERNAME/Live-NBA-Data-Verification.git)
    cd Live-NBA-Data-Verification
    ```
2.  **Create and activate a Python virtual environment:**
    ```bash
    python -m venv venv
    # On Windows: .\venv\Scripts\activate
    # On macOS/Linux: source venv/bin/activate
    ```
3.  **Install dependencies:**
    ```bash
    pip install pandas numpy
    ```

### Running the Simulation

1.  **Start the Data Feeds:**
    * Open a new terminal in your project directory.
    * Activate the venv.
    * Run the generator: `python generate_nba_feeds.py`
    * **Leave this terminal running.**

2.  **Start the Monitoring Script:**
    * Open a **second, separate terminal**.
    * Activate the venv.
    * Run the monitor: `python monitor_nba_data.py`
    * **Leave this terminal running.**

3.  **Open the Excel Dashboard:**
    * Follow the instructions in the **"Excel Dashboard Guide for Live NBA Data"** to build your dashboard.
    * Once built, open the Excel file. The data will automatically refresh every minute, highlighting discrepancies as they are found by the monitoring script.