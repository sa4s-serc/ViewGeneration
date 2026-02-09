from diagrams import Diagram, Cluster
from diagrams.aws.security import Cognito, IAM, Shield, Macie
from diagrams.aws.integration import SNS, SQS, Eventbridge 
from diagrams.aws.compute import Lambda
from diagrams.aws.database import DynamodbTable
from diagrams.aws.storage import S3
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import APIGateway
from diagrams.aws.devtools import Codebuild
from diagrams.saas.chat import Slack

with Diagram("Dow Jones Hammer Security Architecture", show=False):
    
    with Cluster("Security Checks & Monitoring"):
        security_checks = [
            Lambda("IAM Checker"),
            Lambda("S3 Checker"), 
            Lambda("RDS Checker"),
            Lambda("EC2 Checker")
        ]
        
        event_trigger = Eventbridge("Scheduler")
        monitoring = Cloudwatch("Monitoring")

    with Cluster("Core Services"):
        api = APIGateway("REST API")
        auth = Cognito("Authentication")
        access = IAM("Access Control")
        protection = Shield("Protection") 
        data_security = Macie("Data Security")

    with Cluster("Data Storage"):
        issues_db = DynamodbTable("Issues DB")
        config_store = S3("Config Store")
        
    with Cluster("Messaging & Notifications"):
        notification_bus = SNS("Notification Bus")
        message_queue = SQS("Message Queue")
        slack = Slack("Slack Alerts")

    with Cluster("Remediation"):
        remediation = [
            Lambda("Auto-Remediation"),
            Lambda("Manual-Remediation")
        ]
        build = Codebuild("Remediation Builder")

    # Connect components
    event_trigger >> security_checks
    security_checks >> issues_db
    security_checks >> notification_bus
    
    notification_bus >> message_queue
    message_queue >> slack
    
    api >> auth >> access
    
    remediation >> build
    remediation >> issues_db
    
    config_store >> security_checks
    monitoring >> security_checks