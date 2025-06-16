-- migrations/002_create_region_analysis.sql

CREATE TABLE IF NOT EXISTS region_analysis (
  region            VARCHAR(100) NOT NULL PRIMARY KEY,
  total_population  BIGINT,
  mean_gdp          FLOAT,
  median_gdp        FLOAT,
  mean_literacy     FLOAT,
  median_literacy   FLOAT
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
