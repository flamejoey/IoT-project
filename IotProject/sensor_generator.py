import random
from AWSIoTPythonSDK.MQTTLib import AWSIoTMQTTClient
import boto3
import json
import time



dynamodb = boto3.resource('dynamodb', region_name='your-region')

table = dynamodb.Table('your-table-name')

def generate_random_sensor_values():
    temperature = random.uniform(-50, 50)
    humidity = random.uniform(0, 100)
    co2 = random.uniform(300, 2000)
    rain_height = random.uniform(0, 50)
    wind_direction = random.uniform(0, 360)
    wind_intensity = random.uniform(0, 100)

    return {
        'station_id': 'myStation_1',
        'timestamp': int(time.time()),
        'temperature': temperature,
        'humidity': humidity,
        'co2': co2,
        'rain_height': rain_height,
        'wind_direction': wind_direction,
        'wind_intensity': wind_intensity
    }




# Set your certificate, private key, and root CA file paths
certificate_file = '/Users/flamejoey/IotProject/st1-certificate.pem.crt'
private_key_file = '/Users/flamejoey/IotProject/st1-private.pem.key'
root_ca_file = '/Users/flamejoey/IotProject/AmazonRootCA1.pem'

# Set your AWS IoT custom endpoint
mqtt_broker_endpoint = 'a1h8zbnjhesyy7-ats.iot.us-east-1.amazonaws.com'

# Create and configure the AWS IoT MQTT client
client = AWSIoTMQTTClient('myStation_1')  # Replace 'myVirtualStation' with a unique name
client.configureEndpoint(mqtt_broker_endpoint, 8883)
client.configureCredentials(root_ca_file, private_key_file, certificate_file)
client.configureConnectDisconnectTimeout(10)
client.configureMQTTOperationTimeout(5)


def callback(client, userdata, message):
    payload = json.loads(message.payload)
    print(f"Received data from {payload['station_id']}: {payload}")

# Connect to AWS IoT Core and start listening for messages
client.connect()
client.subscribe('stations/+/data', 1, callback)

# Wait for messages indefinitely

while True:
    sensor_data = generate_random_sensor_values()

    response = table.put_item(
        Item=sensor_data
    )

    print(response)

    time.sleep(1)