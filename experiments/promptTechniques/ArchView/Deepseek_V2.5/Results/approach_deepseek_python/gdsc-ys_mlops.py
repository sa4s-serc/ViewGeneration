from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.onprem.client import Client
from diagrams.onprem.network import Nginx

with Diagram("MLOps Architecture", show=False, direction="LR"):
    client = Client("ML Developer")
    
    with Diagram("MLflow Server Infrastructure"):
        nginx = Nginx("Nginx Reverse Proxy")
        mlflow_server = EC2("MLflow Tracking Server")
        mysql = RDS("MySQL Database")
        s3 = S3("AWS S3 Artifact Store")
        
        nginx >> mlflow_server
        mlflow_server >> mysql
        mlflow_server >> s3
    
    client >> nginx