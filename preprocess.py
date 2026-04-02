"""preprocess.py"""

import csv
import os
import random
from datetime import date, datetime, timedelta

random.seed(42)

DATA_DIR = "data"
os.makedirs(DATA_DIR, exist_ok=True)


def rand_date(start, end):
    return start + timedelta(days=random.randint(0, (end - start).days))


def write_csv(filename, fieldnames, rows):
    path = os.path.join(DATA_DIR, filename)
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)
    print(f"Wrote {len(rows)} rows -> {path}")

# References and data (for simulated and raw)

# Cities in FL
CITIES_STATES = [
    ("Miami", "FL"), ("Orlando", "FL"), ("Tampa", "FL"),
    ("Jacksonville", "FL"), ("Fort Lauderdale", "FL"),
    ("Gainesville", "FL"), ("Tallahassee", "FL"),
    ("Naples", "FL"), ("Boca Raton", "FL"), ("Sarasota", "FL"),
]

# Street Names (but all trees)
STREET_NAMES = [
    "Oak Ave", "Maple St", "Pine Rd", "Cedar Blvd", "Elm Dr",
    "Birch Ln", "Walnut Way", "Spruce Ct", "Cherry St", "Ash Pl",
]

# Actual brands (for simulated smart meter models)
MANUFACTURERS = ["Itron", "Landis+Gyr", "Sensus", "Honeywell", "Aclara"]

PLAN_NAMES = [
    "Standard", "Economy", "Premium",
    "Flat Rate Basic", "Green Energy Plus", "Budget",
]

