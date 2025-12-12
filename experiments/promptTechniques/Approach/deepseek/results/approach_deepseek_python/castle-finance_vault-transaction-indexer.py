from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SNS, SQS, Eventbridge
from diagrams.aws.network import CloudFront
from diagrams.aws.storage import S3
from diagrams.onprem.client import User

with Diagram("Castle Finance Vault Transaction Indexer Architecture", show=False, direction="LR"):
    user = User("User")
    
    solscan_api = CloudFront("Solscan API")
    
    index_lambda = Lambda("index-transaction-ids\nLambda")
    sns_topic = SNS("Transaction IDs\nSNS Topic")
    sqs_queue = SQS("Transaction Hashes\nSQS Queue")
    download_lambda = Lambda("download-raw-transaction\nLambda")
    raw_dynamodb = Dynamodb("Raw Transactions\nDynamoDB")
    normalize_lambda = Lambda("normalize-raw-transaction\nLambda")
    normalized_dynamodb = Dynamodb("Normalized Transactions\nDynamoDB")
    
    eventbridge = Eventbridge("EventBridge\n(Scheduler)")
    
    eventbridge >> index_lambda
    index_lambda >> sns_topic
    sns_topic >> sqs_queue
    sqs_queue >> download_lambda
    download_lambda >> raw_dynamodb
    raw_dynamodb >> normalize_lambda
    normalize_lambda >> normalized_dynamodb
    
    download_lambda - solscan_api