from diagrams import Diagram, Cluster
from diagrams.programming.language import Python
from diagrams.onprem.queue import Kafka
from diagrams.onprem.analytics import Flink
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.programming.framework import Spring, Angular
from diagrams.onprem.container import Docker
from diagrams.k8s.compute import Pod

with Diagram("Twitter Data Processing Architecture", show=False):
    with Cluster("Data Collection"):
        collector = Python("Tweet Collector")
        kafka = Kafka("Kafka Queue")

    with Cluster("Processing Layer"):
        flink = Flink("Flink Processor")

    with Cluster("Storage Layer"):
        es = Elasticsearch("Elasticsearch")

    with Cluster("API Layer"):
        api = Spring("REST API")

    with Cluster("Frontend"):
        ui = Angular("Web UI")

    with Cluster("Infrastructure"):
        docker = Docker("Container")
        k8s = Pod("Kubernetes Pod")

    # Data flow
    collector >> kafka >> flink >> es
    es >> api >> ui
    
    # Infrastructure connections
    docker - k8s
    [collector, kafka, flink, es, api, ui] - docker