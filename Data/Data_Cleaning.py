import os
from pathlib import Path

from Data.Import_Raw import Pc
from Import_Raw import pc

import pandas as pd
from dotenv import load_dotenv
from sqlalchemy import URL, create_engine, text
#aaaaa
pc = Pc()
df = pd.read_sql("""

""", con = pc.engine)

for i in range(3):
    print(i)

