from diagrams import Diagram, Cluster, Edge
from diagrams.k8s.compute import Pod
from diagrams.k8s.podconfig import ConfigMap
from diagrams.gcp.compute import GCE
from diagrams.gcp.database import SQL
from diagrams.gcp.storage import GCS
from diagrams.programming.framework import Flask
from diagrams.programming.language import Go
from diagrams.onprem.client import User

with Diagram("Edge Computing Platform for Deep Learning", show=False, direction="TB"):
    with Cluster("Cloud Infrastructure (GCP)"):
        gcp_infra = [GCE("VMs"), GCS("Storage Buckets"), SQL("Cloud SQL")]

    with Cluster("Kubernetes Cluster"):
        kube_cluster = [Pod("Microservice Pods"), ConfigMap("K8s Configs")]

    with Cluster("KubeEdge Cluster"):
        kubeedge_cluster = [Pod("Edge Pods"), ConfigMap("Edge Configs")]

    with Cluster("Backend Services"):
        flask_backend = Flask("Flask Backend")
        model_manager = Go("Model Manager")

    with Cluster("Frontend Application"):
        react_ui = User("React UI")

    with Cluster("Model Management"):
        model_conversion = Pod("Model Conversion (TFLite)")
        inference_services = Pod("Inference Services")

    flask_backend >> Edge(label="API Calls") >> model_manager
    flask_backend >> Edge(label="REST API") >> react_ui
    model_manager >> Edge(label="Deploy Models") >> kube_cluster
    kube_cluster >> Edge(label="Extend to Edge") >> kubeedge_cluster
    model_conversion >> Edge(label="Convert Models") >> inference_services

    gcp_infra >> Edge(label="Provision Via Terraform") >> [kube_cluster, flask_backend]
    gcp_infra >> Edge(label="Store Models") >> inference_services
    react_ui >> Edge(label="User Interactions") >> flask_backend