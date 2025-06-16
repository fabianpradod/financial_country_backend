# Financial Country Backend

A Python-based backend system that ingests global country data, performs financial and demographic analysis, and exposes RESTful APIs for data consumption. Built with Flask, MySQL, and pandas for comprehensive country analytics.

## Overview

This project processes country-level financial and demographic data from CSV sources, stores it in a MySQL database, and provides analytical insights through a REST API. The system includes data validation, cleaning, and analytical aggregations to support financial and demographic research.

## Features

- **Data Ingestion**: CSV data loading with validation and error handling
- **Data Analysis**: Regional analytics including GDP, population, and literacy metrics
- **RESTful API**: Flask-based endpoints for country and regional data
- **Data Quality**: Comprehensive data cleaning and validation processes
- **Regional Insights**: Aggregated statistics and rankings by geographic region
- **Docker Support**: Containerized MySQL database for development

## Architecture

```
financial_country_backend/
├── api/                    # Flask API application
│   ├── __init__.py
│   └── app.py             # Main Flask application with endpoints
├── data/                   # Data storage directory
├── migrations/             # Database schema and setup scripts
│   ├── 000_create_database.sql
│   ├── 001_create_countries_table.sql
│   ├── 002_create_region_analysis.sql
│   ├── 003_create_region_gdp_rankings.sql
│   ├── 004_populate_region_analysis.sql
│   └── 005_populate_region_gdp_rankings.sql
├── load_data.py           # CSV data ingestion script
├── data_analysis.py       # Data cleaning and analysis
└── requirements.txt       # Python dependencies
```

## Getting Started

### Prerequisites

- Python 3.8+
- Docker (for MySQL container)
- pip package manager

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/financial_country_backend.git
   cd financial_country_backend
   ```

2. **Install Python dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Start MySQL Docker container**
   ```bash
   docker run --name mysql-dev -e MYSQL_ROOT_PASSWORD=devpass123 -p 3306:3306 -d mysql:8.0
   ```

4. **Set up environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your database credentials
   ```

5. **Initialize database**
   ```bash
   # Execute migration scripts in order
   docker exec -i mysql-dev mysql -u root -pdevpass123 < migrations/000_create_database.sql
   docker exec -i mysql-dev mysql -u root -pdevpass123 < migrations/001_create_countries_table.sql
   # ... continue with remaining migrations
   ```

## Data Pipeline

### 1. Data Loading
```bash
python load_data.py --csv data/countries_of_the_world.csv
```
- Validates CSV data format and content
- Handles data type conversions and null values
- Logs errors to `errors.log` for debugging
- Bulk inserts validated records into MySQL

### 2. Data Analysis
```bash
python data_analysis.py
```
- Connects to MySQL and loads country data
- Performs data cleaning and validation
- Generates regional analytics and statistics
- Exports cleaned data to CSV format

### 3. API Server
```bash
python api/app.py
```
- Starts Flask development server on port 5001
- Provides RESTful endpoints for data access
- Handles CORS for frontend integration

## API Endpoints

### Countries
- `GET /api/countries` - List all countries with basic information
- `GET /api/countries/<country_name>` - Detailed data for specific country

### Regions
- `GET /api/regions` - Regional analytics and aggregated statistics
- `GET /api/regions/<region_name>` - Analytics for specific region
- `GET /api/regions/<region_name>/gdp_rankings?rank_type=top|bottom` - GDP rankings within region

### Rankings
- `GET /api/gdp_rankings` - Global GDP rankings across all regions

## Data Analysis Features

### Regional Analytics
- **Population Metrics**: Total population by region
- **Economic Indicators**: Mean and median GDP per capita
- **Education Statistics**: Literacy rate analysis
- **Comparative Rankings**: Top/bottom performers by region

### Data Quality Checks
- Duplicate country detection
- Population validation (positive values)
- GDP outlier identification
- Missing data handling

## Database Schema

### Core Tables
- **`countries`**: Primary country data with 20+ demographic and economic indicators
- **`region_analysis`**: Aggregated regional statistics
- **`region_gdp_rankings`**: Top/bottom GDP performers by region

### Key Metrics
- Population, Area, Population Density
- GDP per Capita, Economic Sectors (Agriculture, Industry, Service)
- Demographics (Birth/Death rates, Migration, Infant Mortality)
- Infrastructure (Literacy, Phone access)
- Geography (Coastline, Climate, Land use)

## Development

### Running Tests
```bash
# Test data loading
python load_data.py --csv data/sample_countries.csv

# Test analysis pipeline
python data_analysis.py

# Test API endpoints
curl http://localhost:5001/api/countries
```

### Docker MySQL Management
```bash
# Start container
docker start mysql-dev

# Access MySQL shell
docker exec -it mysql-dev mysql -u root -p

# View logs
docker logs mysql-dev
```

## Dependencies

### Core Libraries
- **Flask**: Web framework for REST API
- **pandas**: Data manipulation and analysis
- **SQLAlchemy**: Database ORM and connection management
- **mysql-connector-python**: MySQL database driver

### Supporting Libraries
- **flask-cors**: Cross-origin resource sharing
- **python-dotenv**: Environment variable management
- **awscli**: AWS integration for cloud deployment
