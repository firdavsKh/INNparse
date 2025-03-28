CREATE USER docker WITH PASSWORD 'taxes4omor!';
-- CREATE DATABASE docker;

CREATE DATABASE db_stat_dep WITH ENCODING 'UTF-8' OWNER docker;
\c db_stat_dep;
SET ROLE docker;
CREATE SCHEMA sma_stat_dep;

-- GRANT ALL PRIVILEGES ON DATABASE db_stat_dep TO docker;
-- GRANT ALL PRIVILEGES ON SCHEMA sma_stat_dep TO docker;

CREATE TABLE sma_stat_dep.tbl_tax_id (
  id SERIAL PRIMARY KEY,
  inn VARCHAR(9) UNIQUE,
  upload_tstmp TIMESTAMP,
  update_tstmp TIMESTAMP,
  required_update BOOLEAN
);

CREATE TABLE sma_stat_dep.tbl_individuals (
  id SERIAL PRIMARY KEY,
  tax_id INT REFERENCES sma_stat_dep.tbl_tax_id(id),
  fst_name VARCHAR(255), 
  lst_name VARCHAR(255), 
  full_name VARCHAR(255),
  sex BOOLEAN,
  brth_date DATE,
  citizenship_1 INT,
  citizenship_2 INT,
  upload_tstmp TIMESTAMP,
  update_tstmp TIMESTAMP,
  required_update BOOLEAN
);

CREATE TABLE sma_stat_dep.tbl_document (
  id SERIAL PRIMARY KEY,
  document_type VARCHAR (100),
  document_id VARCHAR (100),
  issuer VARCHAR (100),
  issue_date DATE,
  expiration_date DATE,
  upload_tstmp TIMESTAMP,
  update_tstmp TIMESTAMP,
  status BOOLEAN 
);

CREATE TABLE sma_stat_dep.tbl_addresses (
  id SERIAL PRIMARY KEY,
  inspection_name VARCHAR(255),
  inspection_code INT,
  inspection_id INT,
  address_text VARCHAR(255),
  address_phone VARCHAR(50),
  address_kpp VARCHAR(50),
  upload_tstmp TIMESTAMP,
  update_tstmp TIMESTAMP,
  status BOOLEAN
);

CREATE TABLE sma_stat_dep.tbl_sole_enterprise (
  id SERIAL PRIMARY KEY,
  tax_id INT REFERENCES sma_stat_dep.tbl_tax_id(id),
  tax_uid VARCHAR(10) UNIQUE,
  reg_date DATE,
  upload_tstmp TIMESTAMP,
  update_tstmp TIMESTAMP,
  status BOOLEAN
);

CREATE TABLE sma_stat_dep.tbl_tax_queue (
  id SERIAL PRIMARY KEY,
  inn_code VARCHAR(10),
  region_section_code INT,
  last_seven_numb VARCHAR(10),
  status BOOLEAN
);
