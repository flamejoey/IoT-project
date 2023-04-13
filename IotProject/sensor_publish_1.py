import random
import time
import json
from paho.mqtt import client as mqtt_client

# Function to generate random sensor values
def generate_sensor_data():
    return {
        "temperature": round(random.uniform(-50, 50), 2),
        "humidity": round(random.uniform(0, 100), 2),
        "co2": round(random.uniform(300, 2000), 2),
        "rain_height": round(random.uniform(0, 50), 2),
        "wind_direction": round(random.uniform(0, 360), 2),
        "wind_intensity": round(random.uniform(0, 100), 2),
    }

# Function to connect to the MQTT broker (AWS IoT Core) and return the client object
def connect_mqtt(broker, port, client_id, certificate_file, private_key_file):
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print(f"{client_id} connected to MQTT broker")
        else:
            print(f"Failed to connect, return code {rc}")

    client = mqtt_client.Client(client_id)
    client.tls_set(ca_certs=None, certfile=certificate_file, keyfile=private_key_file)
    client.tls_insecure_set(False)
    client.on_connect = on_connect
    client.connect(broker, port)
    client.loop_start()

    return client

# Function to publish sensor data to the MQTT topic
def publish(client, topic, data):
    payload = json.dumps(data)
    client.publish(topic, payload)

# Set up AWS IoT Core parameters
broker = "a1h8zbnjhesyy7-ats.iot.us-east-1.amazonaws.com"
port = 8883
station_id = "station_1"
certificate_file = '/Users/flamejoey/IotProject/st1-certificate.pem.crt'
private_key_file = '/Users/flamejoey/IotProject/st1-private.pem.key'
root_ca_file = '/Users/flamejoey/IotProject/AmazonRootCA1.pem'


# Connect to the MQTT broker and periodically publish sensor data
client = connect_mqtt(broker, port, station_id, certificate_file, private_key_file)
topic = f"virtual_station/{station_id}/data"

while True:
    sensor_data = generate_sensor_data()
    publish(client, topic, sensor_data)
    print(f"Published data: {sensor_data}")
    time.sleep(5)  # Adjust the interval as needed
