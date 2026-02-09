from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import DynamoDB
from diagrams.aws.storage import S3
from diagrams.aws.integration import Appsync, StepFunctions
from diagrams.aws.security import IAM
from diagrams.aws.ml import Comprehend
from diagrams.aws.management import Cloudwatch
from diagrams.aws.network import APIGateway
from diagrams.aws.integration import SES

with Diagram("RSS Lambda Architecture", show=False, direction="TB"):
    with Cluster("Security"):
        iam = IAM("IAM Roles")

    with Cluster("Event Triggers"):
        events = Cloudwatch("CloudWatch Events")

    with Cluster("API Layer"):
        api = APIGateway("API Gateway")
        graphql = Appsync("AppSync API")

    with Cluster("Processing"):
        step = StepFunctions("Step Functions")
        crawl = Lambda("RSS Crawl")
        getfeed = Lambda("Get Feed")
        pagecount = Lambda("Page Count")
        comprehend_svc = Comprehend("Entity Recognition")

    with Cluster("Storage"):
        dynamo = DynamoDB("Blog Posts")
        s3 = S3("Public JSON")

    with Cluster("Notifications"):
        ses = SES("Email Notifications")

    # Flow
    events >> step
    step >> crawl >> getfeed
    getfeed >> comprehend_svc
    getfeed >> dynamo
    getfeed >> s3
    getfeed >> ses
    pagecount >> dynamo

    # API Access
    api >> graphql
    graphql >> dynamo

    # IAM connections
    iam - step
    iam - crawl 
    iam - getfeed
    iam - pagecount
    iam - comprehend_svc
    iam - dynamo
    iam - s3
    iam - ses