from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.saas.chat import Slack

with Diagram("SiteChecker Slack Bot Architecture", show=False, direction="LR"):

    slack = Slack("Slack")
    
    with Cluster("AWS"):
        api_gateway = APIGateway("API Gateway")
        master_lambda = Lambda("Master Lambda Function")
        
        with Cluster("Worker Lambdas"):
            worker_lambdas = [Lambda("Worker Lambda Function 1"),
                              Lambda("Worker Lambda Function 2"),
                              Lambda("Worker Lambda Function 3")]
    
    slack >> api_gateway >> master_lambda
    master_lambda >> worker_lambdas
    worker_lambdas >> master_lambda
    master_lambda >> slack