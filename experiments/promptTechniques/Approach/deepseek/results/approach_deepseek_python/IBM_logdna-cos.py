from diagrams import Diagram
from diagrams.aws.storage import S3
from diagrams.aws.compute import Lambda
from diagrams.aws.analytics import KinesisDataFirehose
from diagrams.aws.database import Dynamodb
from diagrams.aws.network import CloudFront
from diagrams.aws.mobile import APIGateway
from diagrams.aws.integration import SQS
from diagrams.aws.database import RDS
from diagrams.aws.compute import EC2
from diagrams.aws.storage import EFS
from diagrams.aws.network import Route53
from diagrams.aws.security import WAF
from diagrams.aws.management import Cloudwatch

with Diagram("IBM CIS Logs to LogDNA Serverless Function Architecture", show=False, direction="LR"):
    dns = Route53("Route53")
    cdn = CloudFront("CloudFront")
    waf = WAF("WAF")
    
    cis_logs = S3("CIS Logs COS Bucket")
    
    serverless_function = Lambda("Serverless Function")
    
    logdna = KinesisDataFirehose("LogDNA")
    
    archive_bucket = S3("Archive COS Bucket")
    
    monitoring = Cloudwatch("CloudWatch")
    
    dns >> cdn
    cdn >> waf
    waf >> cis_logs
    cis_logs >> serverless_function
    serverless_function >> logdna
    serverless_function >> archive_bucket
    serverless_function >> monitoring