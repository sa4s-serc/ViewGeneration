from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SNS
from diagrams.aws.database import Dynamodb
from diagrams.onprem.client import Client
from diagrams.onprem.compute import Server
from diagrams.onprem.database import Mongodb
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.network import Nginx

with Diagram("Article Management Microservice Architecture", show=False, direction="TB"):

    client = Client("User")

    with Cluster("Server Deployment"):
        server = Server("Express App")
        redis_server = Redis("Redis Pub/Sub")
        mongodb = Mongodb("MongoDB")

        client >> Edge(label="HTTP") >> Nginx("Load Balancer") >> server
        server >> Edge(label="CRUD API") >> mongodb
        server >> Edge(label="Cache-aside") >> redis_server

    with Cluster("AWS Lambda Deployment"):
        lambda_function = Lambda("Lambda Function")
        sns = SNS("AWS SNS")

        client >> Edge(label="HTTP") >> lambda_function
        lambda_function >> Edge(label="CRUD API") >> Dynamodb("DynamoDB")
        lambda_function >> Edge(label="Inter-Service") >> sns

    with Cluster("CI/CD Pipeline"):
        gitlab_ci = Client("GitLab CI")
        claudiajs = Client("ClaudiaJS")
        
        gitlab_ci >> Edge(label="Build & Deploy") >> claudiajs
        claudiajs >> Edge(label="Deploy Lambda") >> lambda_function

    server >> Edge(label="Inter-Service") >> redis_server
    lambda_function >> Edge(label="Inter-Service") >> sns