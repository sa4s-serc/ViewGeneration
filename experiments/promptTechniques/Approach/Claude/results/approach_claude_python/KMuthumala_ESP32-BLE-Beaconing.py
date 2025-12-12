from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB
from diagrams.aws.database import RDS
from diagrams.aws.network import VPC
from diagrams.aws.iot import IotMqtt
from diagrams.aws.storage import S3
from diagrams.aws.network import VPCRouter

with Diagram("BLE Beacon Scanner Architecture", show=False):
    with Cluster("AWS Cloud"):
        with Cluster("VPC"):
            mqtt = IotMqtt("MQTT Broker")
            storage = S3("Data Storage")
            router = VPCRouter("Router")

        with Cluster("ESP32 Scanner Devices"):
            scanners = [EC2("BLE Scanner 1"),
                       EC2("BLE Scanner 2")]

    # Add connections
    for scanner in scanners:
        scanner >> router >> mqtt
        mqtt >> storage