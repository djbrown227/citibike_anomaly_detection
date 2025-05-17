import pandas as pd
from detect_flips import detect_station_flipping

def main():
    # Load the parsed data
    df = pd.read_csv('data/parsed_station_data.csv')

    # Run anomaly detection
    anomalies = detect_station_flipping(df)
    anomolies_freq = detect_unusual_flip_frequency(df)
    anomalies_dist = detect_local_synchronized_flips(df)
    # Output anomalies
    print(anomalies)

    # Optional: Save anomalies to a CSV file
    anomalies.to_csv('data/anomalies_detected.csv', index=False)
    anomolies_freq.to_csv('data/anomalies_detected_freq.csv', index=False)
    anomalies_dist.to_csv('data/anomalies_detected_dist.csv', index=False) 

if __name__ == '__main__':
    main()
