from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SQS
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.programming.language import TypeScript
from diagrams.programming.language import Nodejs
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Terraform
from diagrams.onprem.ci import Circleci
from diagrams.onprem.monitoring import Prometheus
from diagrams.generic.os import LinuxGeneral

with Diagram("Todo Management System - Hexagonal Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("External Systems"):
        localstack = Docker("Localstack")
        aws_cloud = LinuxGeneral("AWS Cloud")
        dynamodb = Dynamodb("DynamoDB")
        sqs_queue = SQS("SQS Queue")
    
    with Cluster("Core Business Logic"):
        business_logic = TypeScript("Business Logic\n(src/business/)")
    
    with Cluster("Adapters Layer"):
        adapters = Nodejs("Adapters\n(src/adapters/)")
    
    with Cluster("Ports Layer"):
        http_port = Nginx("HTTP Server\n(src/ports/http/)")
        lambda_port = Lambda("Lambda Handler\n(src/ports/aws-lambda/)")
        dynamo_port = Dynamodb("DynamoDB Repository\n(src/ports/aws-dynamo/)")
        sqs_port = SQS("SQS Handler\n(src/ports/aws-sqs/)")
        logger_port = Prometheus("Logger\n(src/ports/logger/)")
    
    with Cluster("Development & Deployment"):
        terraform = Terraform("Terraform\n(iaac/localstack/)")
        circleci = Circleci("CircleCI")
        serverless = Lambda("Serverless\nFramework")
    
    user >> http_port >> adapters >> business_logic
    lambda_port >> adapters >> business_logic
    business_logic >> adapters >> dynamo_port >> dynamodb
    business_logic >> adapters >> sqs_port >> sqs_queue
    business_logic >> adapters >> logger_port
    
    terraform >> localstack
    circleci >> serverless >> aws_cloud
    serverless >> lambda_port