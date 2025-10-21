from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.analytics import EMR, Glue, Athena
from diagrams.aws.ml import Comprehend
from diagrams.aws.management import Cloudformation
from diagrams.onprem.workflow import Airflow

with Diagram("AWS Data Lake Architecture", show=False, direction="TB"):

    with Cluster("Data Lake Zones"):
        raw_zone = S3("Raw Zone")
        landing_zone = S3("Landing Zone")
        curated_zone = S3("Curated Zone")

    with Cluster("ETL Pipeline"):
        emr = EMR("Spark on EMR")
        glue = Glue("AWS Glue")
        athena = Athena("AWS Athena")

    with Cluster("NLP Processing"):
        comprehend_medical = Comprehend("Comprehend Medical")
        lambda_configure_count = Lambda("Configure Count")
        lambda_call_comprehend = Lambda("Call Comprehend")
        lambda_query_athena = Lambda("Query Athena")
        lambda_iterator = Lambda("Iterator")

    with Cluster("Deployment Automation"):
        cloudformation = Cloudformation("CloudFormation")
        sam = Cloudformation("SAM")

    raw_zone >> emr >> landing_zone >> glue >> curated_zone
    curated_zone >> athena

    lambda_iterator >> lambda_query_athena >> lambda_call_comprehend
    lambda_call_comprehend >> comprehend_medical

    cloudformation >> [raw_zone, landing_zone, curated_zone]
    sam >> [lambda_configure_count, lambda_call_comprehend, lambda_query_athena, lambda_iterator]