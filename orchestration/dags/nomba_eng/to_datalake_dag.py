from datetime import timedelta

from airflow.providers.smtp.operators.smtp import EmailOperator
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator
from airflow.sdk import DAG
from pendulum import datetime

from nomba_eng.include.to_datalake import mongodb_tos3, postgresSource_tos3
from nomba_eng.include.mongo_pipeline import write_to_mongo
from airflow.providers.mongo.hooks.mongo import MongoHook

default_args = {
    "owner": "Nombaa",
    "start_date": datetime(2025, 12, 16),
    "retries": 3,
    "retry_delay": timedelta(minutes=1),
}

with DAG(
    dag_id="to_datalake",
    default_args=default_args,
    schedule=None,
):
    to_mongo = PythonOperator(
        task_id="to_mongo",
        python_callable=write_to_mongo
    )

    mongo_s3 = PythonOperator(
        task_id="mongo_s3",
        python_callable=mongodb_tos3,
    )

    # postgres_s3 = PythonOperator(
    #     task_id="postgres_s3",
    #     python_callable=postgresSource_tos3,
    # )

#     send_notification = EmailOperator(
#         task_id="send_notification",
#         to=["ahardysuccess@gmail.com", "taofeecohadesanu@gmail.com"],
#         subject="FETCH DATA TO NOMBA-ENG S3 LAKE",
#         html_content="""
#         <h3> Loading data to datalake notice </h3>
#         <p>This is the status of your job from airflow</p>
#         <p>Regards.</p>
# """,
#         conn_id="smtp_id",
#     )
    mongo_s3
