from diagrams import Diagram, Cluster
from diagrams.programming.framework import Flask
from diagrams.onprem.database import MongoDB
from diagrams.onprem.inmemory import Redis
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.programming.language import Python
from diagrams.aws.compute import Lambda
from diagrams.gcp.analytics import Bigquery
from diagrams.onprem.queue import Kafka

with Diagram("Open Risk API Architecture", show=False):
    with Cluster("API Layer"):
        api = APIGateway("Open Risk API")
        model_server = Flask("Model Server")
        data_server = Flask("Data Server")

    with Cluster("Storage Layer"):
        mongodb = MongoDB("Portfolio Data")
        redis = Redis("Cache")
        s3 = S3("Model Storage")

    with Cluster("Processing Layer"):
        risk_engine = Python("Risk Engine")
        analytics = Lambda("Analytics Functions")
        metrics = Bigquery("Concentration Metrics")

    with Cluster("Message Layer"):
        queue = Kafka("Event Queue")

    # Define relationships
    api >> model_server
    api >> data_server
    
    model_server >> risk_engine
    model_server >> s3
    
    data_server >> mongodb
    data_server >> redis
    
    risk_engine >> metrics
    risk_engine >> analytics
    
    [model_server, data_server] >> queue
    queue >> analytics