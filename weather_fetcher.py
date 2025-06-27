import requests
import psycopg2
from datetime import datetime, timedelta
import logging
import time

# Configure logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# API configuration
OPENWEATHER_API_KEY = "******************"  # For current weather
WEATHERBIT_API_KEY = "*******************"  # For historical weather
OPENWEATHER_BASE_URL = "http://api.openweathermap.org/data/2.5"
WEATHERBIT_HISTORICAL_URL = "https://api.weatherbit.io/v2.0/history/hourly"
TOWNS = [
    {"name": "Nairobi", "lat": -1.286389, "lon": 36.817223},
    {"name": "Mombasa", "lat": -4.043477, "lon": 39.668206},
    {"name": "Kisumu", "lat": -0.091702, "lon": 34.767956},
    {"name": "Nakuru", "lat": -0.303099, "lon": 36.080026},
    {"name": "Eldoret", "lat": 0.514277, "lon": 35.269780},
    {"name": "Nyeri", "lat": -0.420130, "lon": 36.947589},
    {"name": "Kakamega", "lat": 0.282731, "lon": 34.751966},
    {"name": "Thika", "lat": -1.033333, "lon": 37.069328},
    {"name": "Garissa", "lat": -0.453229, "lon": 39.646099},
    {"name": "Kitale", "lat": 1.019089, "lon": 35.002305}
]

# PostgreSQL configuration
DB_CONFIG = {
    "dbname": "kenya_weather",
    "user": "postgres",
    "password": "Comfortzone",
    "host": "host.docker.internal",
    "port": "5432"
}

def get_db_connection():
    try:
        conn = psycopg2.connect(**DB_CONFIG)
        return conn
    except Exception as e:
        logging.error(f"Database connection failed: {e}")
        raise

def insert_weather_data(town, data, timestamp):
    conn = get_db_connection()
    try:
        with conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO kenya_weather (town, temperature, humidity, weather_description, wind_speed, pressure, timestamp)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
                """,
                (
                    town,
                    data["temp"],
                    data["humidity"],
                    data["weather"][0]["description"],
                    data["wind_speed"],
                    data["pressure"],
                    timestamp
                )
            )
        conn.commit()
        logging.info(f"Inserted data for {town} at {timestamp}")
    except Exception as e:
        logging.error(f"Failed to insert data for {town}: {e}")
    finally:
        conn.close()

def fetch_historical_weather(town, timestamp):
    start_date = timestamp.strftime('%Y-%m-%d:%H')
    end_date = (timestamp + timedelta(hours=1)).strftime('%Y-%m-%d:%H')
    url = f"{WEATHERBIT_HISTORICAL_URL}?lat={town['lat']}&lon={town['lon']}&start_date={start_date}&end_date={end_date}&key={WEATHERBIT_API_KEY}"
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("data"):
            weather_data = {
                "temp": data["data"][0]["temp"],
                "humidity": data["data"][0]["rh"],
                "weather": [{"description": data["data"][0]["weather"]["description"]}],
                "wind_speed": data["data"][0]["wind_spd"],
                "pressure": data["data"][0]["pres"]
            }
            insert_weather_data(town["name"], weather_data, timestamp)
        else:
            logging.warning(f"No historical data for {town['name']} at {timestamp}")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 429:
            logging.error(f"Rate limit exceeded for WeatherBit API: {e}")
        else:
            logging.error(f"Failed to fetch historical weather for {town['name']} at {timestamp}: {e}")
    except Exception as e:
        logging.error(f"Failed to fetch historical weather for {town['name']} at {timestamp}: {e}")
    time.sleep(1)  # Rate-limiting

def batch_load_historical_data():
    end_date = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
    start_date = end_date - timedelta(days=1)  # Limited to 24 hours for free tier
    current_date = start_date
    while current_date < end_date:
        morning = current_date.replace(hour=6, minute=0)
        evening = current_date.replace(hour=18, minute=0)
        for town in TOWNS:
            fetch_historical_weather(town, morning)
            fetch_historical_weather(town, evening)
        current_date += timedelta(days=1)
    logging.info("Completed batch loading of historical data")

def stream_current_weather():
    for town in TOWNS:
        url = f"{OPENWEATHER_BASE_URL}/weather?lat={town['lat']}&lon={town['lon']}&appid={OPENWEATHER_API_KEY}&units=metric"
        try:
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()
            weather_data = {
                "temp": data["main"]["temp"],
                "humidity": data["main"]["humidity"],
                "weather": data["weather"],
                "wind_speed": data["wind"]["speed"],
                "pressure": data["main"]["pressure"]
            }
            timestamp = datetime.fromtimestamp(data["dt"])
            insert_weather_data(town["name"], weather_data, timestamp)
        except Exception as e:
            logging.error(f"Failed to fetch current weather for {town['name']}: {e}")
    logging.info("Completed streaming current weather")
