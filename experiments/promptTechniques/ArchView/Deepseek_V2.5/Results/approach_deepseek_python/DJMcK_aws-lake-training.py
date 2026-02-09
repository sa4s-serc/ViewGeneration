from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.aws.analytics import EMR, Glue, Athena, KinesisDataStreams
from diagrams.aws.compute import Lambda
from diagrams.aws.integration import StepFunctions
from diagrams.aws.ml import Comprehend
from diagrams.aws.security import IAM
from diagrams.aws.management import Cloudformation

with Diagram("AWS Data Lake Architecture", show=False, direction="TB"):
    with Cluster("Data Ingestion"):
        s3_raw = S3("Raw Zone")
        s3_landing = S3("Landing Zone")
        s3_curated = S3("Curated Zone")
    
    with Cluster("Data Processing"):
        emr = EMR("EMR Spark")
        glue_crawler = Glue("Glue Crawler")
        athena = Athena("Athena")
    
    with Cluster("NLP Processing"):
        with Cluster("Serverless Workflow"):
            step_functions = StepFunctions("Step Functions")
            lambda_query = Lambda("query_athena")
            lambda_config = Lambda("configure_count")
            lambda_comprehend = Lambda("call_comprehend")
            lambda_iterator = Lambda("iterator")
        
        comprehend = Comprehend("Comprehend Medical")
    
    with Cluster("Deployment & Security"):
        iam = IAM("IAM Roles")
        cloudformation = Cloudformation("CloudFormation")
    
    s3_raw >> emr >> s3_landing
    s3_landing >> emr >> s3_curated
    s3_curated >> glue_crawler
    glue_crawler >> athena
    athena >> lambda_query
    lambda_query >> step_functions
    step_functions >> lambda_config
    step_functions >> lambda_comprehend
    step_functions >> lambda_iterator
    lambda_comprehend >> comprehend
    iam >> [emr, glue_crawler, lambda_query, lambda_config, lambda_comprehend, lambda_iterator]
    cloudformation >> [s3_raw, s3_landing, s3_curated, iam]