from diagrams import Diagram
from diagrams.aws.iot import IotSensor, IotCore
from diagrams.aws.analytics import KinesisDataStreams
from diagrams.aws.database import Dynamodb
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.network import CloudFront
from diagrams.aws.mobile import APIGateway
from diagrams.onprem.client import User

with Diagram("IoT Data Processing Architecture", show=False, direction="LR"):
    sensors = IotSensor("Sensors")
    iot_core = IotCore("IoT Core")
    kinesis = KinesisDataStreams("Kinesis Data Streams")
    lambda_func = Lambda("Lambda Function")
    dynamodb = Dynamodb("DynamoDB")
    s3 = S3("S3 Bucket")
    cloudfront = CloudFront("CloudFront")
    api_gateway = APIGateway("API Gateway")
    user = User("End User")

    sensors >> iot_core >> kinesis >> lambda_func
    lambda_func >> dynamodb
    lambda_func >> s3
    api_gateway >> lambda_func
    cloudfront >> api_gateway
    user >> cloudfront