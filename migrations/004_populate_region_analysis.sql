-- migrations/004_populate_region_analysis.sql

INSERT INTO region_analysis (
  region, total_population, mean_gdp, median_gdp, mean_literacy, median_literacy
)
SELECT
  region,
  SUM(population)         AS total_population,
  AVG(gdp_per_capita)     AS mean_gdp,
  PERCENTILE_CONT(0.5)
    WITHIN GROUP (ORDER BY gdp_per_capita) AS median_gdp,
  AVG(literacy)           AS mean_literacy,
  PERCENTILE_CONT(0.5)
    WITHIN GROUP (ORDER BY literacy)       AS median_literacy
FROM countries
GROUP BY region;
