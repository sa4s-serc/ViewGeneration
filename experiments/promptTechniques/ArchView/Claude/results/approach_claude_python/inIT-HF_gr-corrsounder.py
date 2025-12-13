from diagrams import Diagram
from diagrams.generic.compute import Rack
from diagrams.programming.language import Python
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.monitoring import Grafana
from diagrams.aws.storage import S3
from diagrams.programming.framework import Django

with Diagram("gr-corrsounder Architecture", show=False, direction="TB"):
    app = Python("gr-corrsounder")
    
    # Core Components
    db = PostgreSQL("Database")
    queue = RabbitMQ("Message Queue")
    storage = S3("Data Storage")
    web = Django("Web Interface")
    monitor = Grafana("Monitoring")

    # Processing Components
    rack = Rack("Signal Processing")
    
    # Connect components
    app >> queue
    queue >> rack
    rack >> storage
    rack >> db
    db >> web
    db >> monitor
    storage >> monitor