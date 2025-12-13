from diagrams import Diagram, Cluster
from diagrams.aws.compute import ECS
from diagrams.aws.database import RDSPostgresqlInstance
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.aws.integration import SQS
from diagrams.aws.ml import Rekognition
from diagrams.aws.storage import S3
from diagrams.aws.network import APIGateway

with Diagram("Predictive Maintenance Architecture", show=False):
    with Cluster("Image Processing Pipeline"):
        lb = ELB("Load Balancer")
        api = APIGateway("API Gateway")
        
        with Cluster("Processing Services"):
            services = [
                ECS("Image Capture"),
                ECS("Image Predictor"),
                ECS("Model Server")
            ]
        
        queue = SQS("Message Queue")
        ml = Rekognition("ML Model")
        storage = S3("Object Storage")
        db = RDSPostgresqlInstance("Results DB")

    # Connect components
    lb >> api
    api >> services[0]
    services[0] >> queue
    queue >> services[1]
    services[1] << ml
    services[1] >> storage
    services[1] >> db
    services[2] >> ml