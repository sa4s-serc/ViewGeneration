from diagrams import Diagram, Cluster
from diagrams.aws.analytics import EMR, Glue, Athena
from diagrams.aws.compute import Lambda
from diagrams.aws.storage import S3
from diagrams.aws.ml import Comprehend
from diagrams.aws.integration import StepFunctions
from diagrams.aws.security import IAM

with Diagram("AWS Data Lake Architecture", show=False):
    with Cluster("Data Lake Zones"):
        raw = S3("Raw Zone")
        landing = S3("Landing Zone")
        curated = S3("Curated Zone")

    with Cluster("Data Processing"):
        emr = EMR("EMR Spark")
        glue = Glue("Glue Catalog")
        athena = Athena("Athena Queries")

    with Cluster("ML Processing"):
        comprehend = Comprehend("Comprehend Medical")
        step = StepFunctions("Step Functions")
        lambda_fn = Lambda("Lambda")

    iam = IAM("IAM Roles")

    # Data flow
    raw >> emr >> landing
    landing >> emr >> curated
    curated >> glue >> athena
    
    # ML flow
    curated >> lambda_fn >> comprehend
    lambda_fn >> step
    step >> lambda_fn
    
    # Security
    iam >> emr
    iam >> lambda_fn
    iam >> comprehend