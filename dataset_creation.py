import fastf1
import pandas as pd 
import os 

def fetch_and_append_event(year, event_name, 
                           session_types=["FP1", "FP2", "FP3", "Q", "R"], 
                           csv_path="data/f1_laps.csv"):
    df_list = []
    
    # Fetch sessions for the specified event
    for session_type in session_types:
        try:
            session = fastf1.get_session(year, event_name, session_type)
            session.load(laps=True)
            laps = session.laps.copy()

            # Add some columns to keep track of the event
            laps["Session"] = session_type
            laps["Year"] = year
            laps["Round"] = session.event.RoundNumber
            laps["EventName"] = session.event.EventName

            df_list.append(laps)
        except Exception as e:
            print(f"Skipping {year} - {event_name} - {session_type} due to error: {e}")

    if not df_list:
        # No data collected, so just return without writing anything
        return

    # Combine all laps for this event
    event_df = pd.concat(df_list, ignore_index=True)

    # Check if the CSV file already exists in your data folder
    if not os.path.exists(csv_path):
        # If the file doesn't exist, create a new one (header included)
        event_df.to_csv(csv_path, index=False)
        print(f"Created new CSV at {csv_path} with data for {event_name} {year}.")
    else:
        # If the file does exist, append data (no header this time)
        event_df.to_csv(csv_path, mode='a', header=False, index=False)
        print(f"Appended data for {event_name} {year} to existing CSV at {csv_path}.")


# Example usage:
# fetch_and_append_event(2025, "Australia")
# fetch_and_append_event(2025, "Bahrain")
