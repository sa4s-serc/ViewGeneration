from diagrams import Diagram, Cluster, Edge
from diagrams.onprem.network import Nginx
from diagrams.onprem.compute import Server
from diagrams.onprem.container import Docker
from diagrams.onprem.database import PostgreSQL, MongoDB
from diagrams.aws.storage import S3
from diagrams.aws.ml import Sagemaker
from diagrams.gcp.ml import AIHub
from diagrams.onprem.analytics import Spark
from diagrams.onprem.queue import Kafka

with Diagram("Karura ML Platform Architecture", show=False):
    with Cluster("Client Layer"):
        kintone = Nginx("Kintone Plugin")
        master = Server("Karura Master App")

    with Cluster("Application Layer"):
        server = Docker("Karura Server")

    with Cluster("Model Building Pipeline"):
        datastream = Kafka("Data Stream")
        feature_eng = Spark("Feature Engineering")
        model_select = AIHub("Model Selection")
        model_train = Sagemaker("Model Training")

    with Cluster("Storage Layer"):
        metadata = PostgreSQL("Metadata DB")
        modelstore = MongoDB("Model Store")
        artifacts = S3("Model Artifacts")

    # Client to Server connections
    kintone >> server
    master >> server

    # Server to Pipeline connections
    server >> datastream
    datastream >> feature_eng
    feature_eng >> model_select
    model_select >> model_train

    # Pipeline to Storage connections
    model_train >> modelstore
    model_train >> artifacts
    server >> metadata

    # Additional connections
    feature_eng >> metadata
    model_select >> metadata