from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS
from diagrams.aws.analytics import KinesisDataStreams

with Diagram("Sakura MK I Credit Card BIN Data Service", show=False, direction="LR"):
    s3 = S3("S3 (CSV Storage)")
    kinesis = KinesisDataStreams("Kinesis/SQS")
    lambda_ingest = Lambda("Ingest Lambda")
    lambda_process = Lambda("Process Lambda")
    dynamodb = Dynamodb("DynamoDB")
    api_gateway = APIGateway("API Gateway")

    s3 >> kinesis >> lambda_ingest >> lambda_process >> dynamodb
    api_gateway >> dynamodb