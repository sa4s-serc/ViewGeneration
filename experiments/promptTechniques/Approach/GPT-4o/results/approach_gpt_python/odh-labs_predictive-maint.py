from diagrams import Diagram
from diagrams.onprem.queue import Kafka
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.k8s.compute import Pod
from diagrams.k8s.network import Ingress
from diagrams.onprem.database import Mongodb
from diagrams.onprem.storage import Ceph
from diagrams.onprem.mlops import Mlflow
from diagrams.k8s.controlplane import APIServer
from diagrams.k8s.compute import Deployment
from diagrams.gcp.ml import AIPlatform
from diagrams.azure.web import AppServicePlans

with Diagram("Predictive Maintenance System", show=False):
    client = Client("Webcam")
    kafka = Kafka("Kafka")
    consumer = Pod("Consumer Application")
    seldon = AIPlatform("Seldon Core")
    minio = Ceph("MinIO")
    mongodb = Mongodb("DB")
    mlflow = Mlflow("MLflow")
    deployment = Deployment("OpenShift Deployment")
    ingress = Ingress("Ingress")
    api_server = APIServer("API Server")
    webapp = AppServicePlans("Data Visualization")

    client >> kafka >> consumer >> seldon >> minio
    consumer >> minio
    seldon >> mongodb
    seldon >> mlflow
    deployment >> ingress >> api_server
    api_server >> webapp