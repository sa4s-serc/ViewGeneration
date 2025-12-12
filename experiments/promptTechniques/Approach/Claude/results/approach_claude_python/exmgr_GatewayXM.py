from diagrams import Diagram, Cluster, Edge
from diagrams.aws.iot import IotGreengrass
from diagrams.aws.integration import SNS
from diagrams.aws.storage import S3
from diagrams.aws.database import Timestream
from diagrams.aws.integration import SQS
from diagrams.custom import Custom
from diagrams.onprem.queue import Kafka
from diagrams.aws.compute import Lambda

with Diagram("IoT Gateway Architecture", show=False, direction="TB"):
    
    with Cluster("Edge Layer"):
        gateway = IotGreengrass("GatewayXM")
        modbus = Custom("ModBus Devices", "./modbus.png")
        sensors = Custom("ESP8266/ESP32\nSensor Nodes", "./sensor.png")
        
    with Cluster("Integration Layer"):
        mqtt = Kafka("Artemis MQTT")
        queue = SQS("Message Queue")

    with Cluster("Processing Layer"):
        processor = Lambda("Data Processor")
        
    with Cluster("Storage Layer"):
        storage = S3("Object Storage")
        timeseries = Timestream("Time Series DB")
        
    with Cluster("Notification Layer"):
        notifier = SNS("Notifications")

    # Edge connections
    modbus >> gateway
    sensors >> gateway
    
    # Integration flow
    gateway >> mqtt
    mqtt >> queue
    
    # Processing and storage
    queue >> processor
    processor >> storage
    processor >> timeseries
    
    # Notifications
    processor >> notifier