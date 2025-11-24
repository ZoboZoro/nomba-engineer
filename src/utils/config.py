import os
from pathlib import Path

from dotenv import load_dotenv
from pymongo import MongoClient

BASE_DIR = Path(__file__).parent.parent.parent
dotenv_path = f"{BASE_DIR}/.env"

load_dotenv(dotenv_path, verbose=True)

# MongoDB config
MONGO_USER = os.getenv("MONGO_USER")
MONGO_PASS = os.getenv("MONGO_PASS")
CONNECTION_STRING = f"mongodb://{MONGO_USER}:{MONGO_PASS}@localhost:27017/"
client = MongoClient(CONNECTION_STRING)
DB = client["nomba"]
COLLECTION = DB["users"]

# Basic config
SQL_DIR = BASE_DIR / "src" / "sql"
SQL = SQL_DIR.mkdir(exist_ok=True)
SQL_FILE = BASE_DIR / "src" / "sql" / "query.sql"
LOG_DIR = BASE_DIR / "logs"
LOG = LOG_DIR.mkdir(exist_ok=True)
PG_LOG_FILE = LOG_DIR / "postgres_src.log"
WH_LOG_FILE = LOG_DIR / "warehouse_pipeline.log"
MG_LOG_FILE = LOG_DIR / "mongo_src.log"
DATA_DIR = BASE_DIR / "data"
DATA = BASE_DIR.mkdir(exist_ok=True)

# SQL_DB config
USER = os.getenv("PG_USER")
PASS = os.getenv("PG_PASS")
HOST = os.getenv("PG_HOST", "postgres_src")
WH_HOST = os.getenv("PG_HOST", "postgres_des")
DBNAME = os.getenv("DB_NAME")
PORT = int(os.getenv("SRC_PG_PORT", 5432))
WH_PORT = int(os.getenv("DES_PG_PORT", 5432))
