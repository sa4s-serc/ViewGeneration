from diagrams import Diagram
from diagrams.aws.iot import IotSensor
from diagrams.aws.network import InternetGateway
from diagrams.aws.compute import EC2
from diagrams.aws.mobile import APIGateway
from diagrams.aws.integration import SNS
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3

with Diagram("BLE Beacon Scanner Architecture", show=False, direction="LR"):
    ble_beacons = IotSensor("BLE Beacons")
    esp32 = EC2("ESP32 Scanner")
    wifi = InternetGateway("WiFi Network")
    mqtt_broker = SNS("MQTT Broker")
    data_processor = APIGateway("Data Processor")
    storage = Dynamodb("Data Storage")
    analytics = S3("Analytics")

    ble_beacons >> esp32
    esp32 >> wifi
    wifi >> mqtt_broker
    mqtt_broker >> data_processor
    data_processor >> storage
    data_processor >> analytics