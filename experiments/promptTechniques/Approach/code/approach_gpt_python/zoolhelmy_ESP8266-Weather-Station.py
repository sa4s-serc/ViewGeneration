from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.client import User
from diagrams.onprem.network import Internet
from diagrams.onprem.compute import Server
from diagrams.programming.language import Nodejs
from diagrams.onprem.vcs import Github
from diagrams.generic.storage import Storage

with Diagram("ESP8266 Weather Station Architecture", show=False):
    user = User("Local User")
    internet = Internet("ThingSpeak Cloud")

    with Cluster("ESP8266 NodeMCU"):
        esp8266 = Nodejs("ESP8266")
        sensors = [
            Nodejs("Temperature Sensor"),
            Nodejs("Humidity Sensor"),
            Nodejs("Pressure Sensor"),
            Nodejs("UV Index Sensor"),
            Nodejs("Altitude Sensor"),
        ]

    with Cluster("OpenWRT Router"):
        openwrt = Server("OpenWRT")
        mosquitto_subscriber = Nodejs("Mosquitto Subscriber")
        collectd = Nodejs("collectd")
        rrdtool = Nodejs("RRDTool")

    github = Github("GitHub Repository")
    storage = Storage("Data Storage")

    # Connections
    user >> Edge(label="HTTP") >> esp8266
    esp8266 >> Edge(label="MQTT") >> internet
    esp8266 >> Edge(label="MQTT") >> openwrt
    esp8266 >> Edge(label="Data Collection") >> sensors
    openwrt >> Edge(label="MQTT Subscription") >> mosquitto_subscriber
    mosquitto_subscriber >> Edge(label="Data to collectd") >> collectd
    collectd >> Edge(label="Data Processing") >> rrdtool
    rrdtool >> Edge(label="Graph Generation") >> github
    rrdtool >> Edge(label="Data Storage") >> storage
    github << Edge(label="Automated Graph Push") << openwrt