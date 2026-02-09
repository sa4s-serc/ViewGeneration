from diagrams import Cluster, Diagram, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import DynamodbTable
from diagrams.aws.integration import SNS, SQS, EventbridgeCustomEventBusResource
from diagrams.aws.general import Client

with Diagram("Castle Finance Vault Transaction Indexer", show=False):
    with Cluster("AWS Cloud"):
        # Core Components
        eventbridge = EventbridgeCustomEventBusResource("EventBridge\nScheduler")
        index_lambda = Lambda("Index Transaction IDs\nLambda")
        sns = SNS("Transaction\nSNS Topic")
        sqs = SQS("Download\nQueue")
        download_lambda = Lambda("Download Raw\nTransaction Lambda")
        raw_ddb = DynamodbTable("Raw Transactions\nDynamoDB")
        normalize_lambda = Lambda("Normalize\nTransaction Lambda") 
        normalized_ddb = DynamodbTable("Normalized\nTransactions DynamoDB")

        # Flow
        eventbridge >> index_lambda >> sns
        sns >> sqs >> download_lambda >> raw_ddb
        raw_ddb >> normalize_lambda >> normalized_ddb

        # External Components
        solscan = Client("Solscan API")
        download_lambda << Edge(color="darkgreen", style="dashed") << solscan