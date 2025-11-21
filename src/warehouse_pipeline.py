import logging
import time
import psycopg2
import pandas as pd
from sqlalchemy import create_engine
from datetime import datetime, timedelta
from pymongo import MongoClient
import subprocess
import boto3
import awswrangler as wr


from utils.config import DBNAME, WH_HOST, HOST, WH_LOG_FILE, USER, PASS, WH_PORT, PORT, DB, DATA_DIR, CONNECTION_STRING

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=WH_LOG_FILE,
    format='%(asctime)s:%(levelname)s:%(message)s',
    level=logging.INFO
    )

# def db_setup() -> None:
#     """ Function to setup postgresql schema and table """
#     conn = None
#     try:
#         logging.info("Initializing database setup...")
#         conn = psycopg2.connect(
#             database=DBNAME,
#             user=USER,
#             password=PASS,
#             host=WH_HOST,
#             port=WH_PORT
#             )

#         # Open a cursor to perform database operations
#         cur = conn.cursor()
#         # Execute query

#         conn.commit()
#     except Exception as e:
#         logging.info(f"An error has occurred:", {e})
#     finally:
#         if conn:
#             cur.close()
#             conn.close()
#             logging.info("Connection closed.")


postgres_src_engine = create_engine(f"postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{DBNAME}")

def from_mongodb():
    client = MongoClient(CONNECTION_STRING)
    collection = client[DBNAME].get_collection("users")
    return pd.DataFrame(collection.find({}))


# mongo_data_file = f"user_collections{time_stamp}.csv"

# subprocess.run([
#     "mongoexport", \
#     "--collection=users", \
#     f"--db={DBNAME}", \
#     f"--out={DATA_DIR}/{mongo_data_file}", \
#     f"--username={MONGO_USER}", \
#     f"--password={MONGO_PASS}", \
#     "--authenticationDatabase=admin"
#     ], capture_output=True)


def from_postgres_source():
    #connect to source
    src_table1 = pd.read_sql_table(
        table_name="savings_plan",
        schema="bronze",
        con=postgres_src_engine,
    )

    src_table2 = pd.read_sql_table(
        table_name="savings_transaction",
        schema="bronze",
        con=postgres_src_engine,
    )
    
    return src_table1, src_table2

tables = {
    "savings_plan": from_postgres_source()[0],
    "savings_transaction": from_postgres_source()[1],
    "users": from_mongodb()
    }

#  Writing to storage staging layer

BUCKET = "nomba-dumpss"
time_stamp = datetime.now().strftime("%Y-%m-%d,%H-%M-%S")
for table, table_data in tables.items():
    wr.s3.to_csv(
        df=table_data,
        path=f's3://{BUCKET}/source_data_dumps/{time_stamp}{table}.csv',
        dataset=False,
        )



# # Writing to local postgres warehouse
# if __name__ == "__main__":
#     try:
#         table1.to_sql(
#         name="savings_plan",
#         schema="staging",
#         con=postgres_des_engine,
#         index=False,
#         if_exists="append",
#         )
#         logging.info(f"Written {len(table1)} records from table1 to warehouse!")

#         table2.to_sql(
#         name="savings_transaction",
#         schema="staging",
#         con=postgres_des_engine,
#         index=False,
#         if_exists="append",
#         )
#         logging.info(f"Written {len(table2)} records from table2 to warehouse!")

#         table3.to_sql(
#         name="users",
#         schema="staging",
#         con=postgres_des_engine,
#         index=False,
#         if_exists="append",
#         )
        
#         logging.info(f"Written {len(table3)} records from {mongo_data_file} to warehouse!")
#     except Exception as e:
#         logging.error(e)
