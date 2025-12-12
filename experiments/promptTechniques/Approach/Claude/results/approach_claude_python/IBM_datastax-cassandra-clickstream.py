from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda 
from diagrams.aws.database import DocumentDB
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.programming.framework import Nextjs, React
from diagrams.onprem.database import Cassandra
from diagrams.aws.management import CloudwatchEventEventBased

with Diagram("Clickstream Data Capture Architecture", show=False, direction="TB"):
    
    with Cluster("Frontend Layer"):
        frontend = [
            Nextjs("Next.js"),
            React("React UI")
        ]
        
    with Cluster("API Layer"):
        api = APIGateway("API Gateway")
        events = CloudwatchEventEventBased("Event Handler")
        
    with Cluster("Backend Layer"):
        lambda_fn = Lambda("Lambda Functions")
        db = Cassandra("DataStax/Cassandra")
        storage = S3("Clickstream Data")

    # Frontend to API connections
    frontend[0] >> api
    frontend[1] >> api
    
    # API to Backend connections  
    api >> events
    events >> lambda_fn
    
    # Backend data flow
    lambda_fn >> db
    lambda_fn >> storage
    db >> storage