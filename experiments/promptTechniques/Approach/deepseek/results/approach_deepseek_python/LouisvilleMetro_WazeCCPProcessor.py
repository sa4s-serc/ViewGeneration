from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.database import Aurora
from diagrams.aws.network import APIGateway
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.database import RDS

with Diagram("LouisvilleMetro_WazeCCPProcessor Architecture", show=False, direction="TB"):
    external_waze = APIGateway("Waze CCP Data Feed")
    
    s3_bucket = S3("S3 Data Lake")
    
    download_lambda = Lambda("waze-data-download")
    
    process_lambda = Lambda("waze-data-process")
    
    alerts_lambda = Lambda("waze-data-alerts-processing")
    jams_lambda = Lambda("waze-data-jams-processing")
    irregularities_lambda = Lambda("waze-data-irregularities-processing")
    
    sqs_queue = SQS("SQS Queue")
    sns_topic = SNS("SNS Topic")
    
    db_initialize_lambda = Lambda("waze-db-initialize")
    aurora_db = Aurora("Aurora PostgreSQL")
    
    api_gateway = APIGateway("API Gateway")
    api_lambda = Lambda("waze-data-api")
    
    external_waze >> download_lambda >> s3_bucket
    s3_bucket >> process_lambda >> sqs_queue
    sqs_queue >> alerts_lambda
    sqs_queue >> jams_lambda
    sqs_queue >> irregularities_lambda
    alerts_lambda >> aurora_db
    jams_lambda >> aurora_db
    irregularities_lambda >> aurora_db
    db_initialize_lambda >> aurora_db
    aurora_db >> api_lambda
    api_lambda >> api_gateway
    process_lambda >> sns_topic
    download_lambda >> sns_topic