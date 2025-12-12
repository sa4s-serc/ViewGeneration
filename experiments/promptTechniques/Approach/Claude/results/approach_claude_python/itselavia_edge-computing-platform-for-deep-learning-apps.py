from diagrams import Diagram, Cluster
from diagrams.gcp.compute import GKE, Run 
from diagrams.gcp.storage import Storage
from diagrams.azure.database import SQLDatabases
from diagrams.programming.framework import Flask, React
from diagrams.oci.devops import APIService
from diagrams.aws.ml import SagemakerModel
from diagrams.firebase.develop import Authentication
from diagrams.azure.security import KeyVaults

with Diagram("Edge Computing Platform Architecture", show=False):
    with Cluster("Cloud Infrastructure"):
        storage = Storage("Google Cloud Storage")
        db = SQLDatabases("Cloud SQL (MySQL)")
        gke = GKE("Kubernetes/KubeEdge")
        secrets = KeyVaults("Secrets Management")
    
    with Cluster("Model Management"):
        api = APIService("API Gateway")
        backend = Flask("Backend Service")
        model_mgmt = SagemakerModel("Model Manager")
        firebase = Authentication("Authentication")
    
    with Cluster("Frontend"):
        ui = React("Web UI")
        cloud_run = Run("Cloud Run")
    
    # Define relationships
    ui >> api >> backend
    backend >> firebase
    backend >> db
    backend >> storage
    model_mgmt >> gke
    model_mgmt >> storage
    backend >> model_mgmt
    backend >> secrets
    cloud_run >> ui