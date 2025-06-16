-- migrations/003_create_region_gdp_rankings.sql

CREATE TABLE IF NOT EXISTS region_gdp_rankings (
  region           VARCHAR(100) NOT NULL,
  country          VARCHAR(100) NOT NULL,
  gdp_per_capita   FLOAT,
  rank_type        ENUM('top','bottom') NOT NULL,
  rank_position    TINYINT UNSIGNED NOT NULL,
  PRIMARY KEY (region, rank_type, rank_position)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4;
