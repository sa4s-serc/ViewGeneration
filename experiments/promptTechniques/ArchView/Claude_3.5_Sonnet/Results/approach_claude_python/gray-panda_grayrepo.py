from diagrams import Diagram, Cluster
from diagrams.aws.security import Shield, IAM, Macie
from diagrams.aws.compute import Lambda
from diagrams.aws.network import VPC
from diagrams.aws.storage import S3
from diagrams.aws.database import DynamodbTable
from diagrams.aws.integration import SQS
from diagrams.aws.network import APIGateway
from diagrams.aws.devtools import Codebuild, Codepipeline
from diagrams.aws.management import Cloudwatch

with Diagram("Flare-On CTF Challenge Architecture", show=False, direction="TB"):
    
    with Cluster("Security Layer"):
        shield = Shield("DDoS Protection")
        iam = IAM("Access Control")
        monitor = Cloudwatch("Threat Detection")
        macie = Macie("Data Security")

    with Cluster("Network Layer"):
        vpc = VPC("Isolated Network")
        api = APIGateway("API Gateway")

    with Cluster("Compute & Storage"):
        lambda_fn = Lambda("Analysis Engine")
        s3 = S3("Challenge Files")
        dynamo = DynamodbTable("User Progress")
        queue = SQS("Task Queue")

    with Cluster("CI/CD Pipeline"):
        build = Codebuild("Build")
        pipeline = Codepipeline("Deploy")

    # Network flow
    api >> shield >> vpc
    vpc >> iam >> lambda_fn
    
    # Data flow
    s3 >> macie
    lambda_fn >> dynamo
    lambda_fn >> queue
    
    # Security monitoring
    vpc >> monitor
    
    # Deployment
    build >> pipeline >> lambda_fn
    pipeline >> s3
    pipeline >> dynamo