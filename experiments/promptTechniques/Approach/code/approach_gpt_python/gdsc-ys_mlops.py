from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.onprem.database import MySQL
from diagrams.onprem.compute import Server
from diagrams.onprem.network import Nginx
from diagrams.onprem.client import User

with Diagram("MLOps Architecture", show=False):
    user = User("ML Developer")

    with Cluster("Containerized Environment"):
        nginx = Nginx("Nginx Reverse Proxy")

        with Cluster("MLflow Tracking Server"):
            mlflow_server = Server("MLflow Server")
            mysql_db = MySQL("MySQL Database")
            s3_storage = S3("AWS S3 Artifact Store")

        nginx >> mlflow_server
        mlflow_server >> mysql_db
        mlflow_server >> s3_storage

    user >> nginx