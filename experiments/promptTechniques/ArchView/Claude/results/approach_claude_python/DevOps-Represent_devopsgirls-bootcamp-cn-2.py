from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.aws.general import Client

with Diagram("Todo Application Architecture", show=False):
    client = Client("Web Client")
    
    with Cluster("AWS Cloud"):
        api = APIGateway("API Gateway")
        
        with Cluster("Backend Services"):
            lambda_fn = Lambda("Todo Lambda")
            db = Dynamodb("Todo Table")
        
        with Cluster("Frontend Hosting"):
            s3 = S3("Static Website")
    
    client >> s3
    client >> api >> lambda_fn >> db