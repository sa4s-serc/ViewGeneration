from diagrams import Diagram, Cluster
from diagrams.onprem.queue import Kafka
from diagrams.onprem.analytics import Flink
from diagrams.onprem.database import Elasticsearch
from diagrams.onprem.compute import Spring
from diagrams.onprem.client import User
from diagrams.onprem.container import Docker
from diagrams.k8s.compute import Pod
from diagrams.programming.framework import Angular

with Diagram("Twitter Data Application Architecture", show=False, direction="TB"):
    with Cluster("Microservices"):
        with Cluster("Tweet Collector"):
            tweet_collector = Docker("Tweet Collector")
            kafka_sink = Kafka("Kafka Sink")
            tweet_collector >> kafka_sink

        with Cluster("Flink Processor"):
            flink_processor = Flink("Flink Processor")
            kafka_queue = Kafka("Kafka Queue")
            flink_processor << kafka_queue
            flink_processor >> Elasticsearch("Elasticsearch Data Store")

        with Cluster("REST API Server"):
            rest_api_server = Spring("Spring Boot")
            rest_api_server >> Elasticsearch("Elasticsearch Data Store")

    user = User("User")
    user >> Angular("Angular Frontend") >> rest_api_server

    with Cluster("Containerization & Orchestration"):
        Docker("Docker")
        Pod("Kubernetes")