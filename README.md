This project demonstrates a fully automated Weather Data ETL Pipeline built using Apache Airflow and Astro CLI, designed to seamlessly extract, transform, and load weather data into a PostgreSQL database. The pipeline is engineered to handle real-time weather data updates, providing a reliable and scalable solution for weather analytics.

🌍 City Considered

The Weather Data ETL Pipeline specifically targets New York City, but it can be easily adapted for use in other cities or regions by modifying the API endpoint, geographical parameters, and data transformations.

- City: New York City
- Region: United States
- Data Source: The weather data is fetched from OpenWeatherMap API, providing real-time weather data like temperature, wind speed, and other critical metrics.

Weather Data Features Collected:

- Temperature (Celsius/Fahrenheit)
- Windspeed
- Wind Direction
- Weather Condition (Clear, Rain, Snow, etc.)
- Timestamp

## 🚀 Getting Started
1. Clone the Repository

```bash
git clone https://github.com/shivampatil98/Weather-ETL-Pipeline-using-Airflow-and-Astro.git

cd Weather-ETL-Pipeline-using-Airflow-and-Astro
```

2. Start the Astro Project

```bash
astro dev start
```
This will spin up all services (Airflow webserver, scheduler, PostgreSQL) via Docker.

3. Access the Airflow UI
Open your browser and go to:
```bash
http://localhost:8080
```
Default credentials: username: admin | password: admin
