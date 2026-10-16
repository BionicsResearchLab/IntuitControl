from cortexAPI.cortex import Cortex
import os
import time
from cortexAPI.sub_data import Subscribe

# Main entry point for the Cortex API
def main():
    # Initialize the Cortex interface
    cortex_session = Cortex(client_id=os.environ['CLIENT_ID'], client_secret=os.environ['CLIENT_SECRET'])
    eeg_data_sub = Subscribe(app_client_id=os.environ['CLIENT_ID'], app_client_secret=os.environ['CLIENT_SECRET'])
    eeg_data_sub.start(streams=['eeg'])

    # Keep the script running to continue receiving EEG data
    # Available Data Streams
    
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("Stopping EEG data subscription.")
        eeg_data_sub.unsub(streams=['eeg'])
        cortex_session.close()
        print("Cortex session closed.")
        print("EEG data subscription stopped.")
        print("Exiting program.")

if __name__ == "__main__":
    main()