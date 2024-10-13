from airflow import DAG
#from airflow.operators.bash import BashOperator
from airflow.operators.python import PythonOperator
#from airflow.operators import PythonOperator
from airflow.providers.postgres.operators.postgres import PostgresOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from Source.API.api_call_v5 import get_and_store_metal_prices
from Source.Models.Model import Model

# Define default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(1),  # Set a reasonable start date for testing
}

# Define the DAG with a schedule that runs hourly during market hours
dag = DAG(
    'metal_prices_market_hours_dag',
    default_args=default_args,
    description='DAG to run the metal prices API call and store in PostgreSQL during market hours',
    schedule_interval='0 9-16 * * 1-5',  # Runs every hour during market hours, Mon-Fri
    catchup=False  # Prevent backfilling for missed intervals
)

# Task 1: Run the API call to update metal_prices_analytics
run_api_call_script = PythonOperator(
    task_id='run_api_call',
    python_callable=get_and_store_metal_prices,
    dag=dag,
)

# Task 2: Update the metal_prices_ml table with the last 12 entries from metal_prices_analytics
update_ml_table = PostgresOperator(
    task_id='update_metal_prices_ml',
    postgres_conn_id='Postgres_connector_BITE_Wired',  # Ensure this connection is defined in Airflow
    sql="""
        SELECT id, timestamp, gold_price, silver_price, platinum_price, palladium_price
        FROM metal_prices_analytics
        ORDER BY timestamp DESC
        LIMIT 12;
    """,
    dag=dag,
)

# Task 3. Run sample ML model
def run_model():
    model = Model(["XAUUSD", "XAGUSD", "XPTUSD", "XPDUSD"], 12, 1)
    model.train(use_generated_data=False)
    model.save("model1")

run_ml_model = PythonOperator(
    task_id='run_sample_model',
    python_callable=Model,
    dag=dag,
)

# Task 2 should run after Task 1
run_api_call_script >> update_ml_table >> run_ml_model
#run_api_call_script >> run_ml_model
