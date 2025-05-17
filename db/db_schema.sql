USE citibike;

CREATE TABLE IF NOT EXISTS station_status (
    id INT AUTO_INCREMENT PRIMARY KEY,
    timestamp DATETIME,
    station_name VARCHAR(255),
    station_id VARCHAR(255),
    longitude DOUBLE,
    latitude DOUBLE,
    capacity INT,
    bikes_available INT,
    percent_filled FLOAT,
    percent_empty FLOAT
);
