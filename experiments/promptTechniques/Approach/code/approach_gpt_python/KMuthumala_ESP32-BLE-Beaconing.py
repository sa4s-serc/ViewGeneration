from diagrams import Diagram, Cluster, Edge
from diagrams.generic.network import Router
from diagrams.generic.device import Tablet
from diagrams.generic.os import LinuxGeneral
from diagrams.generic.storage import Storage

with Diagram("BLE Beacon Scanner Architecture", show=False, direction="TB"):

    with Cluster("ESP32 Microcontroller"):
        ble_scanner = Tablet("BLE Scanner\n(scan_ble())")
        wifi_module = LinuxGeneral("WiFi Module\n(setup_wifi())")
        mqtt_client = Router("MQTT Client\n(callback())")
    
    mqtt_broker = Storage("MQTT Broker")

    ble_scanner >> Edge(label="BLE Scan Data\n(MAC, RSSI)") >> mqtt_client
    wifi_module << Edge(label="WiFi Connectivity\n(setup_wifi(), reconnectWifi())") >> mqtt_client
    mqtt_client >> Edge(label="Publish Data\n(MQTT)") >> mqtt_broker
    mqtt_broker << Edge(label="Receive Commands\n(MQTT)") << mqtt_client