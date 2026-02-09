from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod, Deployment
from diagrams.k8s.network import Service, Ingress
from diagrams.onprem.queue import RabbitMQ
from diagrams.onprem.database import MongoDB
from diagrams.programming.framework import Flask, React
from diagrams.programming.framework import Node

with Diagram("Roof Detection Architecture", show=False):
    with Cluster("Kubernetes Cluster"):
        # Frontend
        with Cluster("Frontend"):
            frontend = React("Next.js Frontend")

        # Backend Services 
        with Cluster("Backend Services"):
            ingress = Ingress("Nginx Ingress")
            api = Flask("Flask API")
            metrics_api = Node("Metrics API")

        # Message Queue
        with Cluster("Message Queue"):
            rabbitmq = RabbitMQ("RabbitMQ")

        # Database
        with Cluster("Database"):
            mongodb = MongoDB("MongoDB")

        # Connect components
        frontend >> ingress
        ingress >> api
        ingress >> metrics_api
        api >> rabbitmq
        metrics_api >> rabbitmq
        api >> mongodb 
        metrics_api >> mongodb
        rabbitmq >> metrics_api