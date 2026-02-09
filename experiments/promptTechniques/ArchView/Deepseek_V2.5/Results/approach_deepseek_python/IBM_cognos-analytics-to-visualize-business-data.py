from diagrams import Diagram, Cluster
from diagrams.aws.analytics import Glue, Athena, Kinesis, Redshift, EMR
from diagrams.aws.database import RDS, Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.network import CloudFront
from diagrams.aws.ml import Sagemaker
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import IAM
from diagrams.aws.integration import SQS, SNS
from diagrams.onprem.client import User

with Diagram("Data Analytics Architecture", show=False, direction="LR"):
    user = User("End User")

    with Cluster("Data Ingestion"):
        kinesis = Kinesis("Kinesis Data Streams")
        sqs = SQS("SQS Queue")
        s3_ingest = S3("Raw Data S3")

    with Cluster("Data Processing"):
        with Cluster("Batch Processing"):
            glue = Glue("AWS Glue")
            emr = EMR("EMR Cluster")
        
        with Cluster("Stream Processing"):
            lambda_stream = Lambda("Stream Lambda")
        
        with Cluster("ML Processing"):
            sagemaker = Sagemaker("SageMaker")

    with Cluster("Data Storage"):
        with Cluster("Structured Data"):
            rds = RDS("RDS")
            redshift = Redshift("Redshift")
        
        with Cluster("NoSQL Data"):
            dynamodb = Dynamodb("DynamoDB")
        
        with Cluster("Data Lake"):
            s3_data_lake = S3("Data Lake S3")

    with Cluster("Data Consumption"):
        athena = Athena("Athena")
        quicksight = User("QuickSight")

    with Cluster("Monitoring & Security"):
        cloudwatch = Cloudwatch("CloudWatch")
        iam = IAM("IAM")

    # Data flow
    user >> CloudFront("CloudFront") >> kinesis
    kinesis >> lambda_stream
    lambda_stream >> [s3_ingest, dynamodb]
    
    s3_ingest >> glue
    glue >> [rds, redshift, s3_data_lake]
    
    emr >> s3_data_lake
    s3_data_lake >> athena
    athena >> quicksight
    
    s3_data_lake >> sagemaker
    sagemaker >> SNS("SNS Notifications") >> user
    
    # Monitoring connections
    [kinesis, glue, emr, lambda_stream, sagemaker] >> cloudwatch
    [kinesis, glue, emr, lambda_stream, sagemaker] >> iam