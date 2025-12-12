from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.network import APIGateway
from diagrams.aws.integration import SQS
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.workflow import Airflow
from diagrams.aws.storage import S3
from diagrams.programming.framework import FastAPI

with Diagram("Spotify Tracker Architecture", show=False):
    api = APIGateway("API Gateway")
    lambda_fn = Lambda("FastAPI App")
    db = RDS("PostgreSQL")
    queue = SQS("Message Queue")
    monitoring = Cloudwatch("Monitoring")
    etl = Airflow("ETL Pipeline") 
    storage = S3("Data Storage")
    ui = FastAPI("UI Dashboard")

    # API Flow
    api >> lambda_fn >> db
    
    # ETL Flow  
    etl >> queue >> lambda_fn
    etl >> storage
    
    # Monitoring
    lambda_fn >> monitoring
    etl >> monitoring
    
    # UI Access
    ui >> api
    ui >> storage