from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.custom import Custom
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.network import Internet
from diagrams.onprem.compute import Server
from diagrams.onprem.database import MySQL
from diagrams.onprem.monitoring import Prometheus
from diagrams.programming.framework import Flask

with Diagram("Weather Station Architecture", show=False, direction="TB"):
    with Cluster("Local Network"):
        esp = Custom("ESP8266", "./esp8266.png")
        openwrt = Server("OpenWRT Router")
        local_db = MySQL("RRDTool DB")
        monitoring = Cluster("Monitoring Stack")
        with monitoring:
            prometheus = Prometheus("Prometheus")
            grafana = Grafana("Grafana")

    with Cluster("Cloud Services"):
        thingspeak = Custom("ThingSpeak", "./thingspeak.png")
        github = Custom("GitHub", "./github.png")

    # Data flow
    esp >> openwrt
    openwrt >> local_db
    local_db >> prometheus
    prometheus >> grafana
    
    # Cloud connections
    esp >> thingspeak
    openwrt >> github

    # HTTP Server
    esp >> Internet("Local HTTP\nInterface")