from diagrams import Diagram, Cluster, Edge
from diagrams.programming.language import Arduino
from diagrams.iot.device import Device
from diagrams.onprem.queue import Mqtt
from diagrams.generic.os import Windows
from diagrams.generic.application import Application

with Diagram("Geiger Counter IoT Sensor Architecture", show=False, direction="TB"):
    esp8266 = Device("ESP8266 (WEMOS D1 mini Pro)")

    with Cluster("Sensing"):
        geiger_counter = Application("Geiger Counter Module")

    with Cluster("Processing"):
        arduino_ide = Arduino("Arduino IDE")
        esp8266 >> arduino_ide

    with Cluster("Communication"):
        mqtt_broker = Mqtt("MQTT Broker")
        esp8266 >> Edge(label="CPM Data") >> mqtt_broker
        mqtt_broker << Edge(label="Control Commands") << esp8266

    with Cluster("Visualization & Storage"):
        node_red = Application("Node-RED")
        gmc_map = Application("GMC.MAP")
        windows = Windows("Windows Machine")
        
        node_red >> Edge(label="Data Flow") >> gmc_map
        node_red << Edge(label="Integration") << windows

    geiger_counter >> esp8266
    esp8266 >> mqtt_broker
    mqtt_broker >> node_red