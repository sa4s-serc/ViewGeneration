from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.mobile import APIGateway
from diagrams.aws.database import DynamodbTable
from diagrams.aws.integration import SNS
from diagrams.aws.integration import SQS

with Diagram("Serverless Chatbot Architecture", show=False):
    with Cluster("Cloud Services"):
        # Core Components
        api = APIGateway("API Gateway")
        function = Lambda("Cloud Functions")
        watson = Lambda("Watson Assistant")
        db = DynamodbTable("MongoDB")
        
        # Event Bus Components
        event_queue = SQS("Message Queue")
        notification = SNS("Notifications")
        
        # Define the flow
        api >> function
        function >> watson
        watson >> function
        function >> db
        function >> event_queue
        event_queue >> notification