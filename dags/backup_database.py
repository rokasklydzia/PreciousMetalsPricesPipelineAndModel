from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import timedelta
from Source.Backup.backup_postgres import backup_postgres  # Import the backup function

# Define default arguments
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
    'start_date': days_ago(1),  # Adjust as needed
}

# Define the DAG
dag = DAG(
    'postgres_backup_dag',
    default_args=default_args,
    description='PostgreSQL Backup DAG every 6 hours, keeping the last 20 backups',
    schedule_interval='0 */6 * * *',  # Run every 6 hours
    catchup=False,
)

# Define the backup task
backup_task = PythonOperator(
    task_id='backup_postgres_task',
    python_callable=backup_postgres,  # The backup function to call
    dag=dag,
)

backup_task
