from diagrams import Diagram
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.programming.framework import Flask
from diagrams.programming.language import Python
from diagrams.aws.storage import S3
from diagrams.onprem.queue import Kafka
from diagrams.onprem.monitoring import Grafana

with Diagram("HARSH Payload Architecture", show=False):
    # Core Components
    fpga = Server("SmartFusion2 FPGA")
    web = Nginx("Web Server")
    api = Flask("API Server")
    db = PostgreSQL("Database")
    storage = S3("Data Storage")
    queue = Kafka("Message Queue")
    monitor = Grafana("Monitoring")
    runtime = Python("FreeRTOS Runtime")

    # Data Flow
    web >> api
    api >> db
    api >> storage
    
    # FPGA Interactions
    fpga >> queue
    queue >> api
    
    # Monitoring Flow
    api >> monitor
    db >> monitor
    
    # Runtime Environment
    runtime - fpga
    runtime >> queue