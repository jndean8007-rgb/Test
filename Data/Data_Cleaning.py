import os
from pathlib import Path

from Data.Import_Raw import Pc

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text

ENV_FILE = Path('C:/Users/rosie/PycharmProjects/Git Testing/.env')

load_dotenv(ENV_FILE, override=True)

pc = Pc(os.getenv("DB_NAME"))
df = pd.read_sql(
    """
    SELECT * from actuarial.house_prices
    """,
    con=pc.engine
)

x = df.drop(columns=["ID","SalePrice"])
y = df[["SalePrice"]]