import speedtest
from datetime import datetime

def perform_speedtest():
    """
    Perform speedtest and return results as a dictionary.
    """
    st = speedtest.Speedtest()
    print("\nConnected to the Speedtest client.")

    # Select the best server
    print("Selecting the best server...")
    st.get_best_server()

    # Measure download speed
    print("Measuring download speed...")
    download_speed = st.download()
    print("Download speed measurement completed.")

    # Measure upload speed
    print("Measuring upload speed...")
    upload_speed = st.upload()
    print("Upload speed measurement completed.")

    # Get ping
    ping = st.results.ping
    print("Ping (latency) calculated.")

    # Prepare results
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    results = st.results.dict()
    results['timestamp'] = timestamp

    print("\n--- Speed Test Results ---")
    print(f"Timestamp: {timestamp}")
    print(f"Ping: {ping:.2f} ms")
    print(f"Download Speed: {download_speed / 1_000_000:.2f} Mbps")
    print(f"Upload Speed: {upload_speed / 1_000_000:.2f} Mbps")

    return results
