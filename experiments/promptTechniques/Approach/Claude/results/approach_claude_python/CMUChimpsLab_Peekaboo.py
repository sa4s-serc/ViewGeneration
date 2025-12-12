from diagrams import Diagram, Cluster
from diagrams.onprem.network import Nginx
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.monitoring import Grafana
from diagrams.generic.device import Mobile
from diagrams.onprem.client import Users

with Diagram("Peekaboo Architecture", show=False, direction="TB"):
    with Cluster("User Interface Layer"):
        users = Users("End Users")
        ui = Nginx("Node-RED UI")
        mobile = Mobile("Mobile Sensors")

    with Cluster("Core Processing Layer"):
        with Cluster("Message Processing"):
            broker = RabbitMQ("Message Queue")
            
        with Cluster("Node Services"):
            provider = Server("Provider Nodes\n(Pull/Push)")
            inference = Server("Inference Nodes\n(Classify/Detect/Extract)")
            filter = Server("Filter Nodes\n(Select/Noisify/Spoof)")
            network = Server("Network Nodes\n(Post)")

    with Cluster("Data Layer"):
        db = PostgreSQL("State Storage")
        monitor = Grafana("Monitoring")

    # Define dataflows
    users >> ui
    mobile >> ui
    ui >> broker
    
    broker >> provider
    broker >> inference
    broker >> filter
    
    provider >> db
    inference >> db
    filter >> network
    
    network >> db
    db >> monitor