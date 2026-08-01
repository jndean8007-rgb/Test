import os
from pathlib import Path

from Data.Import_Raw import Pc
from Import_Raw import pc

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
#awdoawudh
pc = Pc()
df = pd.read_sql("""

""", con = pc.engine)

print('Hello world righty now')