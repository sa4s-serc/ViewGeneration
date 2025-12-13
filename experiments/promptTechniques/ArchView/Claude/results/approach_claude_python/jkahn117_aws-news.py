from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Database, Elasticache
from diagrams.aws.storage import S3
from diagrams.aws.network import CloudFront, APIGateway
from diagrams.aws.integration import Eventbridge, Appsync
from diagrams.aws.analytics import KinesisDataFirehose
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import Cognito

with Diagram("AWS News Aggregator Architecture", show=False):
    with Cluster("Frontend"):
        cdn = CloudFront("CDN")
        auth = Cognito("Authentication")

    with Cluster("API Layer"):
        gql = Appsync("GraphQL API")
        api = APIGateway("REST API")

    with Cluster("Processing"):
        events = Eventbridge("Event Bus")
        ingest = Lambda("RSS Ingestion")
        process = Lambda("Image Processing")
        serve = Lambda("Content Service")

    with Cluster("Storage"):
        s3 = S3("Article Content")
        db = Database("Article Metadata")
        cache = Elasticache("Redis Cache")

    with Cluster("Analytics"):
        firehose = KinesisDataFirehose("Analytics Stream")
        monitor = Cloudwatch("Monitoring")

    # Frontend connections
    cdn >> gql
    auth >> gql

    # API connections
    gql >> serve
    api >> serve

    # Processing flow
    ingest >> events
    events >> process
    process >> s3
    process >> db

    # Storage access
    serve >> cache
    serve >> db
    serve >> s3

    # Analytics flow
    serve >> firehose
    firehose >> monitor