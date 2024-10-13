import os
import subprocess
from datetime import datetime
from airflow.hooks.postgres_hook import PostgresHook

def backup_postgres():
    # Use Airflow's PostgresHook to get connection details
    hook = PostgresHook(postgres_conn_id="Postgres_connector_BITE_Wired")
    connection = hook.get_connection(hook.postgres_conn_id)
    
    db_user = connection.login
    db_name = connection.schema
    db_host = connection.host
    db_port = connection.port
    db_password = connection.password

    # Define backup parameters
    backup_dir = "./backup"
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    backup_file = f"{backup_dir}/{db_name}-backup-{timestamp}.sql.gz"

    # Ensure backup directory exists
    os.makedirs(backup_dir, exist_ok=True)

    # Perform the backup using pg_dump
    try:
        env = os.environ.copy()
        env['PGPASSWORD'] = db_password

        with open(backup_file, 'wb') as f_out:
            subprocess.run(
                ["pg_dump", "-U", db_user, "-d", db_name, "-h", db_host, "-p", str(db_port)],
                stdout=f_out,
                check=True,
                env=env
            )
    except subprocess.CalledProcessError as e:
        raise Exception(f"Backup failed: {e}")

    # Find and remove old backups, keeping only the last 20
    backups = sorted(os.listdir(backup_dir), reverse=True)
    for old_backup in backups[20:]:
        os.remove(os.path.join(backup_dir, old_backup))

    print(f"Backup completed and saved as {backup_file}")
