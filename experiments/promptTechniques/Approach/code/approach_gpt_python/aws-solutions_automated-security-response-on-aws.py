from diagrams import Diagram, Cluster
from diagrams.aws.network import APIGateway, Route53
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import Eventbridge, SNS
from diagrams.aws.management import Cloudwatch
from diagrams.aws.management import SystemsManagerParameterStore
from diagrams.aws.security import IAM, SecurityHub
from diagrams.aws.storage import S3
from diagrams.aws.devtools import Codebuild
from diagrams.aws.general import User

with Diagram("Automated Security Response on AWS", show=False):
    user = User("Admin/User")

    with Cluster("ASR Solution"):
        security_hub = SecurityHub("AWS Security Hub")
        event_bridge = Eventbridge("EventBridge")
        orchestrator = Lambda("Orchestrator (Step Function)")
        with Cluster("Playbooks"):
            lambda_functions = Lambda("Lambda Functions")
            runbooks = SystemsManagerParameterStore("SSM Runbooks")

        custom_actions = SNS("Custom Actions")
        cloudwatch_logs = Cloudwatch("CloudWatch Logs")
        cloudwatch_metrics = Cloudwatch("CloudWatch Metrics")
        s3_bucket = S3("S3 Buckets for Logs")
        iam_roles = IAM("IAM Roles & Policies")
        code_build = Codebuild("AWS CodeBuild")

        ticket_systems = [SNS("Jira"), SNS("ServiceNow")]

    user >> Route53("Route53") >> security_hub >> event_bridge
    event_bridge >> custom_actions >> orchestrator
    orchestrator >> runbooks
    orchestrator >> lambda_functions
    lambda_functions >> [cloudwatch_logs, cloudwatch_metrics, s3_bucket]
    lambda_functions >> ticket_systems
    lambda_functions >> iam_roles
    code_build >> runbooks