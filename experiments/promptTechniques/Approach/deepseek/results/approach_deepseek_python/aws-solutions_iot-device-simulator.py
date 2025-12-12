from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.iot import IotCore, IotRule, IotAnalytics
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import StepFunctions
from diagrams.aws.network import APIGateway
from diagrams.aws.security import Cognito
from diagrams.aws.management import Cloudwatch

with Diagram("AWS IoT Device Simulator Architecture", show=False, direction="TB"):
    user = Cognito("User")
    api = APIGateway("API Gateway")
    
    with Cluster("Microservices"):
        device_mgmt = Lambda("Device Type Manager")
        sim_mgmt = Lambda("Simulation Manager")
        response_mgr = Lambda("Response Manager")
        
    with Cluster("Simulation Engine"):
        simulator = Lambda("Simulator")
        device_factory = Lambda("Device Factory")
        data_generators = Lambda("Data Generators")
        
    iot_core = IotCore("AWS IoT Core")
    iot_rule = IotRule("IoT Rules")
    step_functions = StepFunctions("Step Functions")
    
    analytics = IotAnalytics("IoT Analytics")
    s3 = S3("S3 Storage")
    dynamodb = Dynamodb("Device Config")
    cloudwatch = Cloudwatch("Monitoring")
    
    user >> api >> [device_mgmt, sim_mgmt]
    sim_mgmt >> step_functions
    step_functions >> simulator
    simulator >> device_factory
    device_factory >> data_generators
    data_generators >> iot_core
    iot_core >> iot_rule
    iot_rule >> [analytics, s3, dynamodb]
    [device_mgmt, sim_mgmt, simulator, iot_core] >> cloudwatch