from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.ml import Comprehend
from diagrams.aws.integration import SQS
from diagrams.aws.security import Cognito

with Diagram("Tengine Lite Architecture", show=False):
    with Cluster("User Authentication"):
        auth = Cognito("Authentication")

    with Cluster("API Layer"):
        api = APIGateway("API Gateway")
        
    with Cluster("Core Processing"):
        with Cluster("Model Management"):
            storage = S3("Model Storage")
            converter = Lambda("Model Converter")
        
        with Cluster("Inference Engine"):
            engine = Lambda("Inference Engine")
            operators = Lambda("Operator Library")
            
        with Cluster("Device Layer"):
            device = Lambda("Device Abstraction")
            
    with Cluster("Testing & Validation"):
        queue = SQS("Test Queue")
        validator = Lambda("Model Validator")
        analyzer = Comprehend("Performance Analysis")
        
    with Cluster("Data Storage"):
        db = RDS("Results DB")

    # Define relationships
    auth >> api
    api >> storage
    storage >> converter
    converter >> engine
    engine >> operators
    operators >> device
    device >> validator
    validator >> queue
    queue >> analyzer
    analyzer >> db