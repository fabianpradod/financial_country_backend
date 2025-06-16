#!/usr/bin/env python3
"""
data_analysis.py

Connect to MySQL, load the 'countries' table into a Pandas DataFrame,
perform cleaning, and save cleaned version to CSV.
"""

import pandas as pd
from sqlalchemy import create_engine
import getpass
import argparse
import sys

def analyze_data(args):
    # 1) Prompt for password 
    password = getpass.getpass(f"Enter MySQL password for {args.user}@{args.host}:{args.port}/{args.database}: ")

    # 2) Connect using SQLAlchemy engine
    try:
        engine = create_engine(
            f"mysql+mysqlconnector://{args.user}:{password}@{args.host}:{args.port}/{args.database}",
            echo=False
        )
    except Exception as e:
        print("ERROR: Could not create SQLAlchemy engine:", e)
        sys.exit(1)

    # 3) Read data from MySQL into Pandas DataFrame
    try:
        df = pd.read_sql("SELECT * FROM countries;", con=engine)
    except Exception as e:
        print("ERROR: Failed to read data from MySQL:", e)
        sys.exit(1)

    # 4) Inspect the raw data
    print("\n=== DataFrame information (values and their types): ===")
    print(df.info(), "\n")
    print("\n=== Values missing per column ===")
    print(df.isna().sum(), "\n")
    print("\n=== First 6 rows ===")
    print(df.head(n=6), "\n")

    # 5) Data cleaning
    df = df.dropna(subset=["country"])  # remove rows with missing country names
    numeric_cols = df.select_dtypes("number").columns
    df[numeric_cols] = df[numeric_cols].fillna(0)  # fill numeric NaNs with 0

    # Convert climate column to int if exists
    if "climate" in df.columns:
        df["climate"] = df["climate"].astype(int)


    # 6) Data Analysis

    # Total population per region
    pop_by_region = df.groupby("region")["population"].sum().sort_values(ascending=False)
    print("\n=== Total Population by Region ===")
    print(pop_by_region, "\n")

    # Mean and median GDP per region
    gdp_by_region = df.groupby("region")["gdp_per_capita"].agg(["mean", "median"]).sort_values("mean", ascending=False)
    print("\n=== GDP per Capita by Region (medocker exec -it mysql-dev mysql -u root -p -e an & median) ===")
    print(gdp_by_region, "\n")

    # Literacy rate mean and median per region
    literacy_by_region = df.groupby("region")["literacy"].agg(["mean", "median"]).sort_values("mean", ascending=False)
    print("\n=== Literacy Rate by Region (mean & median) ===")
    print(literacy_by_region, "\n")

    # Top / bottom 3 countries by GDP per capita per region
    for region, group in df.groupby("region"):
        print(f"\n=== Top 3 GDP per Capita in {region} ===")
        top3 = group.nlargest(3, "gdp_per_capita")[["country", "gdp_per_capita"]]
        print(top3.to_string(index=False))

        print(f"\n=== Bottom 3 GDP per Capita in {region} ===")
        bot3 = group.nsmallest(3, "gdp_per_capita")[["country", "gdp_per_capita"]]
        print(bot3.to_string(index=False))


    # 7) Validation Checks via Analysis

    # 7a) Check for duplicate country names
    duplicates = df[df.duplicated(subset=["country"], keep=False)]
    if not duplicates.empty:
        print("WARNING: Duplicate country entries found:")
        print(duplicates[["country"]].drop_duplicates(), "\n")
    else:
        print("\nNo duplicate country entries.\n")

    # 7b) Check for negative or zero population
    neg_pop = df[df["population"] <= 0]
    if not neg_pop.empty:
        print("WARNING: Countries with non-positive population:")
        print(neg_pop[["country", "population"]], "\n")
    else:
        print("\nAll countries have positive population.\n")

    # 7c) Check for GDP per capita outside expected range (e.g., >200k USD)
    outliers = df[df["gdp_per_capita"] > 200_000]
    if not outliers.empty:
        print("WARNING: Countries with extremely high GDP per capita:")
        print(outliers[["country", "gdp_per_capita"]], "\n")
    else:
        print("\nNo extreme GDP outliers found.\n")

    # 8) Save cleaned data
    output_path = "data/countries_cleaned.csv"
    df.to_csv(output_path, index=False)
    print(f"\nCleaned data saved to {output_path}")

if __name__ == "__main__":
    p = argparse.ArgumentParser(description="Analyze and clean country data from MySQL")
    p.add_argument("--host",     default="localhost", help="MySQL host")
    p.add_argument("--port",     type=int, default=3306, help="MySQL port")
    p.add_argument("--user",     default="root", help="MySQL user")
    p.add_argument("--database", default="financial_db", help="MySQL database name")
    args = p.parse_args()
    analyze_data(args)
