from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.aws.integration import SQS
from diagrams.aws.ml import Sagemaker

with Diagram("Architecture View", show=False, direction="TB"):
    with Cluster("Frontend"):
        api_gateway = APIGateway("API Gateway")
    
    with Cluster("Application Layer"):
        lambda_func = Lambda("Lambda Function")
    
    with Cluster("Data Layer"):
        rds = RDS("RDS Database")
        s3 = S3("S3 Storage")
    
    with Cluster("AI/ML Services"):
        sagemaker = Sagemaker("SageMaker")
    
    with Cluster("Messaging"):
        sqs = SQS("SQS Queue")
    
    with Cluster("Monitoring & Security"):
        cloudwatch = Cloudwatch("CloudWatch")
        iam = IAM("IAM")
    
    api_gateway >> lambda_func
    lambda_func >> rds
    lambda_func >> s3
    lambda_func >> sagemaker
    lambda_func >> sqs
    cloudwatch << lambda_func
    iam << lambda_func