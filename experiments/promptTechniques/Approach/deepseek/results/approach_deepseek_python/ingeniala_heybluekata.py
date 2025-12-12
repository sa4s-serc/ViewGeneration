from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway, CloudFront
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.analytics import KinesisDataStreams, Athena
from diagrams.aws.security import Cognito
from diagrams.aws.integration import Eventbridge
from diagrams.aws.management import Cloudwatch
from diagrams.generic.device import Mobile, Tablet

with Diagram("HeyBlue Application Architecture", show=False, direction="TB"):
    mobile_client = Mobile("Mobile Client")
    web_client = Tablet("Web Client")
    
    with Cluster("Frontend Layer"):
        cdn = CloudFront("CDN")
        mobile_bff = Lambda("Mobile BFF")
        web_bff = Lambda("Web BFF")
    
    with Cluster("API Gateway"):
        api_gateway = APIGateway("API Gateway")
    
    with Cluster("Authentication"):
        cognito = Cognito("Cognito")
    
    with Cluster("Core Services"):
        user_mgmt = Lambda("User Management")
        interaction_service = Lambda("Interaction Service")
        gamification = Lambda("Gamification")
        commerce_service = Lambda("Commerce Service")
        content_mgmt = Lambda("Content Management")
    
    with Cluster("Data Layer"):
        with Cluster("Operational Data"):
            dynamodb = Dynamodb("DynamoDB")
        
        with Cluster("Analytics & Archive"):
            kinesis = KinesisDataStreams("Kinesis Streams")
            s3 = S3("Data Lake")
            athena = Athena("Athena")
    
    with Cluster("Event Processing"):
        event_bridge = Eventbridge("EventBridge")
        analytics_processor = Lambda("Analytics Processor")
        notification_service = Lambda("Notification Service")
    
    with Cluster("Monitoring"):
        cloudwatch = Cloudwatch("CloudWatch")
    
    mobile_client >> cdn >> mobile_bff >> api_gateway
    web_client >> cdn >> web_bff >> api_gateway
    
    api_gateway >> cognito
    api_gateway >> user_mgmt
    api_gateway >> interaction_service
    api_gateway >> gamification
    api_gateway >> commerce_service
    api_gateway >> content_mgmt
    
    user_mgmt >> dynamodb
    interaction_service >> dynamodb
    gamification >> dynamodb
    commerce_service >> dynamodb
    content_mgmt >> dynamodb
    
    user_mgmt >> event_bridge
    interaction_service >> event_bridge
    gamification >> event_bridge
    commerce_service >> event_bridge
    
    event_bridge >> analytics_processor
    event_bridge >> notification_service
    
    analytics_processor >> kinesis
    kinesis >> s3
    s3 >> athena
    
    notification_service >> mobile_client
    notification_service >> web_client
    
    user_mgmt >> cloudwatch
    interaction_service >> cloudwatch
    gamification >> cloudwatch
    commerce_service >> cloudwatch
    content_mgmt >> cloudwatch
    analytics_processor >> cloudwatch
    notification_service >> cloudwatch