from diagrams import Diagram, Cluster
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.compute import Lambda
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3
from diagrams.aws.network import APIGateway

with Diagram("LouisvilleMetro Waze CCP Processor Architecture", show=False):
    with Cluster("Data Ingestion"):
        data_download = Lambda("waze-data-download")
        s3_datalake = S3("Data Lake")

    with Cluster("Data Processing"):
        process_controller = Lambda("waze-data-process")
        alerts_processing = Lambda("waze-data-alerts-processing")
        jams_processing = Lambda("waze-data-jams-processing")
        irregularities_processing = Lambda("waze-data-irregularities-processing")
        sqs_queue = SQS("Processing Queue")
        sns_notifications = SNS("Processing Notifications")

    with Cluster("Database Management"):
        aurora_db = RDS("Aurora PostgreSQL")
        db_initialize = Lambda("waze-db-initialize")

    with Cluster("API Access"):
        api_gateway = APIGateway("API Gateway")
        data_api = Lambda("waze-data-api")

    # Data Ingestion Flow
    data_download >> s3_datalake

    # Data Processing Flow
    s3_datalake >> process_controller
    process_controller >> sqs_queue
    sqs_queue >> alerts_processing
    sqs_queue >> jams_processing
    sqs_queue >> irregularities_processing
    process_controller >> sns_notifications

    # Database Management Flow
    alerts_processing >> aurora_db
    jams_processing >> aurora_db
    irregularities_processing >> aurora_db
    db_initialize >> aurora_db

    # API Access Flow
    aurora_db >> data_api
    data_api >> api_gateway