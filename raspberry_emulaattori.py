from multiprocessing import Process, Queue
from datetime import datetime
import sqlite3
import time
import json
from azure.iot.device import IoTHubDeviceClient
from humidity_sensor import generate_humidity_data
from temperature_sensor import generate_temperature_data
from dotenv import load_dotenv
import os

def initialize_azure():
    """Alustetaan Azure IoT Hub -yhteys."""
    try:
        client = IoTHubDeviceClient.create_from_connection_string(CONNECTION_STRING)
        print("Azure IoT Hub connection successful")
        return client
    except Exception as e:
        print(f"Failed to connect to Azure IoT Hub: {e}")
        return None

def initialize_database():
    """Alustetaan SQLite-tietokanta."""
    conn = sqlite3.connect("sensor_data.db", check_same_thread=False)
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS data (device_time TEXT, temperature REAL, humidity REAL)")
    conn.commit()
    print("SQLite database initialized successfully")
    return conn, cursor

def save_to_local_db(cursor, conn, data):
    """Tallenna data paikallisesti tietoliikennekatkojen varalta."""
    print(f"Saving data to local database: {data}")
    cursor.execute(
        "INSERT INTO data (device_time, temperature, humidity) VALUES (?, ?, ?)",
        (data["device_time"], data["temperature"], data["humidity"]),
    )
    conn.commit()

def send_to_azure(client, data):
    """Lähetä data Azure IoT Hubiin."""
    if not client:
        print("Azure client is not initialized, skipping send")
        return

    try:
        message = json.dumps(data)  # Muuta data JSON-muotoon
        client.send_message(message)
        print(f"Sent to Azure: {message}")
    except Exception as e:
        print(f"Failed to send to Azure: {e}")
        print(f"Data being sent: {data}")

def main():
    # Luo viestintäjonot antureille
    humidity_queue = Queue()
    temperature_queue = Queue()

    # Käynnistä anturiprosessit
    humidity_process = Process(target=generate_humidity_data, args=(humidity_queue,))
    temperature_process = Process(target=generate_temperature_data, args=(temperature_queue,))
    humidity_process.start()
    temperature_process.start()
    print("Sensor processes started successfully")

    # Alustetaan Azure ja SQLite
    client = initialize_azure()
    conn, cursor = initialize_database()

    try:
        while True:
            # Lue anturidata
            humidity_data = None
            temperature_data = None

            if not humidity_queue.empty():
                humidity_data = humidity_queue.get()
                print(f"Received humidity data: {humidity_data}")

            if not temperature_queue.empty():
                temperature_data = temperature_queue.get()
                print(f"Received temperature data: {temperature_data}")

            if humidity_data and temperature_data:
                # Yhdistä data ja lisää aikaleima
                combined_data = {
                    "device_time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    "humidity": humidity_data["humidity"],
                    "temperature": temperature_data["temperature"],
                }

                # Tallenna paikalliseen tietokantaan
                save_to_local_db(cursor, conn, combined_data)

                # Lähetä Azure IoT Hubiin
                send_to_azure(client, combined_data)

                # Tulosta yhdistetty data
                print(f"Combined sensor data: {combined_data}")
            
            time.sleep(20)  # Odota ennen seuraavaa kierrosta 20 sekunttia
    except KeyboardInterrupt:
        print("Stopping processes...")
        humidity_process.terminate()
        temperature_process.terminate()
        humidity_process.join()
        temperature_process.join()
        print("Processes stopped cleanly")

if __name__ == "__main__":
    # Ladataan secrets.env-tiedosto, joka sisältää ympäristömuuttujat
    load_dotenv("secrets.env")  # Varmista, että secrets.env on samassa hakemistossa
    # Haetaan connection string ympäristömuuttujasta
    CONNECTION_STRING = os.getenv("AZURE_CONNECTION_STRING")
    if not CONNECTION_STRING:
        raise ValueError("Azure connection string not set in environment variables")
    main()
