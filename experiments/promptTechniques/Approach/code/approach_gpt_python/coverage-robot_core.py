from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SQS, Eventbridge
from diagrams.aws.storage import S3
from diagrams.onprem.client import Users
from diagrams.onprem.vcs import Github

with Diagram("Coverage Robot System", show=False, direction="TB"):
    github = Github("GitHub")
    users = Users("DevOps")

    with Cluster("AWS"):
        with Cluster("Services"):
            api_service = Lambda("api")
            orchestrator_service = Lambda("orchestrator")
            analyse_service = Lambda("analyse")
            publish_service = Lambda("publish")

        with Cluster("Data Storage"):
            bigquery = Dynamodb("BigQuery")
            s3 = S3("Raw Coverage Data")
            dynamodb = Dynamodb("Config & Metadata")

        with Cluster("Event Processing"):
            eventbridge = Eventbridge("EventBridge")
            sqs = SQS("SQS")

        github >> api_service
        users >> api_service

        api_service >> s3
        api_service >> dynamodb

        api_service >> eventbridge
        eventbridge >> orchestrator_service
        orchestrator_service >> sqs
        sqs >> analyse_service
        analyse_service >> publish_service

        publish_service >> github

        api_service >> api_service # Webhook processing

    users >> github