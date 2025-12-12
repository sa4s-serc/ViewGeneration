from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SNS, SQS
from diagrams.aws.devtools import Codepipeline
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import APIGateway
from diagrams.onprem.mlops import Mlflow
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.onprem.queue import Kafka
from diagrams.onprem.container import Docker

with Diagram("LEGO Minifigure MLOps Architecture", show=False):
    
    with Cluster("Data & Training Pipeline"):
        s3 = S3("Image Storage")
        mlflow = Mlflow("MLflow Tracking")
        model = SagemakerModel("Classification Model")
        
        s3 >> mlflow >> model
    
    with Cluster("Model Serving"):
        with Cluster("Batch Prediction"):
            batch = Docker("Batch Service")
            queue = SQS("Job Queue")
            batch_db = Dynamodb("Results Store")
            
            queue >> batch >> batch_db
        
        with Cluster("Stream Prediction"):
            stream = Docker("Stream Service")
            kafka = Kafka("Event Stream")
            api = APIGateway("API Gateway")
            
            api >> stream >> kafka
    
    with Cluster("Monitoring & Operations"):
        prometheus = Prometheus("Metrics")
        grafana = Grafana("Dashboards")
        alerts = SNS("Alerts")
        logs = Cloudwatch("Logs")
        
        prometheus >> grafana >> alerts
        logs >> alerts
    
    with Cluster("CI/CD"):
        pipeline = Codepipeline("Deployment Pipeline")
        pipeline >> [batch, stream]
    
    # Connect components
    model >> batch
    model >> stream
    batch >> prometheus
    stream >> prometheus