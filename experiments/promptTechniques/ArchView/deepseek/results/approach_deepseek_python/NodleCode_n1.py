from diagrams import Diagram
from diagrams.aws.compute import EC2
from diagrams.aws.mobile import Mobile
from diagrams.aws.database import RDS
from diagrams.aws.network import InternetGateway
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudwatch
from diagrams.aws.integration import SNS
from diagrams.aws.storage import S3

with Diagram("Nodle Ecosystem Architecture", show=False, direction="TB"):
    internet = InternetGateway("Internet")
    
    with Diagram("Device Tier"):
        beacon = Mobile("iBeacon Device\n(Dialog DA14531)")
        mobile_app = Mobile("Nodle Mobile App")
    
    with Diagram("Application Tier"):
        cloud_backend = EC2("Nodle Cloud Backend")
        api_gateway = EC2("API Gateway")
        auth_service = IAM("Authentication Service")
    
    with Diagram("Data Tier"):
        database = RDS("Beacon Database")
        storage = S3("File Storage")
        monitoring = Cloudwatch("Monitoring")
        messaging = SNS("Notifications")
    
    # Connections
    beacon >> mobile_app
    mobile_app >> internet >> api_gateway
    api_gateway >> auth_service
    api_gateway >> cloud_backend
    cloud_backend >> database
    cloud_backend >> storage
    cloud_backend >> monitoring
    cloud_backend >> messaging