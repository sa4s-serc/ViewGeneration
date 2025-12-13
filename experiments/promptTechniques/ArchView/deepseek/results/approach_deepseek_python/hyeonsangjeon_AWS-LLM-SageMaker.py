from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Kinesis
from diagrams.aws.integration import SQS
from diagrams.aws.ml import Sagemaker

with Diagram("AWS Architecture", show=False):
    api = APIGateway("API Gateway")
    lambda_func = Lambda("Lambda Function")
    rds = RDS("RDS Database")
    s3 = S3("S3 Bucket")
    kinesis = Kinesis("Kinesis Stream")
    sqs = SQS("SQS Queue")
    sagemaker = Sagemaker("SageMaker")

    api >> lambda_func
    lambda_func >> rds
    lambda_func >> s3
    lambda_func >> kinesis
    kinesis >> sqs
    sqs >> sagemaker