"""dataload.py"""

import oracledb
import csv
from datetime import datetime

# SETUP for local
LIB_DIR = None #r"D:\OracleDatabase\app\oracle\product\11.2.0\server\bin\oracle.exe"  # Your Instant Client path
DB_USER = "cop3710"
DB_PASS = "sp2026"
DB_DSN  = "127.0.0.1:1521/XE"

# Init Thick Mode (local Oracle XE / FreeSQL)
oracledb.init_oracle_client(lib_dir=LIB_DIR)

# Date/datetime Format
DATE_FMT      = "%Y-%m-%d"
TIMESTAMP_FMT = "%Y-%m-%d %H:%M:%S"

# Columns to be converted from string to date/datetime
DATE_COLS      = {"installation_date", "effective_start_date", "effective_end_date",
                  "start_date", "end_date", "install_date", "last_verified_date"}
TIMESTAMP_COLS = {"reading_timestamp"}

def coerce(value, col):
    """Convert a CSV string to the correct Python type for Oracle."""
    if value == "":
        return None
    if col in DATE_COLS:
        return datetime.strptime(value, DATE_FMT).date()
    if col in TIMESTAMP_COLS:
        return datetime.strptime(value, TIMESTAMP_FMT)
    try:
        return int(value)
    except ValueError:
        pass
    try:
        return float(value)
    except ValueError:
        pass
    return value

def bulk_load(cursor, conn, csv_path, table, columns, sql):
    with open(csv_path, mode="r", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        data = [[coerce(row[c], c) for c in columns] for row in reader]

    print(f"Loading {len(data)} rows into {table}...")
    cursor.executemany(sql, data)
    conn.commit()
    print(f"Successfully loaded {len(data)} rows into {table}.")

try:
    conn   = oracledb.connect(user=DB_USER, password=DB_PASS, dsn=DB_DSN)
    cursor = conn.cursor()
    print("Connected to Oracle Database")

    # households
    bulk_load(cursor, conn,
        "data/households.csv", "households",
        ["id", "address", "city", "state", "zip_code", "installation_date"],
        "INSERT INTO households (id, address, city, state, zip_code, installation_date) "
        "VALUES (:1, :2, :3, :4, :5, :6)"
    )

    # rate_plans
    bulk_load(cursor, conn,
        "data/rate_plans.csv", "rate_plans",
        ["id", "plan_name", "base_rate_per_kwh", "peak_rate_per_kwh",
         "effective_start_date", "effective_end_date"],
        "INSERT INTO rate_plans (id, plan_name, base_rate_per_kwh, peak_rate_per_kwh, "
        "effective_start_date, effective_end_date) VALUES (:1, :2, :3, :4, :5, :6)"
    )

    # household_to_rate_plans
    bulk_load(cursor, conn,
        "data/household_to_rate_plans.csv", "household_to_rate_plans",
        ["household_id", "rate_plan_id", "start_date", "end_date"],
        "INSERT INTO household_to_rate_plans (household_id, rate_plan_id, start_date, end_date) "
        "VALUES (:1, :2, :3, :4)"
    )

    # smart_meters
    bulk_load(cursor, conn,
        "data/smart_meters.csv", "smart_meters",
        ["id", "serial_number", "manufacturer", "firmware_version",
         "install_date", "household_id"],
        "INSERT INTO smart_meters (id, serial_number, manufacturer, firmware_version, "
        "install_date, household_id) VALUES (:1, :2, :3, :4, :5, :6)"
    )

    # meter_locations
    bulk_load(cursor, conn,
        "data/meter_locations.csv", "meter_locations",
        ["meter_id", "latitude", "longitude", "last_verified_date"],
        "INSERT INTO meter_locations (meter_id, latitude, longitude, last_verified_date) "
        "VALUES (:1, :2, :3, :4)"
    )

    # energy_readings
    bulk_load(cursor, conn,
        "data/energy_readings.csv", "energy_readings",
        ["meter_id", "reading_timestamp", "global_active_power", "global_reactive_power",
         "voltage", "global_intensity", "sub_metering_1", "sub_metering_2", "sub_metering_3"],
        "INSERT INTO energy_readings (meter_id, reading_timestamp, global_active_power, "
        "global_reactive_power, voltage, global_intensity, sub_metering_1, sub_metering_2, "
        "sub_metering_3) VALUES (:1, :2, :3, :4, :5, :6, :7, :8, :9)"
    )

except Exception as e:
    print(f"Error: {e}")
    if 'conn' in locals():
        conn.rollback()

finally:
    if 'cursor' in locals(): cursor.close()
    if 'conn'   in locals(): conn.close()
    print("Oracle connection closed.")