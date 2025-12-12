from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2
from diagrams.aws.mobile import Amplify
from diagrams.onprem.database import MongoDB
from diagrams.onprem.client import Users
from diagrams.programming.framework import React
from diagrams.programming.language import NodeJS
from diagrams.onprem.analytics import PowerBI
from diagrams.onprem.monitoring import Grafana
from diagrams.aws.network import CloudFront
from diagrams.aws.security import Cognito
from diagrams.aws.analytics import Kinesis
from diagrams.aws.database import Dynamodb

with Diagram("Stotra Stock Trading Simulator Architecture", show=False, direction="TB"):
    users = Users("Users")
    
    with Cluster("Frontend"):
        frontend = React("React App")
        amplify = Amplify("AWS Amplify")
        frontend >> amplify
    
    with Cluster("Backend"):
        with Cluster("API Layer"):
            api = NodeJS("Express API")
            auth = Cognito("JWT Auth")
            rate_limit = Kinesis("Rate Limiting")
        
        with Cluster("Data Layer"):
            db = MongoDB("MongoDB")
            cache = Dynamodb("Cache")
        
        with Cluster("External Services"):
            yahoo_finance = PowerBI("Yahoo Finance API")
            alpha_vantage = Grafana("Alpha Vantage API")
            news_api = CloudFront("News API")
        
        api >> auth
        api >> rate_limit
        api >> db
        api >> cache
        api >> yahoo_finance
        api >> alpha_vantage
        api >> news_api
    
    users >> frontend
    frontend >> api
    amplify >> api