from diagrams import Diagram
from diagrams.aws.security import SecurityHub, IAM
from diagrams.aws.integration import StepFunctions, SQS, Eventbridge
from diagrams.aws.compute import Lambda
from diagrams.aws.management import SystemsManager, Cloudwatch
from diagrams.aws.storage import S3
from diagrams.aws.general import User
from diagrams.aws.mobile import APIGateway
from diagrams.aws.analytics import KinesisDataFirehose
from diagrams.aws.database import Dynamodb

with Diagram("Automated Security Response on AWS", show=False, direction="TB"):
    user = User("Security Analyst")
    security_hub = SecurityHub("Security Hub")
    api_gateway = APIGateway("Custom Actions")
    event_bridge = Eventbridge("EventBridge")
    sqs = SQS("SQS Queue")
    step_functions = StepFunctions("Orchestrator Step Function")
    ssm = SystemsManager("SSM Automation")
    lambda_func = Lambda("Remediation Lambda")
    cloudwatch = Cloudwatch("CloudWatch")
    iam = IAM("IAM Roles")
    s3 = S3("Playbooks")
    kinesis = KinesisDataFirehose("Metrics Stream")
    dynamodb = Dynamodb("Remediation Status")

    user >> security_hub
    user >> api_gateway
    security_hub >> event_bridge
    api_gateway >> event_bridge
    event_bridge >> sqs
    sqs >> step_functions
    step_functions >> ssm
    ssm >> lambda_func
    lambda_func >> security_hub
    lambda_func >> cloudwatch
    lambda_func >> kinesis
    lambda_func >> dynamodb
    iam - [lambda_func, ssm, step_functions]
    s3 - ssm