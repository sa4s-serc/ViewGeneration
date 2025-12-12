from diagrams import Diagram
from diagrams.aws.security import Cognito
from diagrams.aws.mobile import APIGateway
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.network import CloudFront
from diagrams.aws.engagement import Pinpoint
from diagrams.aws.integration import SNS
from diagrams.generic.os import Android
from diagrams.generic.device import Mobile
from diagrams.onprem.client import User

with Diagram("Hypertrack Live Android App Architecture", show=False, direction="TB"):
    user = User("End User")
    android_app = Android("Android App")
    
    cognito = Cognito("AWS Cognito\nUser Authentication")
    api_gateway = APIGateway("API Gateway")
    
    backend = Lambda("Backend Module\nHyperTrack Trips API")
    dynamodb = Dynamodb("DynamoDB\nTrip & Place Data")
    
    s3 = S3("S3\nStatic Assets")
    cloudfront = CloudFront("CloudFront\nCDN")
    
    sns = SNS("SNS\nNotifications")
    pinpoint = Pinpoint("Pinpoint\nPush Notifications")
    
    user >> android_app
    android_app >> cognito
    android_app >> api_gateway
    api_gateway >> backend
    backend >> dynamodb
    backend >> sns
    sns >> pinpoint >> android_app
    
    android_app >> cloudfront
    cloudfront >> s3