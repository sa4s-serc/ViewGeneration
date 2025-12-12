from diagrams import Diagram
from diagrams.programming.framework import React, NextJs
from diagrams.programming.language import TypeScript
from diagrams.onprem.client import User
from diagrams.aws.mobile import APIGateway
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.security import Cognito
from diagrams.aws.network import CloudFront

with Diagram("PyJailBreak Frontend Architecture", show=False, direction="LR"):
    user = User("User")
    cloudfront = CloudFront("CloudFront CDN")
    nextjs = NextJs("Next.js Frontend")
    react = React("React Components")
    redux = TypeScript("Redux Toolkit")
    api_gateway = APIGateway("Backend API")
    lambda_func = Lambda("Scan Execution")
    dynamodb = Dynamodb("Payload Storage")
    cognito = Cognito("Authentication")

    user >> cloudfront >> nextjs
    nextjs >> react
    react >> redux
    redux >> api_gateway
    api_gateway >> lambda_func
    lambda_func >> dynamodb
    cognito >> api_gateway