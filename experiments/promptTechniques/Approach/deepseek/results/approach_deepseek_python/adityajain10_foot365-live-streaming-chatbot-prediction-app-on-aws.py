from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.network import APIGateway
from diagrams.aws.storage import S3
from diagrams.aws.database import Dynamodb
from diagrams.aws.analytics import ElasticsearchService
from diagrams.aws.ml import Sagemaker, Lex
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.security import Cognito, IAM
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.queue import Kafka
from diagrams.onprem.compute import Server
from diagrams.generic.network import Subnet
from diagrams.generic.os import Android
from diagrams.programming.language import Javascript

with Diagram("Foot365 Architecture", show=False, direction="TB"):
    frontend = Javascript("Frontend\n(HTML/CSS/JS)")
    
    with Cluster("AWS Cloud"):
        api_gateway = APIGateway("API Gateway")
        cognito = Cognito("Cognito")
        
        with Cluster("Backend Services"):
            lambda_standings = Lambda("standings.py")
            lambda_predictions = Lambda("predictions.py")
            lambda_lf1 = Lambda("LF1.py")
            lambda_lf2 = Lambda("LF2.py")
            lambda_fixtures = Lambda("getFixtures.py")
            lambda_scores = Lambda("getScore.py\ngetLiveScores.py")
            lambda_scrape = Lambda("scrapeMatchData.py")
        
        with Cluster("Data Storage"):
            dynamodb = Dynamodb("DynamoDB")
            elasticsearch = ElasticsearchService("ElasticSearch")
            s3 = S3("S3")
        
        with Cluster("ML & AI"):
            sagemaker = Sagemaker("SageMaker")
            lex = Lex("Lex")
        
        with Cluster("Messaging"):
            sqs = SQS("SQS")
            sns = SNS("SNS")
        
        with Cluster("Kafka Infrastructure"):
            kafka_server = Server("EC2 Kafka")
            kafka_producer = Kafka("producer.js")
            kafka_consumer = Kafka("consumer.js")
        
        cloudwatch = Cloudwatch("CloudWatch")
        iam = IAM("IAM")

    frontend >> cognito
    frontend >> api_gateway
    
    api_gateway >> lambda_standings
    api_gateway >> lambda_predictions
    api_gateway >> lambda_lf1
    api_gateway >> lambda_lf2
    api_gateway >> lambda_fixtures
    api_gateway >> lambda_scores
    
    lambda_standings >> dynamodb
    lambda_predictions >> sagemaker
    lambda_lf1 >> lex
    lambda_lf1 >> elasticsearch
    lambda_lf2 >> sqs
    lambda_lf2 >> sns
    lambda_fixtures >> elasticsearch
    lambda_scores >> elasticsearch
    lambda_scores >> dynamodb
    lambda_scrape >> dynamodb
    
    s3 >> lambda_scrape
    
    kafka_producer >> kafka_server
    kafka_server >> kafka_consumer
    kafka_consumer >> dynamodb
    
    sqs >> lambda_lf2
    lex >> lambda_lf1
    
    [cognito, iam] >> api_gateway
    [lambda_standings, lambda_predictions, lambda_lf1, lambda_lf2, 
     lambda_fixtures, lambda_scores, lambda_scrape] >> cloudwatch