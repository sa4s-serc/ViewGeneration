from diagrams import Diagram
from diagrams.aws.general import User
from diagrams.aws.network import CloudFront
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.onprem.client import Client
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudwatch

with Diagram("Architectural View", show=False):
    user = User("End User")
    client = Client("Web Client")
    cdn = CloudFront("CDN")
    web_server = EC2("Web Server")
    app_server = EC2("Application Server")
    database = RDS("Database")
    storage = S3("File Storage")
    auth = IAM("Authentication")
    monitoring = Cloudwatch("Monitoring")

    user >> client >> cdn >> web_server >> app_server >> database
    web_server >> storage
    app_server >> auth
    web_server >> monitoring
    app_server >> monitoring