from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDSPostgresqlInstance
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.aws.integration import SNS
from diagrams.aws.security import Cognito
from diagrams.aws.mobile import APIGateway

with Diagram("GPSLogger Architecture", show=False):
    
    with Cluster("Frontend"):
        api = APIGateway("API Gateway")
        auth = Cognito("Authentication")

    with Cluster("Core Services"):
        gps_service = Lambda("GPS Logging Service")
        storage = RDSPostgresqlInstance("GPS Data Store")
        file_storage = S3("Log Files")
        notifications = SNS("Notifications")

    with Cluster("Load Balancing"):
        lb = ELB("Load Balancer")

    # Connect components
    api >> auth
    auth >> lb
    lb >> gps_service
    gps_service >> storage
    gps_service >> file_storage
    gps_service >> notifications