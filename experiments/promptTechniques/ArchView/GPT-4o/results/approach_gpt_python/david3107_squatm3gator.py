from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.framework import Flask
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker

with Diagram("SquatM3gator Architecture", show=False, direction="TB"):
    user = User("User")

    with Cluster("Client"):
        browser = Flask("Web UI")
        real_time_communication = Server("Real-time Communication")

    with Cluster("Server"):
        flask_app = Flask("Flask App")
        
        with Cluster("Backend Processing"):
            producer = Server("API Endpoint (Producer)")
            consumer = Server("Domain Generator (Consumer)")

        with Cluster("Message Queue"):
            redis_queue = Redis("Redis Queue")

        with Cluster("Data Storage"):
            redis_cache = Redis("Redis Cache")

    with Cluster("Infrastructure"):
        docker = Docker("Dockerized Deployment")

    user >> browser >> flask_app
    flask_app >> real_time_communication >> user
    flask_app >> producer >> redis_queue
    redis_queue >> consumer
    consumer >> redis_cache
    flask_app << redis_cache
    flask_app >> docker