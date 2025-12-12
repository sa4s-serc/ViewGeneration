from diagrams import Diagram
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.integration import StepFunctions, Appsync
from diagrams.aws.ml import Comprehend
from diagrams.aws.engagement import SES
from diagrams.aws.network import CloudFront
from diagrams.aws.management import Cloudwatch
from diagrams.aws.security import KMS
from diagrams.onprem.client import User

with Diagram("RSS Lambda Architecture", show=False, direction="LR"):
    user = User("User")
    
    cloudwatch = Cloudwatch("CloudWatch Events")
    rss_crawl = Lambda("rsscrawl")
    step_function = StepFunctions("Step Function")
    rss_getfeed = Lambda("rssgetfeed")
    comprehend = Comprehend("Comprehend")
    dynamodb = Dynamodb("DynamoDB")
    s3 = S3("S3 Storage")
    appsync = Appsync("AppSync API")
    ses = SES("SES")
    pagecount = Lambda("pagecount")
    
    cloudwatch >> rss_crawl
    rss_crawl >> step_function
    step_function >> rss_getfeed
    rss_getfeed >> comprehend
    comprehend >> dynamodb
    dynamodb >> appsync
    dynamodb >> s3
    rss_getfeed >> ses
    user >> appsync
    user >> pagecount
    pagecount >> dynamodb