from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import Eventbridge, SQS
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.security import Cognito
from diagrams.gcp.analytics import BigQuery
from diagrams.onprem.vcs import Github
from diagrams.onprem.client import User

with Diagram("Coverage Robot System Architecture", show=False, direction="LR"):
    user = User("Developer")
    github = Github("GitHub")
    
    api = Lambda("API Service")
    orchestrator = Lambda("Orchestrator Service")
    analyse = Lambda("Analyse Service")
    publish = Lambda("Publish Service")
    ingest = Lambda("Ingest Service")
    
    event_bridge = Eventbridge("EventBridge")
    
    s3 = S3("S3")
    dynamodb = Dynamodb("DynamoDB")
    bigquery = BigQuery("BigQuery")
    cognito = Cognito("Cognito")
    
    user >> cognito
    user >> api
    github >> api
    
    api >> cognito
    api >> s3
    api >> dynamodb
    api >> SQS("Webhook Queue") >> orchestrator
    
    orchestrator >> event_bridge
    event_bridge >> analyse
    event_bridge >> publish
    event_bridge >> ingest
    
    analyse >> dynamodb
    analyse >> bigquery
    analyse >> s3
    
    publish >> github
    ingest >> s3
    ingest >> dynamodb