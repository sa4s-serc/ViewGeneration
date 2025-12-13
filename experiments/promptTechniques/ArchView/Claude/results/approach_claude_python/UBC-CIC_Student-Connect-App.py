from diagrams import Diagram, Cluster
from diagrams.aws.compute import Lambda 
from diagrams.aws.database import Database, ElasticacheCacheNode
from diagrams.aws.security import Cognito
from diagrams.aws.integration import Eventbridge
from diagrams.aws.storage import SimpleStorageServiceS3
from diagrams.aws.network import APIGateway 
from diagrams.aws.analytics import ElasticsearchService
from diagrams.firebase.develop import Authentication
from diagrams.programming.framework import React
from diagrams.aws.general import Users

with Diagram("UBCO Content Platform Architecture", show=False, direction="TB"):
    users = Users("End Users")
    
    with Cluster("Frontend"):
        frontend = React("ReactJS PWA")

    with Cluster("Authentication"):
        auth = Cognito("AWS Cognito")
        saml = Authentication("SAML Integration")
        
        auth - saml

    with Cluster("API Layer"):
        api = APIGateway("GraphQL API")
        events = Eventbridge("CloudWatch Events")

    with Cluster("Backend Services"):
        functions = [
            Lambda("Events Data"),
            Lambda("News Data"), 
            Lambda("Blogs Data"),
            Lambda("Athletics Data"),
            Lambda("Clubs Data")
        ]
        
        sync = Lambda("ES Hasher")
        stream = Lambda("Stream Handler")

    with Cluster("Data Storage"):
        dynamo = Database("DynamoDB")
        elastic = ElasticsearchService("Elasticsearch")
        cache = ElasticacheCacheNode("Redis Cache")
        datalake = SimpleStorageServiceS3("Data Lake")

    users >> frontend
    frontend >> auth
    frontend >> api
    
    api >> functions
    api >> dynamo
    
    events >> functions
    
    functions >> dynamo
    functions >> datalake
    
    dynamo >> stream
    stream >> elastic
    sync >> elastic
    
    elastic >> cache