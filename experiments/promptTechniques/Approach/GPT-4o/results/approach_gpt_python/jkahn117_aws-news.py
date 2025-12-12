from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.network import CloudFront
from diagrams.aws.integration import Appsync
from diagrams.aws.analytics import KinesisDataFirehose
from diagrams.aws.engagement import Pinpoint
from diagrams.aws.network import APIGateway
from diagrams.aws.management import Cloudformation
from diagrams.aws.devtools import Codepipeline
from diagrams.aws.general import User
from diagrams.aws.database import Elasticache

with Diagram("AWS News Aggregator Architecture", show=False):
    user = User("User")

    with Cluster("Frontend"):
        cloudfront = CloudFront("CDN")
        app_frontend = Appsync("Next.js Frontend")
        user >> cloudfront >> app_frontend

    with Cluster("Backend"):
        with Cluster("Ingestion"):
            rss_lambda = Lambda("RSS Feed Parser")
            image_lambda = Lambda("Image Processor")
            ingestion_s3 = S3("Article Storage")
            ingestion_db = Dynamodb("Metadata Storage")
            rss_lambda >> Edge(label="Stores") >> ingestion_s3
            image_lambda >> Edge(label="Updates") >> ingestion_db

        with Cluster("Services"):
            api_gateway = APIGateway("API Gateway")
            appsync_api = Appsync("GraphQL API")
            cache = Elasticache("Redis Cache")
            api_gateway >> appsync_api
            appsync_api >> Edge(label="Caches") >> cache

        with Cluster("Analytics"):
            pinpoint = Pinpoint("User Interaction")
            firehose = KinesisDataFirehose("Data Firehose")
            pinpoint >> Edge(label="Streams Data") >> firehose

    with Cluster("Infrastructure Management"):
        cloudformation = Cloudformation("IaC")
        cicd = Codepipeline("CI/CD Pipeline")

    user >> cloudfront
    cloudfront >> api_gateway
    ingestion_s3 >> cloudfront
    ingestion_db >> cloudfront
    appsync_api >> cloudfront