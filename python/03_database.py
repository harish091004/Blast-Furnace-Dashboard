import sqlite3
import pandas as pd
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

DATABASE = BASE_DIR / "database"

DATABASE.mkdir(exist_ok=True)

DB_FILE = DATABASE / "furnace.db"

DATA = BASE_DIR / "data" / "processed"

conn = sqlite3.connect(DB_FILE)

cursor = conn.cursor()

print("Connected to SQLite Database")

production = pd.read_csv(DATA / "production_clean.csv")

temperature = pd.read_csv(DATA / "temperature_clean.csv")

fuel = pd.read_csv(DATA / "fuel_clean.csv")

power = pd.read_csv(DATA / "power_clean.csv")

downtime = pd.read_csv(DATA / "downtime_clean.csv")

alarms = pd.read_csv(DATA / "alarms_clean.csv")

summary = pd.read_csv(DATA / "daily_summary.csv")

production.to_sql(

    "Production",

    conn,

    if_exists="replace",

    index=False

)

temperature.to_sql(

    "Temperature",

    conn,

    if_exists="replace",

    index=False

)

fuel.to_sql(

    "Fuel",

    conn,

    if_exists="replace",

    index=False

)

power.to_sql(

    "Power",

    conn,

    if_exists="replace",

    index=False

)

downtime.to_sql(

    "Downtime",

    conn,

    if_exists="replace",

    index=False

)

alarms.to_sql(

    "Alarms",

    conn,

    if_exists="replace",

    index=False

)

summary.to_sql(

    "DailySummary",

    conn,

    if_exists="replace",

    index=False

)

tables = pd.read_sql(

    "SELECT name FROM sqlite_master WHERE type='table';",

    conn

)

print(tables)

for table in [

    "Production",

    "Temperature",

    "Fuel",

    "Power",

    "Downtime",

    "Alarms",

    "DailySummary"

]:

    rows = pd.read_sql(

        f"SELECT COUNT(*) as Total FROM {table}",

        conn

    )

    print(table)

    print(rows)

    print()

    query = """

SELECT

Date,

SUM(Actual) as Production

FROM Production

GROUP BY Date

"""

daily = pd.read_sql(query, conn)

print(daily.head())

query = """

SELECT

AVG(Temperature)

FROM Temperature

"""

print(pd.read_sql(query, conn))

query = """

SELECT

Reason,

SUM(Minutes) as Total

FROM Downtime

GROUP BY Reason

ORDER BY Total DESC

"""

print(pd.read_sql(query, conn))

conn.commit()

conn.close()

print("Database Created Successfully")