-- migrations/005_populate_region_gdp_rankings.sql

-- Populate top 3 by GDP per region
INSERT INTO region_gdp_rankings (
  region,
  country,
  gdp_per_capita,
  rank_type,
  rank_position
)
SELECT
  region,
  country,
  gdp_per_capita,
  'top'       AS rank_type,
  rank_position
FROM (
  SELECT
    region,
    country,
    gdp_per_capita,
    ROW_NUMBER() OVER (
      PARTITION BY region
      ORDER BY gdp_per_capita DESC
    ) AS rank_position
  FROM countries
) AS ranked
WHERE
  rank_position <= 3;

-- Populate bottom 3 by GDP per region
INSERT INTO region_gdp_rankings (
  region,
  country,
  gdp_per_capita,
  rank_type,
  rank_position
)
SELECT
  region,
  country,
  gdp_per_capita,
  'bottom'    AS rank_type,
  rank_position
FROM (
  SELECT
    region,
    country,
    gdp_per_capita,
    ROW_NUMBER() OVER (
      PARTITION BY region
      ORDER BY gdp_per_capita ASC
    ) AS rank_position
  FROM countries
) AS ranked
WHERE
  rank_position <= 3;
