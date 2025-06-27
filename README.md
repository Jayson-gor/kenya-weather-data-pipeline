# kenya-weather-data-pipeline
A complete weather data engineering project that automates the collection, storage, and visualization of real-time and historical weather data across 10 major towns in Kenya.
This project uses Apache Airflow to fetch, process, and store weather data for Kenyan towns, with visualization in Metabase.



## 🧰 Tech Stack

| Component     | Tool/Tech                   |
|---------------|-----------------------------|
| Workflow Orchestration | Apache Airflow (Dockerized)     |
| Data Collection        | Python, OpenWeather & Weatherbit APIs |
| Database               | PostgreSQL                    |
| Visualization          | Metabase (Dockerized)         |



## 🌐 Tracked Towns
Nairobi, Mombasa, Kisumu, Nakuru, Eldoret, Nyeri, Kakamega, Thika, Garissa, Kitale

---

## 📊 Features

✅ Hourly streaming of current weather data  
✅ Batch loading of previous day's weather (morning & evening)  
✅ PostgreSQL storage with duplicate protection  
✅ Scheduled using Airflow  
✅ Interactive dashboard built with Metabase  
✅ Insights like temperature trends, humidity scatter plots, heatmaps, and more

---

## 🏗️ Architecture
          +-----------------+         +-----------------+
          |  Airflow DAGs   | ----->  |  Weather APIs    |
          +-----------------+         +-----------------+
                    |
                    v
          +-------------------+
          |   Python Scripts   |
          +-------------------+
                    |
                    v
          +-------------------+
          |   PostgreSQL DB    |
          +-------------------+
                    |
                    v
          +-------------------+
          |     Metabase      |
          +-------------------+

⚙️ Setup Instructions
🐳 1. Clone and Start Docker Compose

_git clone https://github.com/<your-username>/kenya-weather-pipeline.git
cd kenya-weather-pipeline
docker compose up -d

<img width="1004" alt="image" src="https://github.com/user-attachments/assets/d27e251b-5f19-4a31-82de-514053870350" />

🗃️ 2. Connect to PostgreSQL
_docker exec -it airflow-postgres-1 psql -U postgres
CREATE DATABASE kenya_weather;

Run the table creation SQL provided above inside this DB.

<img width="1108" alt="image" src="https://github.com/user-attachments/assets/902c61fc-30b3-4933-95e4-5d7777e93f60" />

🌀 Airflow DAG: kenya_weather_pipeline
Located in: dags/kenya_weather_dag.py

Tasks:
batch_load_historical_data: Pulls weather data from Weatherbit for yesterday (6am & 6pm)

stream_current_weather: Pulls current weather hourly from OpenWeather

<img width="1277" alt="image" src="https://github.com/user-attachments/assets/79bd8d4e-60b1-425c-ad76-a57dedcd6de7" />
<img width="1277" alt="image" src="https://github.com/user-attachments/assets/5dcb62d2-4a68-4063-8170-9d338745a3ac" />
<img width="1273" alt="image" src="https://github.com/user-attachments/assets/ec38aec6-edbb-4ac9-a4d0-792f13ad9d18" />

📦 Python Scripts
Located in: weather_fetcher.py

Handles API requests, rate-limiting, PostgreSQL insertions, and error logging.

Integrates both streaming and batch weather collection

📊 Metabase Dashboard
URL: http://localhost:3000

📌 Suggested Visuals:
1. Current Weather by Town – table of latest weather
2. Temperature Trend Over Time – line chart
3. Humidity vs. Temperature – scatter plot
4. Weather Description Frequency – pie chart
5. Pressure Trend Over Time – line chart
6. Temperature by Hour of Day – heatmap
7. Total Towns Reporting – KPI card
8. Highest Temperature Today – KPI card
9. Avg Humidity Today – KPI card
10. Temperature Change vs. Yesterday – KPI card

<img width="443" alt="image" src="https://github.com/user-attachments/assets/1bfdea0f-0118-4b93-91eb-c19f59ac4285" />



# 💡 How This Project Benefits a Data Engineer

This end-to-end weather data pipeline showcases the essential skill set every data engineer must master—automating data collection, ensuring reliable storage, and enabling downstream analytics. It demonstrates real-world integration with external APIs, effective use of Airflow for orchestration, and Docker-based environment isolation for portability. By ingesting both batch and streaming data into PostgreSQL and visualizing insights with Metabase, the project reinforces core ETL/ELT concepts, scheduling, data modeling, and pipeline monitoring. It also emphasizes good practices like logging, error handling, rate-limiting, and conflict resolution in inserts. This architecture can serve as a reusable framework for any geo-temporal data ingestion use case and prepares data engineers to build production-grade pipelines that drive analytics and decision-making.











