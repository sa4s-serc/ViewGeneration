from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import SNS, SQS, Eventbridge
from diagrams.aws.database import Dynamodb
from diagrams.onprem.ci import GithubActions

with Diagram("Castle Finance Vault Transaction Indexer", show=False):
    github = GithubActions("GitHub Actions")

    with Cluster("Castle Finance Vault Transaction Indexer"):
        sns = SNS("Transaction Hashes SNS")
        sqs = SQS("Transaction Hashes SQS")
        eventbridge = Eventbridge("EventBridge Scheduler")

        with Cluster("Lambda Functions"):
            index_transaction_ids = Lambda("Index Transaction IDs")
            download_raw_transaction = Lambda("Download Raw Transaction")
            normalize_raw_transaction = Lambda("Normalize Raw Transaction")

        with Cluster("DynamoDB Tables"):
            raw_transactions_db = Dynamodb("Raw Transactions")
            normalized_transactions_db = Dynamodb("Normalized Transactions")

    github >> Edge(label="CI/CD") >> index_transaction_ids
    index_transaction_ids >> Edge(label="Publish IDs") >> sns
    sns >> Edge(label="Fan-out") >> sqs
    sqs >> Edge(label="Consume") >> download_raw_transaction
    download_raw_transaction >> Edge(label="Store Raw Data") >> raw_transactions_db
    raw_transactions_db >> Edge(label="Stream Event") >> normalize_raw_transaction
    normalize_raw_transaction >> Edge(label="Store Normalized Data") >> normalized_transactions_db
    eventbridge >> Edge(label="Trigger") >> index_transaction_ids