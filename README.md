## Airflow Example Pipeline With Docker

Repository provides an example of runnig Apache Airflow in Docker for ML pipelines (etl, train, batch inference)

## Usage

1. Install docker and docker compose
2. Clone this repo

    ```bash
    git clone https://github.com/galeriandavid/pipeline-orchestration.git
    ```
3. Move to repo

    ```bash
    cd pipeline-orchestration
    ```

4. Configure user id for the docker-compose (for Linux users)

    ```
    echo -e "AIRFLOW_UID=$(id -u)" > .env
    ```

5. Start Airflow:

    ```bash
    docker compose up
    ```

6. Access the Airflow web interface in your browser at http://localhost:8080.

7. Find dags with tag `home_work` and activate them. Results appears in `data` and `model` folders

8. When you are finished working and want to clean up your environment, run:

    ```bash
    docker compose down --volumes --rmi all
    ```
