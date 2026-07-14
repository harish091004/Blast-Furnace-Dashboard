import os
import random
from datetime import datetime, timedelta

import pandas as pd
import numpy as np



OUTPUT_FOLDER = "../data/raw"

os.makedirs(OUTPUT_FOLDER, exist_ok=True)

random.seed(42)
np.random.seed(42)

print("Generating Blast Furnace Data...")
print()



START_DATE = datetime(2026, 1, 1)
DAYS = 180

SHIFTS = ["A", "B", "C"]


# 1. PRODUCTION DATA


production = []

for day in range(DAYS):

    current_date = START_DATE + timedelta(days=day)

    for shift in SHIFTS:

        target = 800

        actual = random.randint(770, 815)

        downtime = random.randint(0, 30)

        efficiency = round((actual / target) * 100, 2)

        production.append([
            current_date.date(),
            shift,
            "BF-01",
            target,
            actual,
            downtime,
            efficiency
        ])

production_df = pd.DataFrame(
    production,
    columns=[
        "Date",
        "Shift",
        "Furnace",
        "Target",
        "Actual",
        "Downtime",
        "Efficiency"
    ]
)

production_df.to_csv(
    os.path.join(OUTPUT_FOLDER, "production.csv"),
    index=False
)

print("production.csv created")


# 2. TEMPERATURE DATA


temperature = []

for i in range(DAYS * 24 * 4):

    timestamp = START_DATE + timedelta(minutes=i * 15)

    zone = random.choice([
        "Top",
        "Middle",
        "Bottom"
    ])

    temp = round(np.random.normal(1185, 8), 1)

    temperature.append([
        timestamp,
        zone,
        temp
    ])

temperature_df = pd.DataFrame(
    temperature,
    columns=[
        "Timestamp",
        "Zone",
        "Temperature"
    ]
)

temperature_df.to_csv(
    os.path.join(OUTPUT_FOLDER, "temperature.csv"),
    index=False
)

print("temperature.csv created")


# 3. FUEL DATA


fuel = []

for i in range(DAYS * 24):

    timestamp = START_DATE + timedelta(hours=i)

    coke = random.randint(500, 540)

    coal = random.randint(80, 95)

    pci = random.randint(85, 100)

    fuel.append([
        timestamp,
        coke,
        coal,
        pci
    ])

fuel_df = pd.DataFrame(
    fuel,
    columns=[
        "Timestamp",
        "Coke",
        "Coal",
        "PCI"
    ]
)

fuel_df.to_csv(
    os.path.join(OUTPUT_FOLDER, "fuel.csv"),
    index=False
)

print("fuel.csv created")


# 4. POWER DATA


power = []

for i in range(DAYS * 24):

    timestamp = START_DATE + timedelta(hours=i)

    power_used = random.randint(3200, 3600)

    voltage = random.randint(410, 430)

    current = random.randint(180, 220)

    power.append([
        timestamp,
        power_used,
        voltage,
        current
    ])

power_df = pd.DataFrame(
    power,
    columns=[
        "Timestamp",
        "Power_kWh",
        "Voltage",
        "Current"
    ]
)

power_df.to_csv(
    os.path.join(OUTPUT_FOLDER, "power.csv"),
    index=False
)

print("power.csv created")


# 5. DOWNTIME DATA


reasons = [
    "Mechanical",
    "Electrical",
    "Charging Delay",
    "Maintenance",
    "Raw Material Delay"
]

downtime = []

for day in range(DAYS):

    date = START_DATE + timedelta(days=day)

    events = random.randint(0, 3)

    for _ in range(events):

        shift = random.choice(SHIFTS)

        reason = random.choice(reasons)

        minutes = random.randint(5, 45)

        downtime.append([
            date.date(),
            shift,
            reason,
            minutes
        ])

downtime_df = pd.DataFrame(
    downtime,
    columns=[
        "Date",
        "Shift",
        "Reason",
        "Minutes"
    ]
)

downtime_df.to_csv(
    os.path.join(OUTPUT_FOLDER, "downtime.csv"),
    index=False
)

print("downtime.csv created")


# 6. ALARMS
 

alarm_names = [
    "High Temperature",
    "Low Coke Feed",
    "Power Spike",
    "Cooling Water Low",
    "High Gas Pressure",
    "Low Blast Pressure"
]

severity = [
    "Low",
    "Medium",
    "High"
]

alarms = []

for i in range(1000):

    timestamp = START_DATE + timedelta(hours=i)

    alarms.append([
        timestamp,
        random.choice(alarm_names),
        random.choice(severity)
    ])

alarms_df = pd.DataFrame(
    alarms,
    columns=[
        "Time",
        "Alarm",
        "Severity"
    ]
)

alarms_df.to_csv(
    os.path.join(OUTPUT_FOLDER, "alarms.csv"),
    index=False
)

print("alarms.csv created")


print()
print("=" * 50)
print("DATA GENERATION COMPLETE")
print("=" * 50)

print(f"Production Records : {len(production_df)}")
print(f"Temperature Records: {len(temperature_df)}")
print(f"Fuel Records       : {len(fuel_df)}")
print(f"Power Records      : {len(power_df)}")
print(f"Downtime Records   : {len(downtime_df)}")
print(f"Alarm Records      : {len(alarms_df)}")

print()
print("Files saved in:")
print(os.path.abspath(OUTPUT_FOLDER))