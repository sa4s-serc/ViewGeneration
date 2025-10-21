from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb, Elasticache, DynamodbTable
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.ml import Sagemaker
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.security import Cognito
from diagrams.aws.analytics import ElasticsearchService
from diagrams.aws.general import User
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.queue import Kafka
from diagrams.generic.database import SQL
from diagrams.onprem.client import User as OnPremUser
from diagrams.onprem.compute import Server
from diagrams.onprem.client import *

with Diagram("Foot365 Architecture", show=False, direction="TB"):
    user = OnPremUser("Football Enthusiast")

    with Cluster("Frontend"):
        ui = Client("User Interface (HTML/CSS/JS)")

    with Cluster("AWS Cloud"):
        cognito = Cognito("Cognito")
        api_gateway = APIGateway("API Gateway")

        with Cluster("Backend Microservices"):
            lambda_standings = Lambda("standings.py")
            lambda_predictions = Lambda("predictions.py")
            lambda_lf2 = Lambda("LF2.py")
            lambda_get_fixtures = Lambda("getFixtures.py")
            lambda_scrape_match_data = Lambda("scrapeMatchData.py")
            lambda_get_score = Lambda("getScore.py")
            lambda_lf1 = Lambda("LF1.py")
            lambda_get_live_scores = Lambda("getLiveScores.py")

        with Cluster("Data Storage & Processing"):
            s3 = S3("S3")
            dynamo_db = Dynamodb("DynamoDB")
            elastic_search = ElasticsearchService("ElasticSearch")
            sagemaker = Sagemaker("SageMaker")
            kafka = Kafka("Kafka")

        with Cluster("Communication & Notification"):
            sqs = SQS("SQS")
            sns = SNS("SNS")

    cloudwatch = Cloudwatch("CloudWatch")

    user >> ui
    ui >> api_gateway >> lambda_standings
    ui >> api_gateway >> lambda_predictions
    ui >> api_gateway >> lambda_lf2
    ui >> api_gateway >> lambda_get_fixtures
    ui >> api_gateway >> lambda_scrape_match_data
    ui >> api_gateway >> lambda_get_score
    ui >> api_gateway >> lambda_lf1
    ui >> api_gateway >> lambda_get_live_scores

    lambda_standings >> dynamo_db
    lambda_predictions >> sagemaker
    lambda_lf2 >> sqs >> sns
    lambda_get_fixtures >> elastic_search
    lambda_scrape_match_data >> s3 >> dynamo_db
    lambda_get_score >> elastic_search >> dynamo_db
    lambda_lf1 >> cognito
    lambda_get_live_scores >> dynamo_db

    kafka >> dynamo_db

    api_gateway >> cloudwatch