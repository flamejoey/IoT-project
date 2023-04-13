import random
import time
import json
import threading
from paho.mqtt import client as mqtt_client

def generate_sensor_data(station_id):
    sensor_data = {
        "station_id": station_id,
        "temperature": random.uniform(-50, 50),
        "humidity": random.uniform(0, 100),
        "co2": random.uniform(300, 2000),
        "rain_height": random.uniform(0, 50),
        "wind_direction": random.uniform(0, 360),
        "wind_intensity": random.uniform(0, 100),
        "timestamp": time.time()
    }
    return sensor_data

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"{userdata} connected to AWS IoT Core")
    else:
        print("Failed to connect, return code %d\n", rc)

def create_and_run_station(station_id, cert_path, key_path, aws_iot_endpoint):
    client = mqtt_client.Client(station_id)
    client.user_data_set(station_id)
    client.on_connect = on_connect
    client.tls_set(cert_path, key_path)
    client.connect(aws_iot_endpoint, 8883)

    while True:
        sensor_data = generate_sensor_data(station_id)
        for sensor_type, value in sensor_data.items():
            if sensor_type != "station_id" and sensor_type != "timestamp":
                topic = f"{station_id}/{sensor_type}"
                payload = json.dumps({"value": value, "timestamp": sensor_data["timestamp"]})
                client.publish(topic, payload)
                print(f"Published {sensor_type} data: {payload} to topic: {topic}")
        time.sleep(60)  # Publish sensor data every 60 seconds

# Replace these variables with your AWS IoT Core details and security credentials
aws_iot_endpoint = "your-aws-iot-endpoint"
stations = [
    {
        "id": "station_1",
        "cert_path": "path/to/certificate_1",
        "key_path": "path/to/private-key_1"
    },
    {
        "id": "station_2",
        "cert_path": "path/to/certificate_2",
        "key_path": "path/to/private-key_2"
    }
]

for station in stations:
    station_thread = threading.Thread(target=create_and_run_station, args=(station["id"], station["cert_path"], station["key_path"], aws_iot_endpoint))
    station_thread.start()
