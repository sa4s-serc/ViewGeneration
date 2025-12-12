from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS
from diagrams.aws.network import ELB
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Kinesis
from diagrams.aws.integration import SQS
from diagrams.aws.ml import Sagemaker
from diagrams.aws.security import IAM

with Diagram("Architectural View", show=False, direction="TB"):
    with Cluster("Frontend"):
        lb = ELB("Load Balancer")
        web_servers = [EC2("Web Server 1"), EC2("Web Server 2")]

    with Cluster("Backend"):
        with Cluster("Processing"):
            kinesis = Kinesis("Data Stream")
            sqs = SQS("Message Queue")
            lambda_func = Lambda("Processing Function")

        with Cluster("Machine Learning"):
            sagemaker = Sagemaker("ML Model")

        with Cluster("Storage"):
            s3 = S3("Object Storage")
            rds = RDS("Database")

    with Cluster("Security"):
        iam = IAM("IAM")

    lb >> web_servers
    web_servers >> kinesis
    kinesis >> sqs
    sqs >> lambda_func
    lambda_func >> sagemaker
    lambda_func >> s3
    lambda_func >> rds
    iam - web_servers
    iam - lambda_func
    iam - sagemaker
    iam - s3
    iam - rds