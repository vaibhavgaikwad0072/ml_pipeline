from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta
import sys
import os

# Add project root to sys.path to allow importing from src
# Assuming DAG is in /dags and we need to import from /src
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
if PROJECT_ROOT not in sys.path:
    sys.path.append(PROJECT_ROOT)

from src.crawler import run_crawler
from src.processor import run_processor
from src.aggregator import run_aggregator

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    'company_content_pipeline',
    default_args=default_args,
    description='A simple pipeline to crawl, process, and aggregate company website content',
    schedule_interval=timedelta(days=1),
    start_date=datetime(2023, 1, 1),
    catchup=False,
    tags=['evaluation'],
) as dag:

    t1_crawl = PythonOperator(
        task_id='crawl_websites',
        python_callable=run_crawler,
    )

    t2_process = PythonOperator(
        task_id='process_content',
        python_callable=run_processor,
    )

    t3_aggregate = PythonOperator(
        task_id='aggregate_metrics',
        python_callable=run_aggregator,
    )

    t1_crawl >> t2_process >> t3_aggregate
