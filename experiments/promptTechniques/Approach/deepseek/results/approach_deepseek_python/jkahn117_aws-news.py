from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.network import CloudFront
from diagrams.aws.mobile import Amplify
from diagrams.aws.integration import Eventbridge, Appsync, StepFunctions
from diagrams.aws.analytics import KinesisDataFirehose
from diagrams.aws.engagement import Pinpoint
from diagrams.aws.database import Elasticache

with Diagram("AWS News Aggregator Architecture", show=False, direction="TB"):
    frontend = Amplify("Next.js Frontend")
    cdn = CloudFront("CloudFront CDN")
    
    with Cluster("Backend Services"):
        appsync = Appsync("GraphQL API")
        
        with Cluster("Ingestion Layer"):
            event_bus = Eventbridge("EventBridge")
            step_functions = StepFunctions("Step Functions")
            rss_parser = Lambda("RSS Parser")
            image_processor = Lambda("Image Processor")
            
        with Cluster("Services Layer"):
            content_service = Lambda("Content Service")
            cache = Elasticache("Redis Cache")
            
        with Cluster("Analytics Layer"):
            pinpoint = Pinpoint("User Analytics")
            firehose = KinesisDataFirehose("Kinesis Firehose")
            analytics_storage = S3("Analytics Data")
    
    storage = S3("Article Storage")
    metadata_db = Dynamodb("Article Metadata")
    
    frontend >> cdn >> appsync
    appsync >> content_service
    content_service >> cache
    content_service >> metadata_db
    
    rss_parser >> event_bus
    rss_parser >> storage
    rss_parser >> metadata_db
    event_bus >> image_processor
    image_processor >> storage
    image_processor >> metadata_db
    
    frontend >> pinpoint
    pinpoint >> firehose
    firehose >> analytics_storage