-- Create the kenya_weather database
CREATE DATABASE kenya_weather;

-- Connect to the database
\c kenya_weather

-- Create the kenya_weather table
CREATE TABLE IF NOT EXISTS kenya_weather (
    id SERIAL PRIMARY KEY,
    town VARCHAR(100) NOT NULL,
    temperature FLOAT NOT NULL,
    humidity INTEGER NOT NULL,
    weather_description VARCHAR(255),
    wind_speed FLOAT,
    pressure INTEGER,
    timestamp TIMESTAMP NOT NULL,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    CONSTRAINT unique_town_timestamp UNIQUE (town, timestamp)
);

-- Grant permissions (adjust as needed)
GRANT ALL PRIVILEGES ON DATABASE kenya_weather TO postgres;
GRANT ALL ON kenya_weather TO postgres;
