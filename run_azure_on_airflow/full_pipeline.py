from airflow import DAG
from airflow.utils.dates import days_ago
from airflow.providers.microsoft.azure.operators.data_factory import AzureDataFactoryRunPipelineOperator
from airflow.providers.databricks.operators.databricks import DatabricksSubmitRunOperator

# Default DAG arguments
default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
}

# Define the DAG
with DAG(
    'combined_adf_databricks_dag',
    default_args=default_args,
    description='DAG to trigger ADF pipeline and then run Databricks notebook',
    schedule_interval=None,  # Set to desired schedule, None means manual triggering
    start_date=days_ago(1),
    catchup=False,  # Disable catchup to only run the latest instance
) as dag:

    # Task to trigger the ADF pipeline
    trigger_adf_pipeline = AzureDataFactoryRunPipelineOperator(
        task_id='trigger_adf_pipeline',
        pipeline_name='CopyCsvToBronzeLayer',  # Your ADF pipeline name
        factory_name='rsgadfnew',              # Your ADF instance name
        resource_group_name='RSG_RESOURCE_GROUP',  # Your Azure Resource Group
        azure_data_factory_conn_id='azure_data_factory_default',  # Connection ID set in Airflow UI
    )

    # Define the notebook parameters to run on the existing Databricks cluster
    notebook_task = {
        'existing_cluster_id': '1025-225233-assr4g9v',  # Updated Cluster ID
        'notebook_task': {
            'notebook_path': '/Workspace/Users/rohit2101991@gmail.com/rsgfirstNB',
            'base_parameters': {
                'param1': 'value1',
                'param2': 'value2'
            }
        }
    }

    # Task to run the Databricks notebook
    run_databricks_notebook = DatabricksSubmitRunOperator(
        task_id='run_databricks_notebook',
        json=notebook_task,
        databricks_conn_id='databricks_default',  # Databricks connection ID
    )

    # Set task dependencies: ADF pipeline should run first, then Databricks notebook
    trigger_adf_pipeline >> run_databricks_notebook


