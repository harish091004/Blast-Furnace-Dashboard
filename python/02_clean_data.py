import pandas as pd
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

RAW = BASE_DIR / "data" / "raw"
PROCESSED = BASE_DIR / "data" / "processed"

PROCESSED.mkdir(parents=True, exist_ok=True)

production = pd.read_csv(RAW / "production.csv")
temperature = pd.read_csv(RAW / "temperature.csv")
fuel = pd.read_csv(RAW / "fuel.csv")
power = pd.read_csv(RAW / "power.csv")
downtime = pd.read_csv(RAW / "downtime.csv")
alarms = pd.read_csv(RAW / "alarms.csv")

print(production.info())
print(production.head())

print(temperature.info())
print(temperature.head())

production = production.drop_duplicates()
temperature = temperature.drop_duplicates()
fuel = fuel.drop_duplicates()
power = power.drop_duplicates()
downtime = downtime.drop_duplicates()
alarms = alarms.drop_duplicates()

production.fillna(0, inplace=True)
temperature.fillna(method="ffill", inplace=True)
fuel.fillna(0, inplace=True)
power.fillna(0, inplace=True)
downtime.fillna("Unknown", inplace=True)
alarms.fillna("None", inplace=True)

production["Date"] = pd.to_datetime(production["Date"])
temperature["Timestamp"] = pd.to_datetime(temperature["Timestamp"])
fuel["Timestamp"] = pd.to_datetime(fuel["Timestamp"])
power["Timestamp"] = pd.to_datetime(power["Timestamp"])
downtime["Date"] = pd.to_datetime(downtime["Date"])
alarms["Time"] = pd.to_datetime(alarms["Time"])

production["Efficiency"] = (
    production["Actual"] /
    production["Target"]
) * 100

fuel["Fuel_Rate"] = (
    fuel["Coke"] +
    fuel["Coal"] +
    fuel["PCI"]
)

daily_power = power.groupby(power["Timestamp"].dt.date)["Power_kWh"].sum()

daily_production = production.groupby("Date")["Actual"].sum()

temp_summary = temperature.groupby(
    temperature["Timestamp"].dt.date
)["Temperature"].agg([
    "mean",
    "max",
    "min"
])

temp_summary.columns = [
    "Avg_Temp",
    "Max_Temp",
    "Min_Temp"
]

downtime_summary = downtime.groupby("Date")["Minutes"].sum()

downtime_summary = downtime_summary.rename("Downtime")

production_summary = production.groupby("Date").agg(
    Target=("Target","sum"),
    Actual=("Actual","sum"),
    Efficiency=("Efficiency","mean")
)

summary = production_summary.join(temp_summary)

summary = summary.join(daily_power.rename("Power"))

summary = summary.join(downtime_summary)

summary = summary.fillna(0)

production.to_csv(
    PROCESSED / "production_clean.csv",
    index=False
)

temperature.to_csv(
    PROCESSED / "temperature_clean.csv",
    index=False
)

fuel.to_csv(
    PROCESSED / "fuel_clean.csv",
    index=False
)

power.to_csv(
    PROCESSED / "power_clean.csv",
    index=False
)

downtime.to_csv(
    PROCESSED / "downtime_clean.csv",
    index=False
)

alarms.to_csv(
    PROCESSED / "alarms_clean.csv",
    index=False
)

summary.to_csv(
    PROCESSED / "daily_summary.csv"
)

print("=" * 50)
print("DATA CLEANING COMPLETE")
print("=" * 50)

print("Production:", len(production))
print("Temperature:", len(temperature))
print("Fuel:", len(fuel))
print("Power:", len(power))
print("Downtime:", len(downtime))
print("Alarms:", len(alarms))

print("\nProcessed files saved to:")
print(PROCESSED)