from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.ml import Rekognition 
from diagrams.aws.iot import IotCore
from diagrams.aws.mobile import APIGateway
from diagrams.aws.security import IAM
from diagrams.aws.integration import SQS
from diagrams.programming.framework import React
from diagrams.aws.database import Database
from diagrams.aws.business import AlexaForBusiness

with Diagram("JavaWatch Architecture", show=False):
    with Cluster("Frontend"):
        web = React("Web Interface")

    with Cluster("AWS Services"):
        api = APIGateway("API Gateway")
        auth = IAM("Authentication")
        
        with Cluster("Image Processing"):
            bucket = S3("Image Storage")
            rekognition = Rekognition("Bean Detection")
            lambda_check = Lambda("checkImage.py")
        
        with Cluster("Order Management"):
            drs = AlexaForBusiness("DRS")
            dynamo = Database("Device Registry")
            queue = SQS("Order Queue")

        with Cluster("IoT"):
            iot = IotCore("IoT Core")

    # Flow
    web >> api >> auth
    api >> bucket
    bucket >> lambda_check >> rekognition
    lambda_check >> queue
    queue >> drs
    iot >> bucket
    dynamo - api