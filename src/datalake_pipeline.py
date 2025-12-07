import logging
from datetime import datetime, timedelta

import awswrangler as wr
import pandas as pd
from pymongo import MongoClient
from sqlalchemy import create_engine

from utils.config import CONNECTION_STRING, DBNAME, HOST, PASS, PORT, USER, WH_LOG_FILE

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=WH_LOG_FILE,
    format="%(asctime)s:%(levelname)s:%(message)s",
    level=logging.INFO,
)


postgres_src_engine = create_engine(
    f"postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{DBNAME}"
)
BUCKET = "nomba-dumpss"
time_stamp = datetime.now().strftime("%Y-%m-%d,%H-%M-%S")


def mongodb_tos3() -> None:
    """Function to extract from postgresql to s3 bucket"""

    client = MongoClient(CONNECTION_STRING)
    collection = client[DBNAME].get_collection("users")
    users_data = pd.DataFrame(
        collection.find({"updated_at": {"$gt": datetime.now() - timedelta(hours=24)}})
    )
    wr.s3.to_csv(
        df=users_data,
        path=f"s3://{BUCKET}/source_data_dumps/{time_stamp}_users.csv",
        dataset=False,
    )
    logging.info(f"Written {len(users_data)} records to staging layer!")


def postgresSource_tos3() -> None:
    """Function to extract from postgresql to s3 bucket"""

    src_table1 = pd.read_sql(
        sql="""
        SELECT * FROM bronze.savings_plan
        WHERE updated_at > now() - interval '24 hours'
        """,
        con=postgres_src_engine,
    )

    src_table2 = pd.read_sql(
        sql="""
        SELECT * FROM bronze.savings_transaction
        WHERE updated_at > now() - interval '24 hours'
        """,
        con=postgres_src_engine,
    )

    tables = {"savings_plan": src_table1, "savings_transaction": src_table2}

    # Load to staging layer
    for table, table_data in tables.items():
        wr.s3.to_csv(
            df=table_data,
            path=(f"s3://{BUCKET}/source_data_dumps/" f"{time_stamp}{table}.csv"),
            dataset=False,
        )
        logging.info(
            f"Written {len(table_data)} records from" f"{table} to staging layer!"
        )


if __name__ == "__main__":
    mongodb_tos3()
    postgresSource_tos3()
