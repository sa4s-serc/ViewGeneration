from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS
from diagrams.aws.analytics import KinesisDataStreams
from diagrams.aws.management import Cloudwatch
from diagrams.aws.mobile import APIGateway
from diagrams.aws.ml import Comprehend
from diagrams.aws.security import IAMRole
from diagrams.aws.network import APIGatewayEndpoint
from diagrams.aws.engagement import SES
from diagrams.onprem.client import User
from diagrams.onprem.monitoring import Grafana

with Diagram("AWS Serverless RSS Lambda", show=False, direction="TB"):
    user = User("User")
    grafana = Grafana("Monitoring")

    with Cluster("AWS Cloud"):
        cw_event = Cloudwatch("Event")
        ses_email = SES("Email Notification")
        
        with Cluster("Lambda Functions"):
            rss_crawl = Lambda("rsscrawl")
            rss_get_feed = Lambda("rssgetfeed")
            page_count = Lambda("pagecount")
        
        with Cluster("Storage"):
            dynamodb = Dynamodb("DynamoDB Table")
            s3_bucket = S3("S3 Bucket")
        
        with Cluster("APIs"):
            api_gateway = APIGateway("GraphQL API")
            api_gateway_endpoint = APIGatewayEndpoint("AppSync Endpoint")
        
        with Cluster("Machine Learning"):
            comprehend = Comprehend("Entity Recognition")
        
        with Cluster("IAM"):
            iam_role = IAMRole("IAM Roles")
        
        cw_event >> rss_crawl
        rss_crawl >> rss_get_feed
        rss_get_feed >> dynamodb
        rss_get_feed >> s3_bucket
        rss_get_feed >> comprehend
        rss_get_feed >> ses_email
        rss_get_feed >> api_gateway_endpoint
        api_gateway_endpoint >> api_gateway
        api_gateway >> user
        dynamodb >> page_count
        
        user >> grafana
        grafana >> rss_crawl
        grafana >> rss_get_feed
        grafana >> page_count