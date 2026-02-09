from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.database import Database
from diagrams.aws.integration import Eventbridge, SQS
from diagrams.aws.network import APIGateway
from diagrams.gcp.analytics import Bigquery
from diagrams.aws.security import Cognito
from diagrams.aws.security import IAM

with Diagram("Coverage Robot Architecture", show=False):
    with Cluster("API Layer"):
        api = APIGateway("API Gateway")
        auth = Cognito("Authentication")
        api_lambda = Lambda("API Service")

    with Cluster("Storage Layer"):
        s3 = S3("Coverage Data")
        dynamo = Database("Config & Metadata")
        bigquery = Bigquery("Data Warehouse")

    with Cluster("Processing Layer"):
        event_bus = Eventbridge("Event Bus")
        
        with Cluster("Services"):
            orchestrator = Lambda("Orchestrator")
            analyzer = Lambda("Analyze Service")
            publisher = Lambda("Publish Service")
            ingest = Lambda("Ingest Service")

        queue = SQS("Message Queue")

    # Flow
    api >> auth
    api >> api_lambda
    api_lambda >> s3
    api_lambda >> dynamo
    
    event_bus >> orchestrator
    orchestrator >> queue
    
    queue >> analyzer
    queue >> publisher
    queue >> ingest
    
    analyzer >> s3
    analyzer >> bigquery
    publisher >> dynamo
    ingest >> s3

    # Data flows
    s3 >> bigquery
    dynamo >> orchestrator