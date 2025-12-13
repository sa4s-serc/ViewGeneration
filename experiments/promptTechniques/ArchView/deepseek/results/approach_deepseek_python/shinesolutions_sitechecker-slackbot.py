from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.integration import SNS, SQS
from diagrams.saas.chat import Slack
from diagrams.aws.general import User

with Diagram("SiteChecker Slack Bot Architecture", show=False, direction="LR"):
    user = User("Slack User")
    slack = Slack("Slack")
    api_gateway = APIGateway("API Gateway")
    master_lambda = Lambda("Master Lambda")
    worker_lambda_us_east = Lambda("Worker Lambda\n(us-east-1)")
    worker_lambda_us_west = Lambda("Worker Lambda\n(us-west-2)")
    worker_lambda_eu_west = Lambda("Worker Lambda\n(eu-west-1)")

    user >> slack
    slack >> api_gateway
    api_gateway >> master_lambda
    master_lambda >> worker_lambda_us_east
    master_lambda >> worker_lambda_us_west
    master_lambda >> worker_lambda_eu_west
    worker_lambda_us_east >> master_lambda
    worker_lambda_us_west >> master_lambda
    worker_lambda_eu_west >> master_lambda
    master_lambda >> slack