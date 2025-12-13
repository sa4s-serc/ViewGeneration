from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.iot import IotCore
from diagrams.aws.storage import S3
from diagrams.aws.database import DynamodbTable 
from diagrams.aws.integration import StepFunctions
from diagrams.aws.security import Cognito
from diagrams.aws.mobile import APIGateway

with Diagram("AWS IoT Device Simulator Architecture", show=False):
    with Cluster("Frontend"):
        api = APIGateway("API Gateway")
        auth = Cognito("Authentication")

    with Cluster("Backend Services"):
        device_type_mgr = Lambda("Device Type Manager") 
        sim_mgr = Lambda("Simulation Manager")
        response_mgr = Lambda("Response Manager")
        step = StepFunctions("Simulation Orchestrator")

    with Cluster("Simulator Engine"):
        sim_engine = Lambda("Simulator Engine")
        iot = IotCore("AWS IoT Core")

    with Cluster("Storage"):
        dynamo = DynamodbTable("DynamoDB")
        s3 = S3("S3 Assets")

    # Frontend connections
    api >> auth
    api >> device_type_mgr
    api >> sim_mgr 
    api >> response_mgr

    # Backend service connections
    device_type_mgr >> dynamo
    sim_mgr >> step
    step >> sim_engine
    sim_engine >> iot

    # Storage connections
    sim_engine >> dynamo
    device_type_mgr >> s3
    sim_mgr >> s3