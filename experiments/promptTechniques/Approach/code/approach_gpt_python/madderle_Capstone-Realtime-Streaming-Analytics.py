from diagrams import Diagram, Cluster
from diagrams.aws.analytics import Kinesis
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.onprem.queue import Kafka
from diagrams.onprem.database import Mongodb
from diagrams.onprem.inmemory import Redis
from diagrams.programming.language import Python
from diagrams.onprem.container import Docker

with Diagram("Real-Time Streaming Analytics System for Stock Price Prediction", direction="TB"):

    with Cluster("Data Ingestion"):
        twitter_service = Python("Twitter Service")
        iex_service = Python("IEX Service")
        manager_service = Python("Manager Service")
        
    with Cluster("Data Storage"):
        mongodb = Mongodb("MongoDB")
        redis = Redis("Redis")
        s3_storage = S3("S3 Storage")
    
    with Cluster("Data Analysis"):
        model_dev = Python("Model Development")
        model_deploy = Python("Model Deployment")
        eda = Python("Exploratory Data Analysis")
    
    with Cluster("Data Processing & Management"):
        data_service = Python("Data Service")
    
    with Cluster("Infrastructure & Automation"):
        aws_kinesis = Kinesis("AWS Kinesis")
        schedule_task = Lambda("Scheduled Tasks")
    
    # Connectors
    twitter_service >> aws_kinesis >> iex_service
    manager_service >> redis
    aws_kinesis >> mongodb
    model_dev >> s3_storage
    model_deploy >> s3_storage
    eda >> mongodb
    data_service >> mongodb
    data_service >> redis
    schedule_task >> model_deploy
    schedule_task >> data_service
    schedule_task >> manager_service