import pymysql
import paho.mqtt.client as mqtt
import time

db_config = {
    "host": "localhost",
    "user": "scott",
    "password": "tiger",
    "database": "fire_alarm",
    "charset": "utf8mb4"
}

broker_address = "broker.hivemq.com"
broker_port = 1883
topic = "fire_alarm/temperature"

pipe_name = "/tmp/temp_pipe"

def save_to_database(temperature, status):
    connection = pymysql.connect(**db_config)
    with connection.cursor() as cursor:
        query = "INSERT INTO TemperatureData (temperature, status, timestamp) VALUES (%s, %s, NOW())"
        cursor.execute(query, (temperature, status))
    connection.commit()
    connection.close()

def get_status(temperature):
    if temperature >= 80.0:
        return "ALARM"
    elif temperature >= 70.0:
        return "WARNING"
    return "NORMAL"

mqtt_client = mqtt.Client()
mqtt_client.connect(broker_address, broker_port)
mqtt_client.loop_start()

try:
    with open(pipe_name, "r") as pipe:
        while True:
            line = pipe.readline().strip()
            if line:
                temperature = float(line)
                status = get_status(temperature)
                save_to_database(temperature, status)
                mqtt_client.publish(topic, f"{temperature},{status}")
                print(f"Temperature: {temperature}°C, Status: {status} (Sent to MQTT)")
except KeyboardInterrupt:
    print("Exiting...")
finally:
    mqtt_client.loop_stop()
    mqtt_client.disconnect()
