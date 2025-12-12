from diagrams import Cluster, Diagram, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service
from diagrams.k8s.group import Namespace
from diagrams.onprem.client import User
from diagrams.k8s.network import Ingress
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.queue import Rabbitmq
from diagrams.gcp.database import Memorystore
from diagrams.programming.framework import Nextjs, Flask
from diagrams.onprem.container import Docker
from diagrams.onprem.certificates import CertManager

with Diagram("Roof Detection and Geospatial Application Architecture", show=False):
    user = User("User")

    with Cluster("Kubernetes Cluster"):
        ingress = Ingress("Nginx Ingress Controller")

        with Cluster("Microservices Architecture"):
            with Cluster("Frontend Service"):
                frontend = Nextjs("Next.js App")

            with Cluster("Backend Service"):
                backend = Flask("Flask API")

            with Cluster("Metrics Service"):
                metrics_api = Docker("Metrics API")

            with Cluster("Database"):
                database = Memorystore("MongoDB")

            with Cluster("Message Queue"):
                rabbitmq = Rabbitmq("RabbitMQ")

        cert_manager = CertManager("Cert-Manager")

    # Service to Ingress communication
    user >> Edge(label="HTTP/HTTPS") >> ingress

    # Ingress to Frontend
    ingress >> Edge(label="HTTP") >> frontend

    # Frontend to Backend communication
    frontend >> Edge(label="REST API") >> backend

    # Backend to Database communication
    backend >> Edge(label="Query") >> database

    # Backend to RabbitMQ communication
    backend >> Edge(label="Event") >> rabbitmq

    # Metrics API consuming events
    rabbitmq >> Edge(label="Consume") >> metrics_api

    # Metrics API to Database communication
    metrics_api >> Edge(label="Aggregation/Persist") >> database

    # Metrics API to Grafana communication
    metrics_api >> Edge(label="Metrics") >> Grafana("Grafana")

    # Cert-Manager managing certificates
    ingress << Edge(label="TLS Management") << cert_manager