from diagrams import Diagram, Cluster
from diagrams.aws.mobile import APIGateway
from diagrams.aws.compute import Lambda
from diagrams.aws.database import DynamodbTable
from diagrams.aws.storage import S3
from diagrams.programming.language import Python
from diagrams.azure.mobile import MobileEngagement
from diagrams.aws.iot import IotCore

with Diagram("NodleCode Architecture", show=False):
    with Cluster("Mobile & Firmware"):
        beacon = IotCore("iBeacon DA14531")
        mobile = MobileEngagement("Nodle Mobile App")

    with Cluster("Cloud Backend"):
        api = APIGateway("API Gateway")
        beacon_handler = Lambda("Beacon Handler")
        storage = DynamodbTable("Beacon Data Store")
        script = Python("getBeaconInformation.py")
        files = S3("Hardware Files")

    # Data flow
    beacon >> mobile >> api
    api >> beacon_handler >> storage
    storage >> script
    files >> beacon