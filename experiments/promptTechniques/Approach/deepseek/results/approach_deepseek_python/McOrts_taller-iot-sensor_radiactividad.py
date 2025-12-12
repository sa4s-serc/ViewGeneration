from diagrams import Diagram
from diagrams.aws.iot import IotSensor, IotCore
from diagrams.aws.integration import MQ
from diagrams.aws.analytics import KinesisDataStreams
from diagrams.aws.ml import Sagemaker
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.network import CloudFront
from diagrams.aws.compute import Lambda
from diagrams.aws.engagement import Pinpoint
from diagrams.aws.security import IAM

with Diagram("IoT Sensor Data Processing Architecture", show=False, direction="LR"):
    sensor = IotSensor("Sensor Device")
    iot_core = IotCore("IoT Core")
    mqtt = MQ("MQTT Broker")
    kinesis = KinesisDataStreams("Kinesis Data Streams")
    lambda_func = Lambda("Lambda Function")
    sagemaker = Sagemaker("SageMaker")
    dynamodb = Dynamodb("DynamoDB")
    s3 = S3("S3 Bucket")
    cloudfront = CloudFront("CloudFront")
    pinpoint = Pinpoint("Pinpoint")
    iam = IAM("IAM")

    sensor >> iot_core >> mqtt >> kinesis >> lambda_func
    lambda_func >> sagemaker
    lambda_func >> dynamodb
    lambda_func >> s3
    s3 >> cloudfront
    lambda_func >> pinpoint
    iam - [sensor, iot_core, mqtt, kinesis, lambda_func, sagemaker, dynamodb, s3, cloudfront, pinpoint]