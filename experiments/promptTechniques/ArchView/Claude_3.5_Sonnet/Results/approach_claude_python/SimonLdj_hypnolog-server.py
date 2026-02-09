from diagrams import Diagram, Cluster
from diagrams.onprem.client import Client 
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.programming.language import Nodejs
from diagrams.onprem.database import MongoDB
from diagrams.programming.framework import React
from diagrams.onprem.queue import Rabbitmq
from diagrams.onprem.monitoring import Grafana

with Diagram("HypnoLog Architecture", show=False, direction="TB"):
    
    with Cluster("Client Applications"):
        clients = [Client("App 1"), Client("App 2"), Client("App 3")]

    with Cluster("Frontend"):
        web_ui = React("Web UI")

    with Cluster("Load Balancer"):
        nginx = Nginx("Nginx")

    with Cluster("Backend Services"):
        server = Nodejs("Express Server")
        queue = Rabbitmq("Socket.IO")
        monitoring = Grafana("Monitoring")

    with Cluster("Data Storage"):
        db = MongoDB("MongoDB")

    # Connect components
    for client in clients:
        client >> nginx
    
    nginx >> web_ui
    nginx >> server
    server >> queue
    queue >> web_ui 
    server >> db
    server >> monitoring