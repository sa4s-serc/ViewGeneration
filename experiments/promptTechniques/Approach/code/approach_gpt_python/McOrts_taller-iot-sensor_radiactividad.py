from diagrams import Diagram
from diagrams.aws.iot import IotDeviceGateway, IotCore, IotMqtt
from diagrams.onprem.network import Nginx
from diagrams.programming.language import Python
from diagrams.onprem.container import Docker
from diagrams.onprem.analytics import Metabase
from diagrams.onprem.queue import Rabbitmq

with Diagram("Geiger Counter IoT Sensor Architecture", show=False):
    device = IotDeviceGateway("ESP8266")
    geiger = IotCore("Geiger Counter Module")
    mqtt = IotMqtt("MQTT Broker")
    nginx = Nginx("Node-RED")
    python = Python("GMC.MAP")
    docker = Docker("Docker")
    functions = Python("Arduino IDE")
    metabase = Metabase("Visualization & Storage")
    rabbitmq = Rabbitmq("MQTT Commands")

    device >> geiger >> mqtt >> nginx >> python
    device >> functions
    mqtt >> docker >> metabase
    mqtt >> rabbitmq