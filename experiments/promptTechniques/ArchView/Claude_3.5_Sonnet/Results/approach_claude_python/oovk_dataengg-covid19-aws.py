from diagrams import Diagram, Cluster
from diagrams.aws.analytics import Athena, Redshift
from diagrams.aws.storage import S3
from diagrams.aws.integration import Eventbridge
from diagrams.aws.management import Cloudwatch
from diagrams.aws.compute import Lambda
from diagrams.aws.database import DynamodbTable

with Diagram("COVID-19 Data Engineering Architecture", show=False):
    with Cluster("Data Sources"):
        source_data = S3("Raw Data Lake\nCOVID-19 Datasets")
    
    with Cluster("Data Processing"):
        athena = Athena("Data Extraction\nSQL Queries")
        lambda_transform = Lambda("Data Transformation\nPandas Processing")
        
    with Cluster("Data Storage"):
        s3_processed = S3("Processed Data\nCSV Files")
        redshift = Redshift("Data Warehouse\nDimensional Model")
        
    with Cluster("Monitoring & Orchestration"):
        eventbridge = Eventbridge("ETL Orchestration")
        cloudwatch = Cloudwatch("Monitoring & Logging")

    # Data flow
    source_data >> athena >> lambda_transform
    lambda_transform >> s3_processed >> redshift
    
    # Orchestration and monitoring
    eventbridge >> lambda_transform
    lambda_transform >> cloudwatch