from pathlib import Path

from airflow.sdk import Variable
# from dotenv import load_dotenv
from pymongo import MongoClient
from nomba_eng.utils import variables
from nomba_eng.utils.variables import DB_NAME, MONGO_HOST

variable = variables
BASE_DIR = Path(__file__).parent.parent.parent
# dotenv_path = f"{BASE_DIR}/.env"

# load_dotenv(dotenv_path, verbose=True)

# MongoDB config
MONGO_USER = Variable.get("MONGO_USER")
MONGO_PASS = Variable.get("MONGO_PASS")
CONNECTION_STRING = f"mongodb://{MONGO_USER}:{MONGO_PASS}@{MONGO_HOST}:27017/"
client = MongoClient(CONNECTION_STRING)
DB = client[DB_NAME]
COLLECTION = DB["users"]

# Basic config
SQL_DIR = BASE_DIR / "sql"
SQL = SQL_DIR.mkdir(exist_ok=True)
SQL_FILE = BASE_DIR / "sql" / "query.sql"
LOG_DIR = BASE_DIR / "logs"
LOG = LOG_DIR.mkdir(exist_ok=True)
PG_LOG_FILE = LOG_DIR / "postgres_src.log"

DATALAKE_LOG_FILE = LOG_DIR / "datalake_pipeline.log"
MG_LOG_FILE = LOG_DIR / "mongo_src.log"
DATA = BASE_DIR.mkdir(exist_ok=True)

# SQL_DB config
USER = Variable.get("PG_USER")
PASS = Variable.get("PG_PASS")
HOST = Variable.get("PG_HOST", "postgres_src")
DBNAME = Variable.get("DB_NAME")
PG_PORT = int(Variable.get("SRC_PG_PORT", 5432))
