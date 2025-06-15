#!/usr/bin/env python3
"""
load_data.py

Read data/countries_of_the_world.csv, validate each row, and bulk-insert into MySQL.
Any row with a validation or database error is skipped and reported at the end.
"""

import csv
import mysql.connector
import getpass
import argparse
import sys
import logging

logging.basicConfig(
    filename="errors.log",
    filemode="w",
    level=logging.ERROR,
    format="%(message)s"
)


# The exact headers expected in the CSV
EXPECTED_COLUMNS = [
    "Country", "Region", "Population", "Area (sq. mi.)",
    "Pop. Density (per sq. mi.)", "Coastline (coast/area ratio)",
    "Net migration", "Infant mortality (per 1000 births)",
    "GDP ($ per capita)", "Literacy (%)", "Phones (per 1000)",
    "Arable (%)", "Crops (%)", "Other (%)", "Climate",
    "Birthrate", "Deathrate", "Agriculture", "Industry", "Service"
]

# Parameterized INSERT matching the countries table
SQL_INSERT = """
INSERT INTO countries (
  country, region, population, area_sq_mi, pop_density, coastline_ratio,
  net_migration, infant_mortality, gdp_per_capita, literacy, phones_per_1000,
  arable, crops, other, climate, birthrate, deathrate, agriculture, industry, service
) VALUES (
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
)
"""

def validate_and_prepare(row, line_num):
    """Check column count, types, and return (values_tuple, None) or (None, error_msg)."""
    # 1) Header check
    if set(row.keys()) != set(EXPECTED_COLUMNS):
        return None, f"Line {line_num}: unexpected columns: {row.keys()}"
    values = []
    for col in EXPECTED_COLUMNS:
        raw = row[col].strip()
        if col in ("Country", "Region"):
            if raw == "":
                return None, f"Line {line_num}: {col} is required"
            values.append(raw)
        else:
            # All other columns must be numeric
            if raw == "":
                values.append(None)
            else:
                # Replace commas with dots for decimal parsing
                num = raw.replace(",", ".")
                try:
                    values.append(float(num))
                except ValueError:
                    return None, f"Line {line_num}: invalid number in {col}: '{raw}'"
    return tuple(values), None

def load_data(args):
    # 1) Connect to SQL database
    password = getpass.getpass(f"Enter MySQL password for {args.user}@{args.host}:{args.port}/{args.database}: ")
    try:
        conn = mysql.connector.connect(
            host=args.host,
            port=args.port,
            user=args.user,
            password=password,
            database=args.database
        )
    except mysql.connector.Error as err:
        print("ERROR: Could not connect to MySQL:", err)
        sys.exit(1)

    cursor = conn.cursor()
    errors = []
    inserted = 0

    # 2) Open CSV and validate/insert row by row
    with open(args.csv, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        if reader.fieldnames != EXPECTED_COLUMNS:
            print("WARNING: CSV headers do not match expected schema:")
            print("  Found:", reader.fieldnames)
            print("  Expected:", EXPECTED_COLUMNS)
        for lineno, row in enumerate(reader, start=2):
            values, error = validate_and_prepare(row, lineno)
            if error:
                logging.error(error)     
                continue
            try:
                cursor.execute(SQL_INSERT, values)
                inserted += 1
            except Exception as e:
                logging.error(f"Line {lineno}: DB error: {e}") 

    # 3) Commit and summarize
    conn.commit()
    cursor.close()
    conn.close()

    print(f"\nFinished: inserted {inserted} rows.")
    if errors:
        print(f"Encountered {len(errors)} error(s):")
        for e in errors:
            print(" ", e)

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Load countries CSV into MySQL")
    p.add_argument("--host",     default="localhost", help="MySQL host")
    p.add_argument("--port",     type=int, default=3306, help="MySQL port")
    p.add_argument("--user",     default="root", help="MySQL user")
    p.add_argument("--database", default="financial_db", help="MySQL database name")
    p.add_argument("--csv",      default="data/countries_of_the_world.csv",
                   help="Path to countries CSV file")
    args = p.parse_args()
    load_data(args)
