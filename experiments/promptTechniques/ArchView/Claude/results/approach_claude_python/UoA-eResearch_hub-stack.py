from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda
from diagrams.aws.database import ElasticacheForRedis, DynamodbTable
from diagrams.aws.network import APIGateway
from diagrams.aws.security import Cognito
from diagrams.programming.framework import Angular
from diagrams.saas.cdn import Cloudflare
from diagrams.aws.storage import S3

with Diagram("ResearchHub Architecture", show=False, direction="TB"):
    
    with Cluster("Frontend"):
        web = Angular("ResearchHub Website")
        cdn = Cloudflare("CDN")

    with Cluster("Authentication"):
        auth = Cognito("Auth Service")

    with Cluster("Backend Services"):
        api = APIGateway("GraphQL API")
        search = Lambda("Search Proxy")
        gql = Lambda("cer-graphql")

    with Cluster("Storage"):
        content = S3("Content Storage")
        cache = ElasticacheForRedis("Cache")
        db = DynamodbTable("Database")

    # Frontend connections
    web >> cdn
    cdn >> api

    # Auth flow
    web >> auth
    auth >> api

    # Backend connections
    api >> gql
    api >> search
    gql >> content
    gql >> cache
    search >> db

    # Storage connections
    gql >> db