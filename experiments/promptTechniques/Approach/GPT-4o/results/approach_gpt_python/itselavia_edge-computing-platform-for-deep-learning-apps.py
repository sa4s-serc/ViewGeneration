from diagrams import Diagram, Cluster
from diagrams.gcp.ml import AIPlatform, AIHub
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.compute import Pod, Deployment
from diagrams.azure.compute import ACR, AKS
from diagrams.oci.database import ADB
from diagrams.gcp.storage import GCS
from diagrams.programming.framework import Flask, React
from diagrams.programming.language import Go
from diagrams.programming.flowchart import Action, Decision

with Diagram("Edge Computing Platform for Deep Learning", show=False):
    with Cluster("Cloud Infrastructure"):
        cloud_functions = AIPlatform("Cloud Functions for TFLite Conversion")
        terraform = AIHub("Terraform for IaC")
        gcs = GCS("Google Cloud Storage")
        cloud_sql_db = ADB("Cloud SQL Database")

    with Cluster("Kubernetes Cluster"):
        kube_api = APIServer("Kube API Server")
        with Cluster("Model Management"):
            model_manager = Go("Model Manager")
            model_manager_pod = Pod("Model Manager Pod")

        with Cluster("Microservices"):
            microservices = Deployment("Microservices Deployment")
            pods = [Pod("Service Pod 1"), Pod("Service Pod 2")]

    with Cluster("Edge Node"):
        kube_edge = AKS("KubeEdge Node")
        edge_service = Pod("Edge Service Pod")

    with Cluster("Frontend & Backend"):
        flask_backend = Flask("Flask Backend")
        react_frontend = React("React Frontend")

    cloud_functions >> terraform >> [gcs, cloud_sql_db]
    terraform >> kube_api
    kube_api >> model_manager >> model_manager_pod
    model_manager_pod >> microservices
    microservices >> pods
    kube_api >> kube_edge >> edge_service
    flask_backend >> [gcs, cloud_sql_db]
    react_frontend >> flask_backend
    flask_backend >> Decision("API Endpoints")
    Decision("API Endpoints") >> Action("User Authentication")
    Decision("API Endpoints") >> Action("Project Management")