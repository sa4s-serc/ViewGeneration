from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.database import RDS
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.client import User
from diagrams.programming.framework import FastAPI
from diagrams.aws.storage import S3
from diagrams.aws.integration import Eventbridge
from diagrams.aws.management import Cloudwatch

with Diagram("Spotify Tracker Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Frontend"):
        streamlit_app = FastAPI("Streamlit UI")
    
    with Cluster("API Layer"):
        api_gateway = APIGateway("API Gateway")
        with Cluster("FastAPI Microservice"):
            fastapi = FastAPI("FastAPI App")
            lambda_func = Lambda("AWS Lambda")
    
    with Cluster("Data Processing"):
        with Cluster("ETL Pipeline"):
            airflow = Airflow("Apache Airflow")
            event_bridge = Eventbridge("EventBridge")
    
    with Cluster("Data Storage"):
        rds = RDS("PostgreSQL")
        s3 = S3("Data Lake")
    
    with Cluster("Monitoring"):
        cloudwatch = Cloudwatch("CloudWatch")
    
    user >> streamlit_app
    streamlit_app >> api_gateway
    api_gateway >> lambda_func
    lambda_func >> fastapi
    fastapi >> rds
    airflow >> rds
    airflow >> s3
    event_bridge >> airflow
    fastapi >> cloudwatch
    airflow >> cloudwatch
    lambda_func >> cloudwatch