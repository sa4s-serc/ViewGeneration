from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.integration import SNS, SQS
from diagrams.aws.database import DynamodbTable
from diagrams.aws.storage import S3
from diagrams.aws.iot import IotCore
from diagrams.aws.security import IAM

with Diagram("Matrix MALOS Z-Wave Architecture", show=False):
    with Cluster("MATRIX Core (MALOS)"):
        api = APIGateway("MALOS API")
        auth = IAM("Authentication")
        
        with Cluster("Z-Wave Control"):
            zwave = IotCore("Z-Wave Driver")
            queue = SQS("Command Queue")
            events = SNS("Event Bus")
        
        with Cluster("Storage Layer"):
            db = DynamodbTable("Device Registry")
            storage = S3("Command History")
    
    api >> auth
    api >> queue >> zwave
    zwave >> events
    zwave >> db
    events >> storage
    db >> storage