import pandas as pd
import numpy as np
from math import radians, cos, sin, asin, sqrt

def haversine(lon1, lat1, lon2, lat2):
    """
    Calculate the great-circle distance (in km) between two points.
    """
    R = 6371  # Earth radius in kilometers
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])
    dlon, dlat = lon2 - lon1, lat2 - lat1
    a = sin(dlat/2)**2 + cos(lat1) * cos(lat2) * sin(dlon/2)**2
    return 2 * R * asin(sqrt(a))

def detect_local_synchronized_flips(df, radius_km=0.5, min_sync=3):
    """
    Detects synchronized flips among stations within a certain geographic radius.
    Flags timestamp+station clusters with suspicious flip coordination.
    """
    df = df.sort_values(['station_id', 'timestamp']).copy()

    # Calculate percent_full
    if 'percent_filled' in df.columns:
        df['percent_full'] = df['percent_filled'] / 100.0
    else:
        df['percent_full'] = df['num_bikes_available'] / df['capacity']

    # Determine state
    df['state'] = 'normal'
    df.loc[df['percent_full'] >= 0.9, 'state'] = 'full'
    df.loc[df['percent_full'] <= 0.2, 'state'] = 'empty'

    # Detect flips
    df['flip'] = df['state'] != df.groupby('station_id')['state'].shift(1)
    df['flip'] = df['flip'] & df['state'].isin(['full', 'empty'])

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    flip_events = df[df['flip']].copy()

    # Prepare a structure to collect anomalies
    anomaly_rows = []

    # Group by timestamp to analyze flips at each moment
    for timestamp, group in flip_events.groupby('timestamp'):
        group = group.reset_index(drop=True)

        # Compare each station to all others in that time slice
        for i, row_i in group.iterrows():
            nearby = []

            for j, row_j in group.iterrows():
                if row_i['station_id'] == row_j['station_id']:
                    continue

                dist = haversine(
                    row_i['longitude'], row_i['latitude'],
                    row_j['longitude'], row_j['latitude']
                )
                if dist <= radius_km:
                    nearby.append(row_j['station_id'])

            if len(nearby) + 1 >= min_sync:  # +1 for the current station itself
                anomaly_rows.append(row_i)

    anomalies = pd.DataFrame(anomaly_rows)
    return anomalies[[
        'timestamp', 'station_id', 'station_name', 'latitude', 'longitude', 'percent_full', 'state'
    ]]
