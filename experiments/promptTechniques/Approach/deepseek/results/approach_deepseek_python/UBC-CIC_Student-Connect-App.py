from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb
from diagrams.aws.analytics import ElasticsearchService
from diagrams.aws.storage import S3
from diagrams.aws.security import Cognito
from diagrams.aws.integration import StepFunctions
from diagrams.aws.mobile import Amplify
from diagrams.aws.management import Cloudwatch
from diagrams.programming.framework import React
from diagrams.onprem.client import User
from diagrams.elastic.elasticsearch import Kibana

with Diagram("Content Aggregation Platform Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Frontend"):
        frontend = React("React PWA")
        amplify = Amplify("AWS Amplify")
    
    with Cluster("Authentication"):
        cognito = Cognito("AWS Cognito")
    
    with Cluster("Data Sources"):
        sources = [
            "UBCO Events",
            "News",
            "Blogs", 
            "Athletics News",
            "Clubs"
        ]
    
    with Cluster("Data Processing"):
        with Cluster("Data Aggregation"):
            get_events = Lambda("get_events_data")
            get_news = Lambda("get_news_data")
            get_blogs = Lambda("get_blogs_data")
            get_athletics = Lambda("get_athletics_data")
            get_clubs = Lambda("get_clubs_data")
        
        with Cluster("Data Synchronization"):
            stream_handler = Lambda("document_stream_handler")
            es_hasher = Lambda("es_hasher")
    
    with Cluster("Data Storage"):
        dynamodb = Dynamodb("DynamoDB")
        elasticsearch = ElasticsearchService("Elasticsearch")
        s3 = S3("Data Lake")
    
    with Cluster("API Layer"):
        graphql = Lambda("GraphQL API")
        get_es_docs = Lambda("get_es_documents")
    
    with Cluster("Orchestration"):
        step_functions = StepFunctions("Step Functions")
        cloudwatch = Cloudwatch("CloudWatch Events")
    
    with Cluster("Admin Console"):
        kibana = Kibana("Kibana")
    
    user >> frontend
    frontend >> amplify
    frontend >> cognito
    cognito >> frontend
    cloudwatch >> [get_events, get_news, get_blogs, get_athletics, get_clubs]
    [get_events, get_news, get_blogs, get_athletics, get_clubs] >> dynamodb
    dynamodb >> stream_handler >> elasticsearch
    dynamodb >> es_hasher >> elasticsearch
    dynamodb >> s3
    frontend >> graphql >> dynamodb
    frontend >> get_es_docs >> elasticsearch
    elasticsearch >> kibana