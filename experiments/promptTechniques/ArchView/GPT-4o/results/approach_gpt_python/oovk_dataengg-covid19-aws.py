from diagrams import Diagram, Cluster
from diagrams.aws.storage import S3
from diagrams.aws.analytics import Athena, Redshift
from diagrams.aws.management import Cloudwatch
from diagrams.aws.database import RDS
from diagrams.aws.general import User
from diagrams.aws.compute import Lambda

with Diagram("COVID-19 Data Engineering Architecture", show=False, direction="TB"):

    user = User("Data Analyst")

    with Cluster("AWS S3 Data Lake"):
        s3_raw = S3("Raw Data")
        s3_transformed = S3("Transformed Data")
        s3_csv = S3("CSV Files")

    with Cluster("Data Processing"):
        athena = Athena("AWS Athena")
        lambda_function = Lambda("AWS Lambda (Potential)")

    with Cluster("Data Warehouse"):
        redshift = Redshift("Amazon Redshift")

    user >> s3_raw
    s3_raw >> athena >> s3_transformed
    s3_transformed >> lambda_function
    lambda_function >> s3_csv
    s3_csv >> redshift

    with Cluster("Monitoring"):
        cloudwatch = Cloudwatch("Cloudwatch Monitoring")

    cloudwatch >> [athena, redshift]