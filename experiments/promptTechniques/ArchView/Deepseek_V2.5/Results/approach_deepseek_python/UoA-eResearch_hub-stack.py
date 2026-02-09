from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.network import CloudFront, Route53
from diagrams.aws.database import Elasticache
from diagrams.aws.storage import S3
from diagrams.aws.security import Cognito
from diagrams.aws.management import Cloudwatch
from diagrams.onprem.client import User
from diagrams.programming.framework import Angular
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.iac import Terraform
from diagrams.generic.database import SQL

with Diagram("ResearchHub Architecture", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Frontend"):
        frontend = Angular("ResearchHub Website")
        cdn = CloudFront("CDN")
        s3 = S3("Static Assets")
    
    with Cluster("Backend Services"):
        with Cluster("API Layer"):
            graphql = EC2("GraphQL API")
        
        with Cluster("Search Service"):
            search_proxy = Lambda("Search Proxy")
            elasticsearch = Elasticache("ElasticSearch")
        
        with Cluster("Authentication"):
            cognito = Cognito("Cognito")
    
    with Cluster("Content Management"):
        contentful = SQL("Contentful CMS")
    
    with Cluster("Infrastructure"):
        with Cluster("CI/CD"):
            jenkins = Jenkins("Jenkins")
        
        with Cluster("Infrastructure as Code"):
            terraform = Terraform("Terraform")
        
        with Cluster("Monitoring"):
            cloudwatch = Cloudwatch("CloudWatch")
    
    dns = Route53("DNS")
    
    user >> cdn >> frontend
    frontend >> graphql
    graphql >> contentful
    frontend >> search_proxy
    search_proxy >> elasticsearch
    frontend >> cognito
    jenkins >> frontend
    jenkins >> graphql
    jenkins >> search_proxy
    terraform >> frontend
    terraform >> graphql
    terraform >> search_proxy
    cloudwatch >> frontend
    cloudwatch >> graphql
    cloudwatch >> search_proxy
    dns >> cdn
    dns >> graphql