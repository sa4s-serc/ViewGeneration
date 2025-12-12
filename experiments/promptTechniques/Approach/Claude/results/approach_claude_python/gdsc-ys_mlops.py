from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.aws.database import RDSMysqlInstance
from diagrams.onprem.mlops import Mlflow
from diagrams.onprem.network import Nginx
from diagrams.aws.storage import SimpleStorageServiceS3
from diagrams.onprem.container import Docker
from diagrams.custom import Custom

with Diagram("MLOps Architecture", show=False):
    with Cluster("MLflow Infrastructure"):
        mlflow = Mlflow("MLflow Server")
        nginx = Nginx("Nginx Proxy")
        mysql = RDSMysqlInstance("MySQL DB")
        s3 = SimpleStorageServiceS3("S3 Artifact Store")
        
        with Cluster("Docker Environment"):
            docker = Docker("Docker Container")
            
    nginx >> mlflow
    mlflow >> mysql
    mlflow >> s3
    docker >> mlflow