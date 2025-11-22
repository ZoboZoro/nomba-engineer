import logging
import random
from datetime import datetime, timedelta

import pandas as pd
from faker import Faker
from random_timestamp import random_timestamp
from sqlalchemy import create_engine

from utils.config import DBNAME, HOST, PASS, PG_LOG_FILE, PORT, USER

logger = logging.getLogger(__name__)
logging.basicConfig(
    filename=PG_LOG_FILE,
    format='%(asctime)s:%(levelname)s:%(message)s',
    level=logging.INFO
    )

# Initiate faker object
fake = Faker()


#  Savings plan
def generate_plans(no_of_records):
    plans_record = []
    start_date = random_timestamp(year=2025)
    end_date = start_date + timedelta(days=random.randint(30, 365))
    product_type = ["fixed", "target", "flex"]
    frequency = ["daily", "weekly", "monthly"]

    for _ in range(no_of_records):
        savings_plan = {
            "plan_id": fake.uuid4(),
            "product_type": random.choice(product_type),
            "customer_uid": fake.uuid4(),
            "amount": random.randrange(300000, 1000000),
            "frequency": random.choice(frequency),
            "start_date": start_date,
            "end_date": end_date,
            "status": random.choice(["active", "completed"]),
            "created_at": random_timestamp(2025),
            "updated_at": datetime.now(),
            "deleted_at": None,
                }
        plans_record.append(savings_plan)
    plan_df = pd.DataFrame(plans_record)
    return plan_df


# Transactions
def generate_transactions(plan_ids, no_of_txns):
    transactions = []
    sides = ["buy", "sell"]
    for id in plan_ids:
        for _ in range(no_of_txns):
            transaction = {
                "txn_id": fake.uuid4(),
                "plan_id": id,
                "amount": random.randrange(300000, 1000000),
                "currency": fake.currency_code(),
                "side": random.choice(sides),
                "rate": round(random.uniform(0.5, 2.0), 4),
                "txn_timestamp": random_timestamp(year=2025),
                "updated_at": datetime.now(),
                "deleted_at": None
            }
            transactions.append(transaction)
    txn_df = pd.DataFrame(transactions)
    return txn_df


if __name__ == "__main__":
    plans = generate_plans(100)
    savings_txn = generate_transactions(plans.plan_id, 50)
    try:
        engine = create_engine(
            f"postgresql+psycopg2://{USER}:{PASS}@{HOST}:{PORT}/{DBNAME}"
            )

        # Write to savings_plan table
        plans.to_sql(
            name="savings_plan",
            con=engine,
            schema="bronze",
            if_exists="append",
            index=False
            )
        logging.info(f"Written {len(plans)} records to plans table!")

        # Write to transactions table
        savings_txn.to_sql(
            name="savings_transaction",
            con=engine,
            schema="bronze",
            if_exists="append",
            index=False
            )
        logging.info(
            f"Written {len(savings_txn)} records to savings_transaction table!"
            )
    except Exception as e:
        logging.error(e)
