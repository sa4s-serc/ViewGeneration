from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.database import Database
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.aws.integration import SNS, SQS, EventBridge
from diagrams.aws.network import VPC

with Diagram("Piattaforma Notifiche Infrastructure", show=False):
    with Cluster("AWS Cloud"):
        # Core Components
        api = APIGateway("API Gateway")
        lambda_fn = Lambda("Lambda Functions")
        eventbridge = EventBridge("EventBridge")
        s3 = S3("Storage")
        dynamodb = Database("DynamoDB")
        
        # Monitoring & Security
        cloudwatch = Cloudwatch("CloudWatch")
        iam = IAM("IAM/Security")
        
        # Message Components
        sns = SNS("SNS Topics")
        sqs = SQS("SQS Queues")
        
        # VPC Components
        with Cluster("VPC"):
            vpc = VPC("Virtual Private Cloud")
        
        # Flow
        api >> lambda_fn
        lambda_fn >> dynamodb
        lambda_fn >> s3
        lambda_fn >> eventbridge
        eventbridge >> sns
        sns >> sqs
        
        # Monitoring & Security Flow
        lambda_fn >> cloudwatch
        api >> cloudwatch
        iam - api
        iam - lambda_fn
        iam - s3
        iam - dynamodb