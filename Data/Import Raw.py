import os
from pathlib import Path


import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

ENV_FILE = Path('C:/Users/rosie/PycharmProjects/Git Testing/.env')

print("Script folder:", Path(__file__).resolve().parent)
print(".env path:", ENV_FILE)
print(".env exists:", ENV_FILE.exists())

load_dotenv(ENV_FILE, override=True)

print("Password loaded:", bool(os.getenv("DB_PASSWORD")))


print("DB_HOST:", repr(os.getenv("DB_HOST")))
print("DB_USER:", repr(os.getenv("DB_USER")))
print("DB_PASSWORD set:", bool(os.getenv("DB_PASSWORD")))
print("DB_PORT:", repr(os.getenv("DB_PORT")))
print("DB_NAME:", repr(os.getenv("DB_NAME")))

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(database_url)

# Test the connection before importing the CSV
with engine.connect() as connection:
    print("Connected as:", connection.execute(text("SELECT current_user")).scalar())
    print("Database:", connection.execute(text("SELECT current_database()")).scalar())

claims = pd.read_csv("hf://datasets/mabilton/fremtpl2/freMTPL2freq.csv")

claims.columns = (
    claims.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
    .str.replace(r"[^a-z0-9_]", "", regex=True)
)

claims.to_sql(
    name="raw_claims",
    con=engine,
    schema="actuarial",
    index=False,
    if_exists="replace",
    chunksize=1_000,
)

print(f"Imported {len(claims):,} rows.")