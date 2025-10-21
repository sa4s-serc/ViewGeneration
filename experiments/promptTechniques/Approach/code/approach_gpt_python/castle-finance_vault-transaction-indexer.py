from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.management import Eventbridge
from diagrams.aws.general import Generic

with Diagram("Castle Finance Vault Transaction Indexer Architecture", show=False, direction="TB"):
    with Cluster("AWS Infrastructure"):
        cdk = Generic("AWS CDK")

        index_lambda = Lambda("Index Transaction IDs")
        download_lambda = Lambda("Download Raw Transaction")
        normalize_lambda = Lambda("Normalize Raw Transaction")

        raw_dynamodb = Dynamodb("Raw Transactions Table")
        norm_dynamodb = Dynamodb("Normalized Transactions Table")

        sns_topic = SNS("Transaction Hashes Topic")
        sqs_queue = SQS("Transaction Hashes Queue")

        eventbridge = Eventbridge("Schedule Event")

        eventbridge >> index_lambda
        index_lambda >> sns_topic
        sns_topic >> sqs_queue
        sqs_queue >> download_lambda
        download_lambda >> raw_dynamodb
        raw_dynamodb >> normalize_lambda
        normalize_lambda >> norm_dynamodb

        cdk >> index_lambda
        cdk >> download_lambda
        cdk >> normalize_lambda
        cdk >> raw_dynamodb
        cdk >> norm_dynamodb
        cdk >> sns_topic
        cdk >> sqs_queue
        cdk >> eventbridge