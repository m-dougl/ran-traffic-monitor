```markdown
# RAN Traffic Monitor

This project is a data pipeline setup using Apache Airflow to manage ETL (Extract, Transform, Load) tasks and generate simulated data for monitoring traffic in Radio Access Networks (RAN).

## Project Structure

## Directory and File Descriptions

- **dags/**: Contains the Airflow DAGs.
  - `el_dag.py`: Defines a DAG to extract data from CSV files, transform it, and load it into a database.
  - `simulator_dag.py`: Defines a DAG to generate simulated data for towers and KPIs.
- **data/**: Stores the generated and processed CSV data.
  - `kpis/`: Contains the KPI CSV files.
  - `towers/`: Contains the tower CSV files.
- **logs/**: Contains the Airflow logs.
- **plugins/**: Directory for Airflow plugins.
- **simulator/**: Contains the code to generate simulated data.
  - `ran_simulator.py`: Contains the `TowerDataGenerator` and `KPIDataGenerator` classes to generate simulated data.
- **src/**: Contains the code related to CRUD operations, models, schemas, and database initialization.
  - `crud.py`: Contains functions to create data in the database.
  - `database.py`: Sets up the database connection and initializes the database.
  - `models.py`: Defines the database models.
  - `schemas.py`: Defines the schemas for data validation.
- **.env**: Contains environment variables for database configuration.
- **docker-compose.yml**: Configures the Airflow services, including the scheduler and webserver.
- **Dockerfile**: Defines the Docker image for the project.
- **requirements.txt**: Lists the project dependencies.
- **README.md**: This file, containing the project documentation.

## Setup and Execution

### Prerequisites

- Docker
- Docker Compose

### Setup Steps

1. Clone the repository:
   ```sh
   git clone <REPOSITORY_URL>
   cd ran-traffic-monitor