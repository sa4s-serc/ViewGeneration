from diagrams import Diagram
from diagrams.aws.analytics import Athena, Glue, Redshift
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.integration import SQS
from diagrams.aws.network import CloudFront
from diagrams.onprem.client import User

with Diagram("COVID-19 Data Engineering Architecture", show=False):
    user = User("Data Scientist")
    
    athena = Athena("AWS Athena")
    glue = Glue("AWS Glue")
    redshift = Redshift("Amazon Redshift")
    s3 = S3("S3 Data Lake")
    lambda_func = Lambda("ETL Processing")
    
    user >> athena
    athena >> s3
    glue >> s3
    s3 >> lambda_func
    lambda_func >> redshift