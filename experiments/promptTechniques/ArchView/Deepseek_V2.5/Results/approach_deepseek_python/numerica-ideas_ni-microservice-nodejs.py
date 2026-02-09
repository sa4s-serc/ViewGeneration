from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda, EC2
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SNS
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.ci import GitlabCI
from diagrams.aws.network import APIGateway
from diagrams.aws.security import Cognito
from diagrams.onprem.database import MongoDB
with Diagram("Article Management Microservice Architecture", show=False, direction="TB"):
    api_gateway = APIGateway("API Gateway")
    cognito = Cognito("JWT Authentication")
    with Cluster("Deployment Environments"):
        with Cluster("Server Deployment (EC2/VPS)"):
            server_app = EC2("NodeJS Server")
            redis_server = Redis("Redis")
        with Cluster("Lambda Deployment"):
            lambda_app = Lambda("NodeJS Lambda")
            sns = SNS("SNS")
    mongodb = MongoDB("MongoDB")
    gitlab_ci = GitlabCI("GitLab CI/CD")
    api_gateway >> cognito
    api_gateway >> server_app
    api_gateway >> lambda_app
    server_app >> redis_server
    server_app >> mongodb
    lambda_app >> sns
    lambda_app >> mongodb
    redis_server - server_app
    sns - lambda_app
    gitlab_ci >> server_app
    gitlab_ci >> lambda_app