# Raw data from the web (Kaggle)
# format: Date;Time;Global_active_power;Global_reactive_power;
#         Voltage;Global_intensity;Sub_metering_1;Sub_metering_2;Sub_metering_3
RAW_DATA = """16/12/2006;17:24:00;4.216;0.418;234.840;18.400;0.000;1.000;17.000
16/12/2006;17:25:00;5.360;0.436;233.630;23.000;0.000;1.000;16.000
16/12/2006;17:26:00;5.374;0.498;233.290;23.000;0.000;2.000;17.000
16/12/2006;17:27:00;5.388;0.502;233.740;23.000;0.000;1.000;17.000
16/12/2006;17:28:00;3.666;0.528;235.680;15.800;0.000;1.000;17.000
16/12/2006;17:29:00;3.520;0.522;235.020;15.000;0.000;2.000;17.000
16/12/2006;17:30:00;3.702;0.520;235.090;15.800;0.000;1.000;17.000
16/12/2006;17:31:00;3.700;0.520;235.220;15.800;0.000;1.000;17.000
16/12/2006;17:32:00;3.668;0.510;233.990;15.800;0.000;1.000;17.000
16/12/2006;17:33:00;3.662;0.510;233.860;15.800;0.000;2.000;16.000
16/12/2006;17:34:00;4.448;0.498;232.860;19.600;0.000;1.000;17.000
16/12/2006;17:35:00;5.412;0.470;232.780;23.200;0.000;1.000;17.000
16/12/2006;17:36:00;5.224;0.478;232.990;22.400;0.000;1.000;16.000
16/12/2006;17:37:00;5.268;0.398;232.910;22.600;0.000;2.000;17.000
16/12/2006;17:38:00;4.054;0.422;235.240;17.600;0.000;1.000;17.000
16/12/2006;17:39:00;3.384;0.282;237.140;14.200;0.000;0.000;17.000
16/12/2006;17:40:00;3.270;0.152;236.730;13.800;0.000;0.000;17.000
16/12/2006;17:41:00;3.430;0.156;237.060;14.400;0.000;0.000;17.000
16/12/2006;17:42:00;3.266;0.000;237.130;13.800;0.000;0.000;18.000
16/12/2006;17:43:00;3.728;0.000;235.840;16.400;0.000;0.000;17.000
16/12/2006;17:44:00;5.894;0.000;232.690;25.400;0.000;0.000;16.000
16/12/2006;17:45:00;7.706;0.000;230.980;33.200;0.000;0.000;17.000
16/12/2006;17:46:00;7.026;0.000;232.210;30.600;0.000;0.000;16.000
16/12/2006;17:47:00;5.174;0.000;234.190;22.000;0.000;0.000;17.000
16/12/2006;17:48:00;4.474;0.000;234.960;19.400;0.000;0.000;17.000
16/12/2006;17:49:00;3.248;0.000;236.660;13.600;0.000;0.000;17.000
16/12/2006;17:50:00;3.236;0.000;235.840;13.600;0.000;0.000;17.000
16/12/2006;17:51:00;3.228;0.000;235.600;13.600;0.000;0.000;17.000
16/12/2006;17:52:00;3.258;0.000;235.490;13.800;0.000;0.000;17.000
16/12/2006;17:53:00;3.178;0.000;235.280;13.400;0.000;0.000;17.000
16/12/2006;17:54:00;2.720;0.000;235.060;11.600;0.000;0.000;17.000
16/12/2006;17:55:00;3.758;0.076;234.170;16.400;0.000;0.000;17.000
16/12/2006;17:56:00;4.342;0.090;233.770;18.400;0.000;0.000;16.000
16/12/2006;17:57:00;4.512;0.000;233.620;19.200;0.000;0.000;17.000
16/12/2006;17:58:00;4.058;0.200;234.680;17.600;0.000;0.000;17.000
16/12/2006;17:59:00;2.472;0.058;236.940;10.400;0.000;0.000;17.000
16/12/2006;18:00:00;2.790;0.180;237.520;11.800;0.000;0.000;18.000
16/12/2006;18:01:00;2.624;0.144;238.200;11.000;0.000;0.000;17.000
16/12/2006;18:02:00;2.772;0.118;238.280;11.600;0.000;0.000;17.000
16/12/2006;18:03:00;3.740;0.108;236.930;16.400;0.000;16.000;18.000
16/12/2006;18:04:00;4.928;0.202;235.010;21.000;0.000;37.000;16.000
16/12/2006;18:05:00;6.052;0.192;232.930;26.200;0.000;37.000;17.000
16/12/2006;18:06:00;6.752;0.186;232.120;29.000;0.000;36.000;17.000
16/12/2006;18:07:00;6.474;0.144;231.850;27.800;0.000;37.000;16.000
16/12/2006;18:08:00;6.308;0.116;232.250;27.000;0.000;36.000;17.000
16/12/2006;18:09:00;4.464;0.136;234.660;19.000;0.000;37.000;16.000
16/12/2006;18:10:00;3.396;0.148;236.200;15.000;0.000;22.000;18.000
16/12/2006;18:11:00;3.090;0.152;237.070;13.800;0.000;12.000;17.000
16/12/2006;18:12:00;3.730;0.144;235.780;16.400;0.000;27.000;17.000
16/12/2006;18:13:00;2.308;0.160;237.430;9.600;0.000;1.000;17.000
16/12/2006;18:14:00;2.388;0.158;237.260;10.000;0.000;1.000;17.000
16/12/2006;18:15:00;4.598;0.100;234.250;21.400;0.000;20.000;17.000
16/12/2006;18:16:00;4.524;0.076;234.200;19.600;0.000;9.000;17.000
16/12/2006;18:17:00;4.202;0.082;234.310;17.800;0.000;1.000;17.000
16/12/2006;18:18:00;4.472;0.000;233.290;19.200;0.000;1.000;16.000
16/12/2006;18:19:00;2.852;0.000;235.610;12.000;0.000;1.000;17.000
16/12/2006;18:20:00;2.928;0.000;235.250;12.400;0.000;1.000;17.000
16/12/2006;18:21:00;2.940;0.000;236.040;12.400;0.000;2.000;17.000
16/12/2006;18:22:00;2.934;0.000;235.510;12.400;0.000;1.000;17.000
16/12/2006;18:23:00;2.926;0.000;235.680;12.400;0.000;1.000;17.000
16/12/2006;18:24:00;3.452;0.000;235.200;15.200;0.000;1.000;17.000
16/12/2006;18:25:00;4.870;0.000;233.740;20.800;0.000;1.000;17.000
16/12/2006;18:26:00;4.868;0.000;233.840;20.800;0.000;1.000;17.000
16/12/2006;18:27:00;4.866;0.000;233.790;20.800;0.000;1.000;17.000
16/12/2006;18:28:00;3.176;0.000;235.500;13.800;0.000;1.000;17.000
16/12/2006;18:29:00;2.920;0.000;235.840;12.400;0.000;1.000;17.000
16/12/2006;18:30:00;2.930;0.000;236.150;12.400;0.000;1.000;17.000
16/12/2006;18:31:00;2.912;0.050;235.810;12.400;0.000;1.000;17.000
16/12/2006;18:32:00;2.608;0.052;235.410;11.000;0.000;1.000;17.000
16/12/2006;18:33:00;2.714;0.162;234.820;11.600;0.000;0.000;17.000
16/12/2006;18:34:00;3.538;0.086;233.760;15.600;0.000;1.000;16.000
16/12/2006;18:35:00;6.072;0.000;232.480;26.400;0.000;27.000;17.000
16/12/2006;18:36:00;4.536;0.000;233.540;19.400;0.000;1.000;17.000
16/12/2006;18:37:00;4.408;0.000;232.320;18.800;0.000;1.000;16.000
16/12/2006;18:38:00;2.912;0.048;234.020;13.000;0.000;1.000;17.000
16/12/2006;18:39:00;2.326;0.054;234.760;9.800;0.000;1.000;17.000
16/12/2006;18:40:00;2.264;0.054;234.670;9.600;0.000;1.000;17.000
16/12/2006;18:41:00;2.270;0.054;235.270;9.600;0.000;1.000;17.000
16/12/2006;18:42:00;2.258;0.054;235.120;9.600;0.000;1.000;17.000
16/12/2006;18:43:00;2.188;0.068;235.800;9.200;0.000;1.000;17.000
16/12/2006;18:44:00;2.978;0.166;234.810;13.200;0.000;1.000;17.000
16/12/2006;18:45:00;4.200;0.174;234.380;17.800;0.000;1.000;17.000
16/12/2006;18:46:00;4.204;0.186;234.200;17.800;0.000;1.000;16.000
16/12/2006;18:47:00;4.218;0.178;233.980;18.000;0.000;1.000;17.000
16/12/2006;18:48:00;2.786;0.188;234.990;12.000;0.000;2.000;17.000
16/12/2006;18:49:00;2.540;0.088;234.670;10.800;0.000;4.000;17.000
16/12/2006;18:50:00;2.496;0.080;233.920;10.600;0.000;3.000;17.000
16/12/2006;18:51:00;2.336;0.070;233.510;10.000;0.000;1.000;16.000
16/12/2006;18:52:00;2.322;0.000;233.440;9.800;0.000;0.000;17.000
16/12/2006;18:53:00;2.448;0.000;233.640;10.600;0.000;1.000;17.000
16/12/2006;18:54:00;4.298;0.000;232.390;18.400;0.000;1.000;16.000
16/12/2006;18:55:00;4.230;0.090;232.250;18.200;0.000;1.000;17.000
16/12/2006;18:56:00;4.230;0.090;232.320;18.200;0.000;2.000;16.000
16/12/2006;18:57:00;3.924;0.084;232.790;17.000;0.000;1.000;17.000
16/12/2006;18:58:00;4.218;0.090;232.090;18.000;0.000;1.000;17.000
16/12/2006;18:59:00;4.224;0.090;231.960;18.200;0.000;1.000;16.000
16/12/2006;19:00:00;4.070;0.088;231.990;17.400;0.000;1.000;17.000
16/12/2006;19:01:00;3.612;0.090;232.360;15.600;0.000;2.000;16.000
16/12/2006;19:02:00;3.458;0.090;232.710;14.800;0.000;1.000;17.000
16/12/2006;19:03:00;3.434;0.090;232.010;14.800;0.000;1.000;16.000"""


