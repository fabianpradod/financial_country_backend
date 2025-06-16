#!/usr/bin/env python3
"""
api/app.py

Flask application exposing RESTful endpoints for country and region analytics.
"""
from flask import Flask, jsonify, request, abort
from flask_cors import CORS
from sqlalchemy import create_engine, text
import pandas as pd
import os
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()
DB_USER = os.getenv("DB_USER", "root")
DB_PASS = os.getenv("DB_PASS", "")
DB_HOST = os.getenv("DB_HOST", "localhost")
DB_PORT = os.getenv("DB_PORT", "3306")
DB_NAME = os.getenv("DB_NAME", "financial_db")

# Create SQLAlchemy engine
engine = create_engine(
    f"mysql+mysqlconnector://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}",
    echo=False
)

app = Flask(__name__)
CORS(app)

# GET /api/countries - list all countries with basic info
@app.route("/api/countries", methods=["GET"])
def get_countries():
    df = pd.read_sql("SELECT country, region FROM countries;", con=engine)
    return jsonify(df.to_dict(orient="records"))

# GET /api/countries/<country_name> - detailed data for a specific country
@app.route("/api/countries/<string:country_name>", methods=["GET"])
def get_country(country_name):
    sql = text("SELECT * FROM countries WHERE country = :ctry;")
    result = engine.execute(sql, {"ctry": country_name}).fetchone()
    if not result:
        abort(404, description=f"Country '{country_name}' not found.")
    return jsonify(dict(result))

# GET /api/regions - analytics per region
@app.route("/api/regions", methods=["GET"])
def get_regions():
    df = pd.read_sql("SELECT * FROM region_analysis;", con=engine)
    return jsonify(df.to_dict(orient="records"))

# GET /api/regions/<region_name> - analytics for one region
@app.route("/api/regions/<string:region_name>", methods=["GET"])
def get_region(region_name):
    sql = text("SELECT * FROM region_analysis WHERE region = :r;")
    result = engine.execute(sql, {"r": region_name}).fetchone()
    if not result:
        abort(404, description=f"Region '{region_name}' not found.")
    return jsonify(dict(result))

# GET /api/regions/<region_name>/gdp_rankings?rank_type=top|bottom
@app.route("/api/regions/<string:region_name>/gdp_rankings", methods=["GET"])
def get_region_gdp_rankings(region_name):
    rank_type = request.args.get("rank_type")
    base_q = "SELECT country, gdp_per_capita, rank_type, rank_position FROM region_gdp_rankings WHERE region = :r"
    params = {"r": region_name}
    if rank_type in ("top", "bottom"):
        base_q += " AND rank_type = :rt"
        params["rt"] = rank_type
    base_q += " ORDER BY rank_type, rank_position;"
    df = pd.read_sql(text(base_q), con=engine, params=params)
    if df.empty:
        abort(404, description=f"No GDP rankings found for region '{region_name}' with type '{rank_type}'.")
    return jsonify(df.to_dict(orient="records"))

# (Optional) GET /api/gdp_rankings - all rankings
@app.route("/api/gdp_rankings", methods=["GET"])
def get_all_gdp_rankings():
    df = pd.read_sql("SELECT * FROM region_gdp_rankings;", con=engine)
    return jsonify(df.to_dict(orient="records"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001, debug=True)
