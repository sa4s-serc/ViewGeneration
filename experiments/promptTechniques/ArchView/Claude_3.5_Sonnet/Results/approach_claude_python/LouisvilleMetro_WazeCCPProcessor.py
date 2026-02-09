from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.database import Aurora
from diagrams.aws.integration import SQS, SNS
from diagrams.aws.network import APIGateway
from diagrams.aws.management import Cloudwatch

with Diagram("Waze CCP Data Processing Architecture", show=False):
    with Cluster("Data Collection"):
        s3_raw = S3("Raw Data Lake")
        download_lambda = Lambda("waze-data-download")
        api_gw = APIGateway("Waze CCP Feed")

    with Cluster("Processing Pipeline"):
        sqs = SQS("Processing Queue")
        sns = SNS("Notifications")
        process_lambda = Lambda("waze-data-process")
        alerts_lambda = Lambda("alerts-processing")
        jams_lambda = Lambda("jams-processing")
        irreg_lambda = Lambda("irregularities-processing")

    with Cluster("Storage & API"):
        db = Aurora("PostgreSQL DB")
        api_lambda = Lambda("waze-data-api")
        api_endpoint = APIGateway("API Endpoint")

    monitoring = Cloudwatch("Monitoring")

    # Data Collection Flow
    api_gw >> download_lambda >> s3_raw
    
    # Processing Flow
    s3_raw >> process_lambda >> sqs
    sqs >> [alerts_lambda, jams_lambda, irreg_lambda]
    [alerts_lambda, jams_lambda, irreg_lambda] >> db
    process_lambda >> sns
    
    # API Flow
    api_endpoint >> api_lambda >> db
    
    # Monitoring
    [download_lambda, process_lambda, alerts_lambda, jams_lambda, irreg_lambda, api_lambda] >> monitoring