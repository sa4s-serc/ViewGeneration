from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS, Aurora
from diagrams.aws.storage import S3
from diagrams.aws.network import CloudFront, Route53
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.analytics import Kinesis
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.client import User
from diagrams.programming.language import Python, R
from diagrams.programming.framework import Flask, React
from diagrams.onprem.network import Nginx

with Diagram("Microservices Architecture", show=False, direction="LR"):
    user = User("End User")
    
    with Cluster("Frontend Layer"):
        cdn = CloudFront("CDN")
        web_app = React("React App")
        nginx = Nginx("Load Balancer")
        
    with Cluster("API Layer"):
        api_gateway = Flask("API Gateway")
        
        with Cluster("Microservices"):
            data_service = Python("Data Service")
            auth_service = Python("Auth Service")
            analytics_service = Python("Analytics Service")
    
    with Cluster("Data Layer"):
        with Cluster("Primary Storage"):
            postgres = PostgreSQL("PostgreSQL")
            aurora = Aurora("Aurora DB")
        
        with Cluster("Cache & Queue"):
            redis = RDS("Redis Cache")
            sqs = SQS("Message Queue")
            sns = SNS("Notifications")
        
        with Cluster("Data Lake"):
            s3 = S3("Data Lake")
            kinesis = Kinesis("Data Streams")
    
    with Cluster("Orchestration"):
        airflow = Airflow("Airflow DAGs")
        lambda_func = Lambda("ETL Functions")
    
    with Cluster("External Services"):
        reddit = Python("Reddit API")
        aws_services = EC2("AWS Services")
    
    # Connections
    user >> cdn >> web_app >> nginx >> api_gateway
    api_gateway >> [data_service, auth_service, analytics_service]
    
    data_service >> [postgres, aurora, redis]
    auth_service >> postgres
    analytics_service >> [s3, kinesis]
    
    sqs >> lambda_func
    sns >> user
    kinesis >> s3
    
    airflow >> [lambda_func, data_service]
    lambda_func >> [postgres, s3]
    
    reddit >> data_service
    aws_services >> [api_gateway, data_service]