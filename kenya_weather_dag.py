from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
from weather_fetcher import batch_load_historical_data, stream_current_weather

default_args = {
    "owner": "airflow",
    "depends_on_past": False,
    "email_on_failure": False,
    "email_on_retry": False,
    "retries": 1,
    "retry_delay": timedelta(minutes=5),
}

with DAG(
    "kenya_weather_pipeline",
    default_args=default_args,
    description="Pipeline for historical and streaming Kenya weather data",
    schedule="@hourly",
    start_date=datetime(2025, 6, 23),
    catchup=False,
) as dag:
    batch_load = PythonOperator(
        task_id="batch_load_historical_data",
        python_callable=batch_load_historical_data,
    )

    stream_task = PythonOperator(
        task_id="stream_current_weather",
        python_callable=stream_current_weather,
    )

    batch_load >> stream_task