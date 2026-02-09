from diagrams import Diagram
from diagrams.aws.iot import IotSensor, IotCore
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import CloudFront
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Kinesis
from diagrams.aws.ml import Sagemaker
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudwatch

with Diagram("IoT Gateway Architecture", show=False, direction="TB"):
    sensors = IotSensor("Sensor Nodes")
    gateway = EC2("GatewayXM")
    iot_core = IotCore("IoT Core")
    kinesis = Kinesis("Kinesis Stream")
    sagemaker = Sagemaker("SageMaker")
    rds = RDS("RDS")
    s3 = S3("S3")
    cloudfront = CloudFront("CloudFront")
    iam = IAM("IAM")
    cloudwatch = Cloudwatch("CloudWatch")

    sensors >> gateway
    gateway >> iot_core
    iot_core >> kinesis
    kinesis >> sagemaker
    sagemaker >> rds
    sagemaker >> s3
    s3 >> cloudfront
    iam - gateway
    cloudwatch - gateway