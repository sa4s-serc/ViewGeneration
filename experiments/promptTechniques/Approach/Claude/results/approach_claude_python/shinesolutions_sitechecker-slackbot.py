from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.integration import SNS
from diagrams.aws.compute import ECS
from diagrams.aws.network import VPC
from diagrams.aws.network import CloudFront
from diagrams.saas.chat import Slack

with Diagram("SiteChecker Slack Bot Architecture", show=False):
    with Cluster("AWS Cloud"):
        with Cluster("VPC"):
            workers = [ECS("Worker 1"), 
                      ECS("Worker 2"),
                      ECS("Worker 3")]

        api = APIGateway("API Gateway")
        master = Lambda("Master Lambda")
        notification = SNS("SNS")
        cdn = CloudFront("CloudFront")

    slack = Slack("Slack")

    slack >> api >> master >> workers
    master >> notification >> slack
    cdn >> workers