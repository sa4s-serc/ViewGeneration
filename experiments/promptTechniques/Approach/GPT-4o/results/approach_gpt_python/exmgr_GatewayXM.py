from diagrams import Diagram, Cluster, Edge
from diagrams.custom import Custom
from diagrams.onprem.network import Internet
from diagrams.onprem.compute import Server
from diagrams.generic.device import Mobile

with Diagram("exmgr_GatewayXM Architecture", show=False, direction="TB"):
    internet = Internet("Internet")
    thingsboard = Custom("Thingsboard IoT Platform", "./icons/thingsboard.png")

    with Cluster("GatewayXM"):
        kura = Custom("Eclipse Kura", "./icons/kura.png")
        kura_bundle = Custom("Kura Bundle", "./icons/kura_bundle.png")
        docker = Custom("Docker Container", "./icons/docker.png")

        kura_bundle - Edge(label="Data Forwarding") >> thingsboard
        kura >> kura_bundle
        kura >> docker

    with Cluster("Sensor Nodes"):
        sensor_node_1 = Mobile("ESP8266 Node")
        sensor_node_2 = Mobile("ESP32 Node")

        sensor_node_1 - Edge(label="Mesh Network") - sensor_node_2
        sensor_node_1 >> kura
        sensor_node_2 >> kura

    modbus_device = Mobile("Modbus Smart Meter")
    modbus_device >> kura

    kura << Edge(label="OTA Updates") << internet
    sensor_node_1 << Edge(label="OTA Updates") << internet
    sensor_node_2 << Edge(label="OTA Updates") << internet