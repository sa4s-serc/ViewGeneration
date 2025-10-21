from diagrams import Diagram, Cluster
from diagrams.aws.compute import EC2, Lambda
from diagrams.aws.database import RDS
from diagrams.aws.integration import SQS
from diagrams.aws.network import APIGateway, ELB
from diagrams.aws.storage import S3
from diagrams.onprem.client import User
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Github

with Diagram("ResearchHub Architecture", show=False):
    user = User("User")

    with Cluster("ResearchHub Platform"):
        with Cluster("Frontend"):
            frontend = EC2("ResearchHub Website")

        with Cluster("Backend"):
            api_gateway = APIGateway("API Gateway")
            graphql_api = EC2("GraphQL API")
            search_proxy = Lambda("Search Proxy")
            link_checker = Lambda("SubHub Link Checker")

        with Cluster("Infrastructure"):
            jenkins = Jenkins("Jenkins CI/CD")
            terraform = EC2("Terraform")
            s3_bucket = S3("S3 Bucket")
            elb = ELB("Load Balancer")
            database = RDS("Database")

    with Cluster("Contentful CMS"):
        contentful = EC2("Contentful")

    user >> frontend
    frontend >> api_gateway
    api_gateway >> graphql_api
    graphql_api >> contentful
    search_proxy >> RDS("Elasticsearch")
    link_checker >> contentful

    github = Github("GitHub")
    github >> jenkins
    jenkins >> terraform
    terraform >> elb
    terraform >> s3_bucket

    search_proxy >> SQS("Event Queue")
    api_gateway >> database
    frontend >> database