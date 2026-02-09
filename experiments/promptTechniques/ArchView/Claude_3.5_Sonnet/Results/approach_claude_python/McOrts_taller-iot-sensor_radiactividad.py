from diagrams import Diagram, Cluster
from diagrams.aws.iot import IotSensor, IotRule, IotAnalytics
from diagrams.aws.integration import SNS
from diagrams.aws.network import VPCRouter
from diagrams.aws.compute import Lambda
from diagrams.onprem.monitoring import Grafana

with Diagram("Geiger Counter IoT Architecture", show=False):
    with Cluster("IoT Device"):
        sensor = IotSensor("Geiger Counter")
        esp8266 = VPCRouter("ESP8266")

    with Cluster("Data Processing"):
        mqtt = IotRule("MQTT Broker")
        analytics = IotAnalytics("Data Processing")

    with Cluster("Visualization"):
        nodered = Lambda("Node-RED")
        grafana = Grafana("GMC.MAP")

    sensor >> esp8266 >> mqtt >> analytics
    analytics >> nodered >> grafana
    mqtt >> SNS("Notifications")