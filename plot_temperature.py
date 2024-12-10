import matplotlib.pyplot as plt
import pymysql
import pandas as pd
import time

db_config = {
    "host": "localhost",
    "user": "scott",
    "password": "tiger",
    "database": "fire_alarm",
    "charset": "utf8mb4"
}

def fetch_latest_data():
    connection = pymysql.connect(**db_config)
    query = "SELECT timestamp, temperature, status FROM TemperatureData ORDER BY id DESC LIMIT 50"
    data = pd.read_sql(query, connection)
    connection.close()
    return data

plt.ion()
fig, ax = plt.subplots(figsize=(10, 6))

while True:
    data = fetch_latest_data()
    ax.clear()
    ax.plot(data["timestamp"], data["temperature"], label="Temperature (°C)")
    
    warnings = data[data["status"] == "WARNING"]
    alarms = data[data["status"] == "ALARM"]
    ax.scatter(warnings["timestamp"], warnings["temperature"], color="orange", label="Warning", zorder=5)
    ax.scatter(alarms["timestamp"], alarms["temperature"], color="red", label="Alarm", zorder=5)
    
    ax.set_title("Real-Time Temperature Monitoring")
    ax.set_xlabel("Time")
    ax.set_ylabel("Temperature (°C)")
    ax.legend()
    ax.grid(True)
    plt.pause(1)
