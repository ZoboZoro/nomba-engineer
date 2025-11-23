import logging
from datetime import datetime

from faker import Faker

from utils.config import COLLECTION, DBNAME, MG_LOG_FILE

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=MG_LOG_FILE,
    format='%(asctime)s:%(levelname)s:%(message)s',
    level=logging.INFO
    )

fake = Faker()

full_document = []

for _ in range(500):
    user = {
      "Uid": fake.uuid4(),
      "firstName": fake.first_name(),
      "lastName": fake.last_name(),
      "occupation": fake.job(),
      "state":  fake.state(),
      "updated_at": datetime.now()
    }
    full_document.append(user)

logging.info(f"writing records to database: {DBNAME}...")

COLLECTION.insert_many(full_document)
logging.info(
   f"writen records of {len(full_document)} to database: {DBNAME}..."
   )
