from diagrams import Diagram
from diagrams.onprem.queue import Kafka
from diagrams.onprem.analytics import Flink
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.programming.framework import Spring
from diagrams.programming.framework import Angular
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Service
from diagrams.k8s.network import Ingress
from diagrams.azure.compute import ContainerInstances

with Diagram("Microservices Twitter Data Application", show=False):
    kafka = Kafka("Kafka Cluster")
    
    tweet_collector = Pod("Tweet Collector")
    kafka << tweet_collector

    flink_processor = Flink("Flink Processor")
    kafka >> flink_processor

    elasticsearch = Elasticsearch("Elasticsearch")
    flink_processor >> elasticsearch

    spring_boot = Spring("REST API Server")
    elasticsearch >> spring_boot

    angular_frontend = Angular("Frontend Visualization")
    spring_boot >> angular_frontend

    kubernetes = ContainerInstances("Kubernetes")
    kubernetes - tweet_collector
    kubernetes - flink_processor
    kubernetes - spring_boot