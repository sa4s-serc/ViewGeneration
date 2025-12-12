from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.gcp.compute import KubernetesEngine, Functions
from diagrams.gcp.storage import Storage
from diagrams.gcp.database import SQL
from diagrams.gcp.network import LoadBalancing
from diagrams.onprem.container import Docker
from diagrams.programming.framework import React, Flask
from diagrams.programming.language import Go
from diagrams.onprem.iac import Terraform
from diagrams.aws.ml import TensorflowOnAWS
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.storage import SimpleStorageServiceS3

with Diagram("Edge Computing Platform for Deep Learning", show=False, direction="TB"):
    user = User("End User")

    with Cluster("Frontend"):
        react_ui = React("React UI")

    with Cluster("Backend Services"):
        with Cluster("Model Management"):
            flask_backend = Flask("Flask Backend")
            model_manager = Go("Go Model Manager")
            mysql_db = SQL("MySQL Database")

        with Cluster("Infrastructure"):
            terraform = Terraform("Terraform IaC")
            gcs = Storage("Google Cloud Storage")

    with Cluster("Cloud Infrastructure (GCP)"):
        with Cluster("Kubernetes Cluster"):
            k8s_engine = KubernetesEngine("Kubernetes Engine")
            with Cluster("Model Services"):
                tflite_service = Docker("TFLite Service")
                tensorrt_service = Docker("TensorRT Service")

        cloud_functions = Functions("Cloud Functions")
        cloud_sql = SQL("Cloud SQL")

    with Cluster("Edge Infrastructure"):
        with Cluster("KubeEdge Cluster"):
            kubeedge = KubernetesEngine("KubeEdge")
            edge_service = Docker("Edge Service")

    user >> react_ui
    react_ui >> flask_backend
    flask_backend >> mysql_db
    flask_backend >> model_manager
    model_manager >> k8s_engine
    model_manager >> kubeedge
    flask_backend >> gcs
    terraform >> k8s_engine
    terraform >> kubeedge
    terraform >> cloud_functions
    terraform >> cloud_sql
    cloud_functions >> gcs
    k8s_engine >> tflite_service
    k8s_engine >> tensorrt_service
    kubeedge >> edge_service
    tflite_service >> gcs
    tensorrt_service >> gcs
    edge_service >> gcs