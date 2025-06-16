-- migrations/004_populate_region_analysis.sql

INSERT INTO region_analysis (
  region, total_population, mean_gdp, median_gdp, mean_literacy, median_literacy
)
SELECT
  region,
  SUM(population) AS total_population,
  AVG(gdp_per_capita) AS mean_gdp,
  (
    SELECT AVG(val) FROM (
      SELECT gdp_per_capita AS val,
             ROW_NUMBER() OVER (PARTITION BY region ORDER BY gdp_per_capita)         AS rn,
             COUNT(*)       OVER (PARTITION BY region)                            AS cnt
      FROM countries
    ) t
    WHERE rn IN (FLOOR((cnt+1)/2), CEIL((cnt+1)/2))
  ) AS median_gdp,
  AVG(literacy) AS mean_literacy,
  (
    SELECT AVG(val) FROM (
      SELECT literacy AS val,
             ROW_NUMBER() OVER (PARTITION BY region ORDER BY literacy)             AS rn,
             COUNT(*)       OVER (PARTITION BY region)                            AS cnt
      FROM countries
    ) t
    WHERE rn IN (FLOOR((cnt+1)/2), CEIL((cnt+1)/2))
  ) AS median_literacy
FROM countries
GROUP BY region;
