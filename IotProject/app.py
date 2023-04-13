from flask import Flask, render_template
import boto3
from boto3.dynamodb.conditions import Key, Attr
import time

app = Flask(__name__)

# Set up AWS credentials
dynamodb = boto3.resource(
    "dynamodb",
    region_name="us-east-1",
    aws_access_key_id="AKIA567727Y36IFRL4JI",
    aws_secret_access_key="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",
)

table = dynamodb.Table("VirtualStationData")

def get_latest_data(station_id):
    response = table.query(
        KeyConditionExpression=Key("station_id").eq(station_id),
        ScanIndexForward=False,
        Limit=1
    )
    if response["Items"]:
        return response["Items"][0]
    return None




# ...

def get_sensor_data(sensor, hours=5):
    timestamp_threshold = int(time.time()) - hours * 3600

    response = table.scan(
        FilterExpression=(Key("timestamp").gt(timestamp_threshold) & Attr(sensor).exists())
    )

    return response["Items"]


@app.route("/")
def home():
    return render_template("index.html")

@app.route("/station/<station_id>")
def station_data(station_id):
    data = get_latest_data(station_id)
    return render_template("station.html", station_id=station_id, data=data)

@app.route("/sensor/<sensor>")
def sensor_data(sensor):
    data = get_sensor_data(sensor)
    return render_template("sensor.html", sensor=sensor, data=data)

if __name__ == "__main__":
    app.run(debug=True)
