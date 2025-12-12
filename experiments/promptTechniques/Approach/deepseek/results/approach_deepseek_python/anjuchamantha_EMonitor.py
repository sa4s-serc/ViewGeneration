from diagrams import Diagram, Cluster
from diagrams.aws.iot import IotButton
from diagrams.onprem.client import Client
from diagrams.onprem.network import Internet
from diagrams.onprem.database import Redis
from diagrams.onprem.compute import Server
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.logging import Loki

with Diagram("EMonitor ESP32 Device Architecture", show=False, direction="TB"):
    esp32 = IotButton("ESP32 Device")
    
    with Cluster("Device Components"):
        sensors = Server("Sensor Readings\n(DHT11, BMP180, LDR)")
        wifi = Server("WiFi Connection")
        display = Client("OLED Display")
        buffer = Redis("Data Buffer")
        xml = Server("XML Formatter")
        email = Server("Email Alert")
    
    with Cluster("External Services"):
        ntp = Server("NTP Server")
        backend = Server("Backend Server")
        smtp = Server("SMTP Server")
    
    esp32 >> sensors
    esp32 >> wifi
    esp32 >> display
    esp32 >> buffer
    esp32 >> xml
    esp32 >> email
    
    wifi >> ntp
    wifi >> backend
    email >> smtp
    
    sensors >> buffer
    buffer >> xml
    xml >> backend