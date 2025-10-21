from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.iot import IotCore
from diagrams.aws.management import Cloudformation
from diagrams.aws.devtools import ToolsAndSdks
from diagrams.aws.analytics import KinesisDataStreams
from diagrams.aws.integration import StepFunctions
from diagrams.aws.storage import SimpleStorageServiceS3

with Diagram("AWS IoT Device Simulator Architecture", show=False):
    iot = IotCore("AWS IoT")

    with Cluster("Microservices Architecture"):
        lambda_microservices = Lambda("Microservices Lambda")
        lambda_simulator = Lambda("Simulator Lambda")

    with Cluster("Device Management"):
        device_type_manager = Lambda("Device Type Manager")
        simulation_manager = Lambda("Simulation Manager")
        response_manager = Lambda("Response Manager")

    lambda_microservices >> device_type_manager
    lambda_microservices >> simulation_manager
    lambda_microservices >> response_manager

    with Cluster("Simulator"):
        device_index = Lambda("Device Index")
        data_generators = [
            Lambda("Random Generator"),
            Lambda("Vehicle Generator")
        ]

    lambda_simulator >> device_index
    device_index >> data_generators

    with Cluster("Infrastructure"):
        cdk = ToolsAndSdks("AWS CDK")
        cloudformation = Cloudformation("CloudFormation")

    cdk >> cloudformation

    step_functions = StepFunctions("Event Orchestration")
    s3 = SimpleStorageServiceS3("S3 Asset Storage")

    iot >> lambda_microservices
    iot >> lambda_simulator
    iot >> step_functions
    step_functions >> lambda_simulator
    cloudformation >> s3