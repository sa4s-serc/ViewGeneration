from diagrams import Diagram, Cluster
from diagrams.gcp.analytics import BigQuery, Dataflow, PubSub
from diagrams.gcp.storage import GCS
from diagrams.gcp.compute import GKE
from diagrams.onprem.client import User
from diagrams.onprem.monitoring import Prometheus
from diagrams.programming.language import Go, Java

with Diagram("Event Analytics Pipeline Architecture", show=False, direction="LR"):
    users = User("Web/Mobile Users")
    
    with Cluster("Frontend (Go)"):
        frontend = GKE("Kubernetes Cluster")
        collector = Go("Event Collector\n(/track endpoint)")
        publisher = Go("Async Publisher")
        prometheus = Prometheus("Metrics\n(/metrics endpoint)")
        
        users >> collector
        collector >> publisher
        collector >> prometheus
    
    pubsub = PubSub("Google Pub/Sub")
    
    with Cluster("Backend (Java)"):
        dataflow = Dataflow("Dataflow Pipeline")
        bigquery = BigQuery("BigQuery Tables")
        gcs = GCS("GCS Schema Bucket")
        error_table = BigQuery("Error Table")
        
        publisher >> pubsub
        pubsub >> dataflow
        gcs >> dataflow
        dataflow >> bigquery
        dataflow >> error_table