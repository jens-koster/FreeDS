from apache_airflow_client.client.api.dag_run_api import DagRunApi
from apache_airflow_client.client.api.task_instance_api import (
    TaskInstanceApi,
)
from apache_airflow_client.client.api_client import ApiClient
from apache_airflow_client.client.configuration import Configuration
from apache_airflow_client.client.model.dag_run import DAGRun


def get_run_result() -> None:
    # Configure your Airflow instance
    configuration = Configuration(host="http://localhost:8080/api/v1", username="admin", password="your-password")

    with ApiClient(configuration) as api_client:
        dag_id = "test_parallel_tasks"

        dag_run_api = DagRunApi(api_client)
        task_instance_api = TaskInstanceApi(api_client)

        # Get latest DAG run
        dag_runs = dag_run_api.get_dag_runs(dag_id=dag_id, limit=1, order_by="-execution_date")
        if not dag_runs.dag_runs:
            print("No DAG runs found.")
        else:
            run = dag_runs.dag_runs[0]
            print(f"Run ID: {run.dag_run_id}, State: {run.state}, Exec Date: {run.execution_date}")

            # Get task instances for this DAG run
            task_instances = task_instance_api.get_task_instances(dag_id=dag_id, dag_run_id=run.dag_run_id)

            for ti in task_instances.task_instances:
                print(f"Task: {ti.task_id} - State: {ti.state}")


def trigger_dag_run() -> None:
    # Setup connection
    configuration = Configuration(host="http://localhost:8080/api/v1", username="admin", password="your-password")

    with ApiClient(configuration) as api_client:
        dag_run_api = DagRunApi(api_client)

        dag_id = "test_parallel_tasks"

        # Trigger the DAG
        run = dag_run_api.post_dag_run(dag_id=dag_id, dag_run=DAGRun(conf={"reason": "triggered via API"}))

        print(f"Triggered run_id: {run.dag_run_id} at {run.execution_date}")
