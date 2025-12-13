from diagrams import Diagram
from diagrams.aws.general import Client, User
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import CloudFront
from diagrams.aws.security import Cognito
from diagrams.aws.mobile import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Kinesis
from diagrams.aws.ml import Sagemaker

with Diagram("Web Application Architecture", show=False, direction="LR"):
    users = User("Users")
    cdn = CloudFront("CDN")
    client = Client("Web Client")
    
    with Diagram("Frontend Layer"):
        frontend = EC2("Web Server")
        static_assets = S3("Static Assets")
    
    with Diagram("Backend Layer"):
        api_gateway = APIGateway("API Gateway")
        auth = Cognito("Authentication")
        
        with Diagram("Application Services"):
            app_servers = [EC2("App Server 1"),
                          EC2("App Server 2"),
                          EC2("App Server 3")]
        
        with Diagram("Data Layer"):
            database = RDS("Database")
            analytics = Kinesis("Data Stream")
            ml_service = Sagemaker("ML Service")
    
    users >> cdn >> client
    client >> frontend
    frontend >> static_assets
    client >> api_gateway
    api_gateway >> auth
    api_gateway >> app_servers
    app_servers >> database
    app_servers >> analytics
    analytics >> ml_service