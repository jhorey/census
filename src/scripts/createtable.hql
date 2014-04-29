CREATE TABLE economic (
median INT,
mean INT,
capita INT,
state_name STRING,
state_cd STRING,
county_name STRING,
county_cd STRING
) 
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE;

CREATE TABLE population (
 total INT, 
 white INT, 
 black INT, 
 native INT, 
 asian INT, 
 pacific INT, 
 latino INT,
 state_name STRING,
 state_cd STRING,
 county_name STRING,
 county_cd STRING
) 
ROW FORMAT DELIMITED
FIELDS TERMINATED BY '|'
STORED AS TEXTFILE;