#1 households
print("Generating households...")
households = []
for i in range(1, 101):
    city, state = random.choice(CITIES_STATES)
    households.append({
        "id":                i,
        "address":           f"{random.randint(100, 9999)} {random.choice(STREET_NAMES)}",
        "city":              city,
        "state":             state,
        "zip_code":          f"{random.randint(32000, 34999):05d}",
        "installation_date": rand_date(date(2006, 1, 1), date(2006, 12, 15)),
    })

write_csv("households.csv",
          ["id", "address", "city", "state", "zip_code", "installation_date"],
          households)

household_ids = [h["id"] for h in households]


#2 rate_plans
print("Generating rate_plans...")
rate_plans = []
for i, name in enumerate(PLAN_NAMES, start=1):
    base = round(random.uniform(0.08, 0.18), 4)
    rate_plans.append({
        "id":                    i,
        "plan_name":             name,
        "base_rate_per_kwh":     base,
        "peak_rate_per_kwh":     round(base * random.uniform(1.2, 1.8), 4),
        "effective_start_date":  date(2006, 1, 1),
        "effective_end_date":    date(2010, 12, 31),
    })

write_csv("rate_plans.csv",
          ["id", "plan_name", "base_rate_per_kwh", "peak_rate_per_kwh",
           "effective_start_date", "effective_end_date"],
          rate_plans)

