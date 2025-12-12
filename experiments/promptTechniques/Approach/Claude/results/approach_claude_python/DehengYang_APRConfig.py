from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import DynamodbTable
from diagrams.aws.network import APIGateway
from diagrams.aws.security import Cognito
from diagrams.aws.integration import SNS

with Diagram("Architecture View", show=False):
    with Cluster("AWS Cloud"):
        api = APIGateway("API Gateway")
        auth = Cognito("Authentication")
        
        with Cluster("Processing Layer"):
            lambda_fn = Lambda("Business Logic")
        
        with Cluster("Data Layer"):
            db = DynamodbTable("Data Store")
            events = SNS("Event Bus")
        
        # Define relationships
        api >> auth
        api >> lambda_fn
        lambda_fn >> db
        lambda_fn >> events