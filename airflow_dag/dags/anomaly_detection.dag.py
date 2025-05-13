# airflow_dag/dags/anomaly_detection.dag.py

from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import os
import pandas as pd

from anomoly_detection.data_pipeline import parse_log_file
from anomoly_detection.detect_flips import detect_flips
from anomoly_detection.output_results import save_results

DATA_PATH = os.path.join(os.path.dirname(__file__), '../../data/station_data_1.log')
RESULTS_PATH = os.path.join(os.path.dirname(__file__), '../../data/anomaly_results.csv')

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2025, 5, 8),
}

dag = DAG(
    'citibike_anomaly_detection',
    default_args=default_args,
    schedule_interval=None,  # Trigger manually or as needed
    catchup=False,
    description='Detect anomalies in CitiBike data',
)

def transform_data():
    df = parse_log_file(DATA_PATH)
    df.to_csv('/tmp/transformed_station_data.csv', index=False)
    return True

from anomoly_detection.detect_flips import detect_station_flipping

def run_anomaly_detection():
    df = pd.read_csv('/tmp/transformed_station_data.csv', parse_dates=['timestamp'])
    anomalies = detect_station_flipping(df)
    save_results(anomalies, RESULTS_PATH)
    return True


transform_task = PythonOperator(
    task_id='transform_log_data',
    python_callable=transform_data,
    dag=dag,
)

detect_task = PythonOperator(
    task_id='detect_anomalies',
    python_callable=run_anomaly_detection,
    dag=dag,
)

transform_task >> detect_task
