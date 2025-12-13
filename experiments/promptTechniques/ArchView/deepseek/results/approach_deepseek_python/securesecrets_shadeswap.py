from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS
from diagrams.aws.ml import Sagemaker

with Diagram("Serverless Architecture", show=False, direction="LR"):
    api = APIGateway("API Gateway")
    lambda_func = Lambda("Lambda Function")
    dynamodb = Dynamodb("DynamoDB")
    s3 = S3("S3 Bucket")
    sqs = SQS("SQS Queue")
    sagemaker = Sagemaker("SageMaker")

    api >> lambda_func
    lambda_func >> dynamodb
    lambda_func >> s3
    lambda_func >> sqs
    sqs >> sagemaker