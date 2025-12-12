from diagrams import Diagram, Cluster
from diagrams.gcp.analytics import Pubsub, BigQuery
from diagrams.programming.language import Go, Java
from diagrams.gcp.storage import GCS
from diagrams.gcp.compute import GKE
from diagrams.aws.management import Cloudwatch
from diagrams.gcp.devtools import ContainerRegistry

with Diagram("Event Analytics Pipeline Architecture", show=False):
    with Cluster("Frontend (Event Reception)"):
        frontend = Go("Go Frontend")
        metrics = Cloudwatch("Prometheus Metrics")
        frontend - metrics

    with Cluster("Message Queue"):
        queue = Pubsub("Google Pub/Sub")

    with Cluster("Backend (Data Processing)"):
        backend = Java("Java Dataflow")
        storage = GCS("GCS Schema Storage")
        db = BigQuery("BigQuery Tables")

    with Cluster("Deployment"):
        k8s = GKE("Kubernetes")
        registry = ContainerRegistry("Container Registry")
        k8s - registry

    frontend >> queue >> backend
    backend >> db
    storage >> backend