# 🌱 Raspberry Pi Environment Monitoring Simulator

A simulated Raspberry Pi environment with two virtual sensors: **temperature** and **humidity**.  
This project demonstrates a typical IoT system architecture: generating sensor data, processing it, storing it locally, and sending it to the cloud (Azure IoT Hub).

---

## 🎯 Project Goals

- 🔌 Simulate sensor behavior without physical hardware  
- 🐍 Showcase skills in **Python**, multiprocessing, and database integration  
- ☁️ Demonstrate **IoT data flow management** (sensors → processing → database → cloud)  
- 💾 Provide **data resilience** with local SQLite storage when cloud connectivity is unavailable  

---

## 🛠️ Technologies Used

- **Python 3**  
- **Multiprocessing** – concurrent sensor processes  
- **SQLite** – local database for resilience  
- **Azure IoT Hub** – cloud service for receiving data  
- **dotenv** – environment variable management (secure cloud connection)  

---

## 📂 Project Structure

```
Raspberry-Pi-Temperature-Humidity-Simulation/
├── humidity_sensor.py       # Simulated humidity sensor
├── temperature_sensor.py    # Simulated temperature sensor
├── raspberry_emulaattori.py # Main program: combines, stores, and sends data
├── sensor_data.db           # SQLite database (auto-created)
├── secrets.env              # Azure IoT Hub connection string (not in version control)
└── README.md
```

---

## 🚀 How to Run

⚠️ **Requirements**  
Make sure you have **Python 3.10 or later** and **pip** installed and added to your system PATH.  

```python
python --version
pip --version
```

### 1. Clone the repository

### 2. Set up environment variables  
Create a file named `secrets.env` and add your Azure IoT Hub connection string:
AZURE_CONNECTION_STRING=PASTE_YOUR_CONNECTION_STRING_HERE

### 3. Install dependencies

```python
pip install -r requirements.txt
```

### 4. Run the simulation

```python
python raspberry_emulaattori.py
```

---

## 📊 Example Output

```
Sensor processes started successfully
SQLite database initialized successfully
Generated temperature data: {'temperature': 25.8}
Generated humidity data: {'humidity': 42.1}
Received temperature data: {'temperature': 25.8}
Received humidity data: {'humidity': 42.1}
Saving data to local database: {...}
Sent to Azure: {"device_time": "2025-09-14 14:35:20", "temperature": 25.8, "humidity": 42.1}
Combined sensor data: {...}
```

---

## 🔒 Security Considerations

- 🔑 The Azure IoT Hub connection string is stored in `secrets.env` (excluded from version control).
- 🗄️ Local SQLite storage acts as a buffer if the cloud connection is unavailable.

---
