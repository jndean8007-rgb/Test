import os
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine

DATA_FILE = Path("C:/Users/rosie/Downloads/wkcomp_pos_98-07.csv")

database_url = URL.create(
    drivername = 'postgresql+psycopg',
    host = os.getenv('DB_HOST'),
    username = os.getenv('DB_USER'),
    password = os.getenv('DB_PASSWORD'),
    port = os.getenv('DB_PORT'),
    database = os.getenv('DB_NAME'),
)

engine = create_engine(database_url)

claims = pd.read_csv(DATA_FILE)

claims.columns = claims.columns.str.strip().str.lower().str.replace(' ', '_').str.replace(r"[^a-z0-9_]","",regex=True)

claims.to_sql(name='raw_claims', con=engine, index=False, if_exists='replace', method="multi", chunksize=10000)