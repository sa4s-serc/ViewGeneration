from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, ECS, Lambda
from diagrams.aws.integration import SQS, SNS, Eventbridge
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import WAF
from diagrams.aws.database import Dynamodb
from diagrams.aws.analytics import Kinesis
from diagrams.aws.security import SecretsManager
from diagrams.aws.management import Cloudtrail
from diagrams.aws.general import Client

with Diagram("Piattaforma Notifiche (PN) Architecture", show=False, direction="TB"):
    client = Client("User")

    with Cluster("API Layer"):
        api_gateway = APIGateway("API Gateway")
        waf = WAF("WAF")
        client >> waf >> api_gateway

    with Cluster("Microservices"):
        lambda_reverse_proxy = Lambda("Lambda Reverse Proxy")

        with Cluster("ECS Cluster"):
            ecs_service = ECS("Microservice")
            ecs_service - Lambda("aws-otel-collector")

        api_gateway >> lambda_reverse_proxy >> ecs_service

    with Cluster("Event-Driven Architecture"):
        eventbridge = Eventbridge("EventBridge")
        sqs_queue = SQS("SQS Queue")
        sns_topic = SNS("SNS Topic")
        lambda_function = Lambda("Lambda Function")

        eventbridge >> lambda_function
        lambda_function >> sns_topic
        sns_topic >> sqs_queue

    with Cluster("Data Management"):
        s3 = S3("S3 Bucket")
        dynamodb = Dynamodb("DynamoDB")
        kinesis = Kinesis("Kinesis Stream")
        secrets_manager = SecretsManager("Secrets Manager")

        s3 << kinesis
        dynamodb - s3
        secrets_manager >> lambda_function

    with Cluster("Monitoring and Alarms"):
        cloudwatch = Cloudwatch("CloudWatch")
        cloudtrail = Cloudtrail("CloudTrail")

        ecs_service >> cloudwatch
        lambda_function >> cloudwatch
        cloudtrail >> cloudwatch

    client << api_gateway
    api_gateway >> eventbridge