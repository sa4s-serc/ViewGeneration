from diagrams import Diagram, Cluster
from diagrams.gcp.analytics import PubSub, Dataflow
from diagrams.gcp.storage import GCS
from diagrams.gcp.devtools import SourceRepositories
from diagrams.gcp.compute import GKE
from diagrams.onprem.client import Client
from diagrams.programming.language import Go, Java

with Diagram("doitintl_banias Architecture", show=False, direction="LR"):
    client = Client("Web/Mobile App")
    
    with Cluster("Frontend (Go)"):
        event_reception = Go("Event Reception")
        event_publishing = PubSub("Event Publishing")
        
        client >> event_reception >> event_publishing
    
    with Cluster("Backend (Java Dataflow)"):
        data_processing = Dataflow("Data Processing")
        schema_management = GCS("Schema Management")
        
        event_publishing >> data_processing
        schema_management >> data_processing
        
    with Cluster("Deployment and Monitoring"):
        deployment = GKE("Kubernetes")
        monitoring = SourceRepositories("Prometheus Metrics")
        
        event_reception >> deployment
        monitoring << event_reception