# anomaly_detection/detect_flips.py

import pandas as pd

def detect_station_flipping(df, full_thresh=0.6, empty_thresh=0.5, flip_window='45min', flip_threshold=3):
    """
    Detects frequent state flips between 'empty' and 'full' within a time window.
    Flags as anomaly if flip count exceeds threshold in that window.
    Also compares current state with states 10, 20, and 30 rows prior within the same station.
    """

    # Sort data
    df = df.sort_values(['station_id', 'timestamp']).copy()

    # Compute percent full
    if 'percent_filled' in df.columns:
        df['percent_full'] = df['percent_filled'] / 100.0
    else:
        df['percent_full'] = df['num_bikes_available'] / df['capacity']

    # Define state
    df['state'] = 'normal'
    df.loc[df['percent_full'] >= full_thresh, 'state'] = 'full'
    df.loc[df['percent_full'] <= empty_thresh, 'state'] = 'empty'

    # Shifts for comparison
    for n in [10, 20, 30]:
        df[f'state_{n}_before'] = df.groupby('station_id')['state'].shift(n)

        # Define a "flip" only if current and past states are 'full' and 'empty' in either order
        df[f'flip_{n}'] = (
            ((df['state'] == 'full') & (df[f'state_{n}_before'] == 'empty')) |
            ((df['state'] == 'empty') & (df[f'state_{n}_before'] == 'full'))
        )

    # Detect immediate flip (lag 1)
    df['prev_state'] = df.groupby('station_id')['state'].shift(1)
    df['flip'] = (
        ((df['state'] == 'full') & (df['prev_state'] == 'empty')) |
        ((df['state'] == 'empty') & (df['prev_state'] == 'full'))
    )

    # Rolling flip count
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)
    df['flip_count'] = df.groupby('station_id')['flip'].rolling(flip_window).sum().reset_index(0, drop=True)

    # Flag anomalies
    df['is_anomaly'] = df['flip_count'] >= flip_threshold

    df.reset_index(inplace=True)

    return df[df['is_anomaly'] == True][[
        'timestamp', 'station_id', 'station_name', 'percent_full', 'state',
        'state_10_before', 'flip_10',
        'state_20_before', 'flip_20',
        'state_30_before', 'flip_30',
        'flip_count'
    ]]
