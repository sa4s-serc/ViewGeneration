from diagrams import Diagram, Cluster
from diagrams.programming.framework import Flask
from diagrams.onprem.client import Client
from diagrams.onprem.network import Internet
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.monitoring import Grafana

with Diagram("Zswag Architecture", show=False):
    client = Client("Python/C++ Client")
    internet = Internet("HTTP/REST")
    with Cluster("Zserio Services"):
        zserio_data = Server("Zserio Data Layer")
        zserio_services = [Server(f"Zserio Service {i}") for i in range(1, 4)]
    
    with Cluster("Python Server (OAServer)"):
        flask_server = Flask("Flask/Connexion")
        redis = Redis("Cache")
        queue = RabbitMQ("Queue")
        db = PostgreSQL("Database")
        prometheus = Prometheus("Monitoring")
        grafana = Grafana("Dashboard")

    client >> internet >> flask_server >> zserio_data
    zserio_data >> zserio_services
    flask_server >> redis
    flask_server >> queue
    flask_server >> db
    flask_server >> prometheus
    prometheus >> grafana