rate_plan_ids = [r["id"] for r in rate_plans]


#3 household_to_rate_plans
print("Generating household_to_rate_plans...")
h2rp_rows = []
seen = set()
for hid in household_ids:
    plan_id = random.choice(rate_plan_ids)
    start   = rand_date(date(2006, 1, 1), date(2006, 11, 30))
    key     = (hid, plan_id, start)
    if key not in seen:
        seen.add(key)
        h2rp_rows.append({
            "household_id": hid,
            "rate_plan_id": plan_id,
            "start_date":   start,
            "end_date":     rand_date(start + timedelta(days=365), date(2010, 12, 31)),
        })

write_csv("household_to_rate_plans.csv",
          ["household_id", "rate_plan_id", "start_date", "end_date"],
          h2rp_rows)


#4 smart_meters
print("Generating smart_meters...")
smart_meters = []
serial_nums  = set()
for i, hid in enumerate(household_ids, start=1):
    while True:
        serial = f"SM-{random.randint(100000, 999999)}"
        if serial not in serial_nums:
            serial_nums.add(serial)
            break
    smart_meters.append({
        "id":               i,
        "serial_number":    serial,
        "manufacturer":     random.choice(MANUFACTURERS),
        "firmware_version": f"{random.randint(1,4)}.{random.randint(0,9)}.{random.randint(0,20)}",
        "install_date":     rand_date(date(2006, 1, 1), date(2006, 12, 15)),
        "household_id":     hid,
    })

write_csv("smart_meters.csv",
          ["id", "serial_number", "manufacturer", "firmware_version",
           "install_date", "household_id"],
          smart_meters)

meter_ids = [m["id"] for m in smart_meters]


#5 meter_locations
print("Generating meter_locations...")
meter_locations = []
for mid in meter_ids:
    meter_locations.append({
        "meter_id":           mid,
        "latitude":           round(random.uniform(24.5, 31.0), 6),
        "longitude":          round(random.uniform(-87.6, -80.0), 6),
        "last_verified_date": rand_date(date(2006, 12, 1), date(2007, 6, 1)),
    })

write_csv("meter_locations.csv",
          ["meter_id", "latitude", "longitude", "last_verified_date"],
          meter_locations)


#6 energy_readings
# The real data + simulated across the full date range (16/12/2006 to 26/11/2010)
# just so the first 100 records doesn't occur in a couple of mins
print("Processing real energy readings data...")

range_start = datetime(2006, 12, 16, 17, 24, 0)
range_end   = datetime(2010, 11, 26, 21,  2, 0)
range_secs  = int((range_end - range_start).total_seconds())

# Generate unique random time across the range (sorted)
random_offsets = sorted(random.sample(range(range_secs), 100))
random_timestamps = [range_start + timedelta(seconds=s) for s in random_offsets]

energy_rows = []
for i, line in enumerate(RAW_DATA.strip().split("\n"), start=1):
    parts = line.split(";")
    # Use a random time spread across the full date range
    dt = random_timestamps[i-1]
    energy_rows.append({
        "meter_id":              i,
        "reading_timestamp":     dt.strftime("%Y-%m-%d %H:%M:%S"),
        "global_active_power":   parts[2],
        "global_reactive_power": parts[3],
        "voltage":               parts[4],
        "global_intensity":      parts[5],
        "sub_metering_1":        parts[6],
        "sub_metering_2":        parts[7],
        "sub_metering_3":        parts[8],
    })

write_csv("energy_readings.csv",
          ["meter_id", "reading_timestamp", "global_active_power",
           "global_reactive_power", "voltage", "global_intensity",
           "sub_metering_1", "sub_metering_2", "sub_metering_3"],
          energy_rows)

print(f"\nDone. All CSV files are in the ./{DATA_DIR}/ folder.")
print(f"Note: energy_readings contains {len(energy_rows)} real readings for meter_id = 1.")
print("      Place additional raw data files in this folder and extend the script to load them.")
