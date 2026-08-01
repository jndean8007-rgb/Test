import os
from pathlib import Path

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
from sklearn.datasets import fetch_openml

class Pc:

    def __init__(self, name = os.getenv("DB_NAME")):

        ENV_FILE = Path('C:/Users/rosie/PycharmProjects/Git Testing/.env')
        load_dotenv(ENV_FILE, override=True)

        self.engine = create_engine(URL.create(
            drivername="postgresql+psycopg",
            username=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD"),
            host=os.getenv("DB_HOST", "localhost"),
            port=int(os.getenv("DB_PORT", "5432")),
            database=name,
            )
        )


ENV_FILE = Path('C:/Users/rosie/PycharmProjects/Git Testing/.env')

load_dotenv(ENV_FILE, override=True)

database_url = URL.create(
    drivername="postgresql+psycopg",
    username=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    host=os.getenv("DB_HOST", "localhost"),
    port=int(os.getenv("DB_PORT", "5432")),
    database=os.getenv("DB_NAME"),
)

engine = create_engine(database_url)


# claims = pd.read_csv("hf://datasets/mabilton/fremtpl2/freMTPL2freq.csv")

# claims.columns = (
    #claims.columns
    #.str.strip()
    #.str.lower()
    #.str.replace(" ", "_")
    #.str.replace(r"[^a-z0-9_]", "", regex=True)
#)

# claims.to_sql(
    #name="raw_claims",
    #con=engine,
    #schema="actuarial",
    #index=False,
    #if_exists="replace",
    #chunksize=1_000,
#)
ames = fetch_openml(
    name="house_prices",
    as_frame=True,
    parser="auto"
)

df = ames.frame

df.to_sql(name="house_prices", con=engine, if_exists="replace", index=False, schema = 'actuarial')