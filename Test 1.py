import os
from dotenv import load_dotenv


import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

load_dotenv()

url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST"),
    port=os.getenv("DB_PORT"),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(url)

query = """
SELECT
    p.policy_id,
    p.policyholder_name,
    p.age,
    p.annual_premium,
    p.policy_type
FROM policies AS p;
"""

df = pd.read_sql(query,engine)

print(df)
