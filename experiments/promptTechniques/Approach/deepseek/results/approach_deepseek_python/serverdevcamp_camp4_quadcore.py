from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.network import ELB, CloudFront
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS
from diagrams.aws.analytics import Kinesis
from diagrams.onprem.database import Cassandra
from diagrams.onprem.queue import Kafka
from diagrams.onprem.analytics import Spark
from diagrams.programming.framework import React
from diagrams.onprem.inmemory import Redis

with Diagram("TweetDeck Clone Architecture", show=False, direction="TB"):
    frontend = React("React Frontend")
    
    with Cluster("API Gateway Layer"):
        api_gateway = ELB("APIGateway")
        auth_front = EC2("AuthFront")
    
    with Cluster("Authentication Service"):
        auth_server = EC2("AuthServer")
        redis = Redis("Redis")
    
    with Cluster("Data Pipeline"):
        kafka = Kafka("Kafka")
        data_pipeline = EC2("DataPipeline")
    
    with Cluster("Data Processing"):
        spark = Spark("Spark")
        data_processing = EC2("DataProcessing")
    
    with Cluster("Data Storage"):
        cassandra = Cassandra("Cassandra")
        data_sending = EC2("DataSending")
    
    with Cluster("User Activity"):
        user_activity = EC2("UserActivity")
        rds = RDS("UserDB")
    
    twitter_api = CloudFront("Twitter API")
    
    frontend >> api_gateway
    api_gateway >> auth_front
    auth_front >> auth_server
    auth_server >> redis
    api_gateway >> user_activity
    user_activity >> rds
    api_gateway >> data_sending
    data_sending >> cassandra
    twitter_api >> kafka
    kafka >> data_pipeline
    data_pipeline >> spark
    spark >> data_processing
    data_processing >> cassandra
    data_sending >> frontend