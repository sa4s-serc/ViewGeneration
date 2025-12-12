from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.network import APIGateway
from diagrams.aws.database import Dynamodb
from diagrams.generic.device import Tablet

with Diagram("Serverless Todo Application Architecture", show=False, direction="LR"):
    user = Tablet("User")
    ui = S3("UI (React Frontend)")
    api = APIGateway("API Gateway")
    lambda_func = Lambda("Lambda Function")
    db = Dynamodb("DynamoDB")

    user >> ui
    user >> api
    api >> lambda_func
    lambda_func >> db