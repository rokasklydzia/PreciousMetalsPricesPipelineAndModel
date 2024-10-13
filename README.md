# Metal Prices Data Pipeline and Machine Learning Forecasting
This project implements an ETL pipeline for fetching, processing, and storing metal price data, followed by a machine learning forecasting model that predicts future prices. The pipeline is orchestrated using Airflow, and the data is stored in a PostgreSQL database.

## Project Overview
### Key Components:
- API Data Fetching: Metal prices for gold, silver, platinum, and palladium are fetched from an external API and stored in a PostgreSQL database.
- ETL Pipeline: The fetched data is inserted into a table called metal_prices_analytics, and the latest 12 entries are moved into metal_prices_ml for machine learning training.
- Machine Learning Model: An ARIMA model is used to forecast future metal prices based on historical data.
- Automated Backup: The PostgreSQL database is backed up every 6 hours with Airflow handling the scheduling and retention policy.
- Airflow DAGs: Airflow manages the scheduling and execution of the ETL pipeline, ML training, and database backups.
## Project Structure
```bash
.
├── dags
│   ├── metal_prices_market_hours_dag.py   # DAG to fetch metal prices and update DB
│   └── backup_dag.py                      # DAG to backup the Postgres database
├── plugins
│   ├── Source
│   │   ├── API
│   │   │   └── api_call_v5.py             # Function to fetch metal prices from API and store in DB
│   │   └── Models
│   │       └── Model.py                   # Machine learning model for forecasting metal prices
│   └── Backup
│       └── backup_postgres.py             # Function to backup PostgreSQL database
└── docker-compose.yaml                    # Airflow, PostgreSQL, and other services configuration
```
## Getting Started
### 1. Prerequisites
Make sure you have the following installed:

- Docker and Docker Compose
- Python 3.9 or higher
- PostgreSQL
- Apache Airflow
### 2. Installation
#### 1. Clone the repository:

```bash
git clone https://github.com/TuringCollegeSubmissions/roklydz-DE2.4.1.git
cd roklydz-DE2.4.1
```
#### 2. Build the Airflow environment with Docker Compose:

```bash
docker-compose up --build
```
#### 3. Install Python Dependencies:

You will need to install dependencies in your environment:

```bash
pip install -r requirements.txt
```
#### 4. Configure PostgreSQL Database:

Make sure your PostgreSQL database is set up properly. You should create a database called MetalPrices. The connection parameters (host, port, user, and password) should be updated in the api_call_v4.py and backup_postgres.py scripts if necessary.

Example PostgreSQL setup:

```bash
CREATE DATABASE MetalPrices;
```
Make sure the Postgres service is running in Docker.

### 3. Airflow Configuration
#### 1. Set Up Connections:

In the Airflow Admin panel, add a Postgres connection under Admin -> Connections. Use the following parameters:

- Connection ID: PostgresDesktop
- Host: localhost or the IP address of your Postgres container.
- Port: 5432 (default)
- Login: postgres
- Password: your Postgres password
- Database: MetalPrices
### 2. Deploy DAGs:

Make sure your DAG files (metal_prices_market_hours_dag.py, backup_dag.py) are correctly placed inside the Airflow DAGs folder (dags/).

### 3. Access Airflow:

Once your Docker containers are running, open the Airflow web interface at http://localhost:8080.

#### Activate the DAGs:
![image](https://github.com/user-attachments/assets/d2f74e70-7165-4bfc-b8c1-8b47d0d1534d)

- metal_prices_market_hours_dag: Fetches metal prices and updates metal_prices_analytics and metal_prices_ml.
- backup_dag: Performs backups of the PostgreSQL database every 6 hours.
## Detailed Walkthrough
### 1. API Call to Fetch Metal Prices
The api_call_v5.py script handles the API request to fetch metal prices and store the data into the metal_prices_analytics table. The function get_and_store_metal_prices is executed via an Airflow DAG task, ensuring data is fetched and stored every hour during market hours.

Key data points:

- gold_price -> XAUUSD
- silver_price -> XAGUSD
- platinum_price -> XPTUSD
- palladium_price -> XPDUSD
### 2. Machine Learning Model
The ARIMA model is used to forecast future prices based on the most recent 12 hourly entries from metal_prices_analytics. The model is trained using the Model.py script and is triggered within Airflow for daily forecasts.
![image](https://github.com/user-attachments/assets/78c59a64-261c-44c0-ae4b-7ce2adc470d6)

### 3. Backup Process
The backup_postgres.py script automates the process of creating PostgreSQL backups every 6 hours. The Airflow task ensures only the last 20 backups are stored on disk.

![image](https://github.com/user-attachments/assets/4b4132c2-9fce-4d2b-9611-9ffdb8cf3e01)

## Airflow DAGs
### metal_prices_market_hours_dag
This DAG is responsible for the following tasks:

### 1. Run API Call: Fetches the latest metal prices and stores them in the metal_prices_analytics table.
### 2. Update Metal Prices ML Table: Moves the last 12 records from metal_prices_analytics to metal_prices_ml for machine learning training.
### backup_dag
This DAG handles the database backups. It runs every 6 hours and ensures the retention of the last 20 backups.

## Troubleshooting
### Common Errors:
- Connection Issues: Ensure that your PostgreSQL server is running and the connection parameters are correct in both the Airflow connection and the Python scripts.
- Dependency Issues: If you encounter issues with dependencies (e.g., pg_dump, pmdarima), ensure you have installed all required packages and libraries.
### Debugging Airflow Logs:
To view detailed logs of DAG runs, navigate to the Airflow web interface, select your DAG, and inspect task logs.

## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Built with
- Apache Airflow for task scheduling and orchestration.
- PostgreSQL for the database used to store and query metal price data.
- PMDARIMA for time-series forecasting with ARIMA.
- MetalPriceAPI for real-time metal price data.

Author: Rokas Klydžia

This README provides an overview of the project, installation steps, and details on how the pipeline operates.
