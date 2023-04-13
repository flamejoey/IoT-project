import paho.mqtt.client as mqtt
import json
import matplotlib.pyplot as plt

data = {
    'station_1': [],
    'station_2': []
}

# Create the plot
fig, ax = plt.subplots()
lines = {}
for station_id in data:
    lines[station_id], = ax.plot([], [], label=station_id)
ax.set_xlabel('Time')
ax.set_ylabel('Temperature')
ax.legend()

def on_connect(client, userdata, flags, rc):
    print(f"Connected with result code {rc}")
    client.subscribe("stations/station1/data")
    client.subscribe("stations/station2/data")

def on_message(client, userdata, msg):
    payload = json.loads(msg.payload)
    station_id = payload['station_id']
    data[station_id].append(payload)
    print(f"Received data from {station_id}: {payload}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt.eclipseprojects.io", 1883, 60)

client.loop_start()

try:
    while True:
        for station_id in data:
            temperatures = [entry['temperature'] for entry in data[station_id]]
            x_values = list(range(len(temperatures)))
            lines[station_id].set_data(x_values, temperatures)
        ax.relim()
        ax.autoscale_view(True, True, True)
        plt.pause(5)
except KeyboardInterrupt:
    print("Interrupted by user, stopping...")
    client.loop_stop()
    client.disconnect()
