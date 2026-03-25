from airflow import DAG
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.decorators import task
from datetime import datetime  # ✅ Fix 1: replaced days_ago with datetime

LATITUDE = '40.7128'
LONGITUDE = '-74.0060'

POSTGRES_CONN_ID = 'postgres_default'
API_CONN_ID = 'open_meteo_api'

default_args = {
    'owner': 'airflow',
    'start_date': datetime(2024, 1, 1),  # ✅ Fix 2: use datetime instead of days_ago
}

with DAG(dag_id='weather_data_pipeline',
         default_args=default_args,
         schedule='@daily',
         catchup=False) as dag:  # ✅ Fix 3: renamed 'dags' to 'dag' (convention)

    @task
    def fetch_weather_data():
        http_hook = HttpHook(method='GET', http_conn_id=API_CONN_ID)
        endpoint = f'/v1/forecast?latitude={LATITUDE}&longitude={LONGITUDE}&current_weather=true'
        response = http_hook.run(endpoint)
        return response.json()

    @task
    def transform_weather_data(weather_data):
        current_weather = weather_data.get('current_weather')
        transformed_data = {
            'latitude': LATITUDE,
            'longitude': LONGITUDE,
            'temperature': current_weather.get('temperature'),
            'windspeed': current_weather.get('windspeed'),
            'winddirection': current_weather.get('winddirection'),
            'weathercode': current_weather.get('weathercode'),
            'time': current_weather.get('time')
        }
        return transformed_data

    @task
    def load_weather_data(transformed_data):
        postgres_hook = PostgresHook(postgres_conn_id=POSTGRES_CONN_ID)
        conn = postgres_hook.get_conn()
        cursor = conn.cursor()

        cursor.execute("""
            CREATE TABLE IF NOT EXISTS weather_data (
                id SERIAL PRIMARY KEY,
                latitude FLOAT,
                longitude FLOAT,
                temperature FLOAT,
                windspeed FLOAT,
                winddirection FLOAT,
                weathercode INT,
                time TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            );
        """)

        cursor.execute("""
            INSERT INTO weather_data (latitude, longitude, temperature, windspeed, winddirection, weathercode, time)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (
            transformed_data['latitude'],
            transformed_data['longitude'],
            transformed_data['temperature'],
            transformed_data['windspeed'],
            transformed_data['winddirection'],
            transformed_data['weathercode'],
            transformed_data['time']
        ))

        conn.commit()
        cursor.close()

    # ✅ All inside 'with DAG' block - correct indentation
    weather_data = fetch_weather_data()
    transformed_data = transform_weather_data(weather_data)
    load_weather_data(transformed_data)
