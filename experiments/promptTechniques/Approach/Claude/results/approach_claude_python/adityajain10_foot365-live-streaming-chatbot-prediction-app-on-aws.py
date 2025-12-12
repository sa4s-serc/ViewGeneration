from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Database, Elasticache
from diagrams.aws.network import APIGateway, CloudFront
from diagrams.aws.security import Cognito
from diagrams.aws.storage import S3
from diagrams.aws.ml import SagemakerModel
from diagrams.aws.integration import SNS, SQS
from diagrams.aws.analytics import ES

with Diagram("Foot365 Architecture", show=False):
    # Frontend/API Layer
    cf = CloudFront("CloudFront\nCDN")
    api = APIGateway("API Gateway")
    auth = Cognito("Authentication")

    # Static Content
    s3 = S3("Static Content")
    cf >> s3

    # API Gateway Flow
    cf >> api >> auth

    # Backend Services
    lambda_standings = Lambda("Standings")
    lambda_predictions = Lambda("Predictions")
    lambda_chat = Lambda("Chatbot")
    lambda_fixtures = Lambda("Fixtures")
    lambda_scores = Lambda("Live Scores")

    # Databases and Caches
    dynamo = Database("Match Data")
    elastic = ES("Match Search")
    redis = Elasticache("Score Cache")
    
    # ML Component
    ml = SagemakerModel("Prediction Model")

    # Message Services
    sqs = SQS("Message Queue")
    sns = SNS("Notifications")

    # Connect Components
    api >> [lambda_standings, lambda_predictions, lambda_chat, lambda_fixtures, lambda_scores]
    
    lambda_standings >> dynamo
    lambda_predictions >> ml
    lambda_chat >> [sqs, sns]
    lambda_fixtures >> elastic
    lambda_scores >> redis
    
    sqs >> lambda_chat
    ml >> dynamo