-- migrations/001_create_countries_table.sql

CREATE TABLE IF NOT EXISTS countries (
  id                  INT           AUTO_INCREMENT PRIMARY KEY,
  country             VARCHAR(100)  NOT NULL,
  region              VARCHAR(100)  NOT NULL,
  population          BIGINT,
  area_sq_mi          FLOAT,
  pop_density         FLOAT,
  coastline_ratio     FLOAT,
  net_migration       FLOAT,
  infant_mortality    FLOAT,
  gdp_per_capita      FLOAT,
  literacy            FLOAT,
  phones_per_1000     FLOAT,
  arable              FLOAT,
  crops               FLOAT,
  other               FLOAT,
  climate             TINYINT,
  birthrate           FLOAT,
  deathrate           FLOAT,
  agriculture         FLOAT,
  industry            FLOAT,
  service             FLOAT
) ENGINE=InnoDB
  DEFAULT CHARSET = utf8mb4;
