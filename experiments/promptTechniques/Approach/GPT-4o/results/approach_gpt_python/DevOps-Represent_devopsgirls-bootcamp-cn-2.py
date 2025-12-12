from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.programming.framework import React

with Diagram("Serverless Todo Application Architecture", show=False):
    frontend = React("React Frontend")
    
    with Cluster("AWS"):
        s3 = S3("Static Hosting")
        api_gateway = APIGateway("API Gateway")
        lambda_function = Lambda("Lambda Function")
        dynamodb = Dynamodb("DynamoDB")

    frontend >> s3
    s3 >> api_gateway
    api_gateway >> lambda_function
    lambda_function >> dynamodb