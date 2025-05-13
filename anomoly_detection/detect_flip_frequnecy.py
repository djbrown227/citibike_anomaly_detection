import pandas as pd

def detect_unusual_flip_frequency(df, flip_window='45min', z_thresh=3):
    """
    Detects flip anomalies based on z-score threshold per station.
    Flags if a station flips significantly more than its usual pattern.
    Only counts flips from empty ↔ full as valid.
    """
    df = df.sort_values(['station_id', 'timestamp']).copy()

    # Calculate percent_full
    if 'percent_filled' in df.columns:
        df['percent_full'] = df['percent_filled'] / 100.0
    else:
        df['percent_full'] = df['num_bikes_available'] / df['capacity']

    # Define state
    df['state'] = 'normal'
    df.loc[df['percent_full'] >= 0.9, 'state'] = 'full'
    df.loc[df['percent_full'] <= 0.2, 'state'] = 'empty'

    # Detect strict flips (empty <-> full only)
    df['prev_state'] = df.groupby('station_id')['state'].shift(1)
    df['flip'] = (
        ((df['state'] == 'full') & (df['prev_state'] == 'empty')) |
        ((df['state'] == 'empty') & (df['prev_state'] == 'full'))
    )

    # Convert to datetime and rolling index
    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df.set_index('timestamp', inplace=True)

    # Rolling flip count per station
    df['flip_count'] = df.groupby('station_id')['flip'].rolling(flip_window).sum().reset_index(0, drop=True)

    # Z-score per station
    flip_stats = df.groupby('station_id')['flip_count'].agg(['mean', 'std']).rename(columns={'mean': 'mu', 'std': 'sigma'})
    df = df.join(flip_stats, on='station_id')
    df['z_score'] = (df['flip_count'] - df['mu']) / df['sigma']

    # Flag anomalies
    df['is_anomaly'] = df['z_score'] > z_thresh
    df.reset_index(inplace=True)

    return df[df['is_anomaly'] == True][[
        'timestamp', 'station_id', 'station_name', 'percent_full', 'state', 'flip_count', 'z_score'
    ]]
