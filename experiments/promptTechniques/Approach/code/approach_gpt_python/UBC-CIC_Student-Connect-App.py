from diagrams import Diagram, Cluster, Edge
from diagrams.aws.compute import Lambda
from diagrams.aws.database import Dynamodb, Elasticache, S3
from diagrams.aws.network import CloudFront
from diagrams.aws.integration import SQS
from diagrams.aws.security import Cognito
from diagrams.onprem.client import Client
from diagrams.onprem.network import Nginx
from diagrams.onprem.iac import Ansible

with Diagram("Content Aggregation Platform Architecture", show=False, direction="TB"):
    client = Client("User")

    with Cluster("Frontend"):
        nginx = Nginx("Nginx")
        pwa = Client("React PWA")

    with Cluster("Backend"):
        with Cluster("Authentication"):
            cognito = Cognito("AWS Cognito")

        with Cluster("Data Processing"):
            with Cluster("Lambda Functions"):
                lambdas = [
                    Lambda("get_events_data"),
                    Lambda("get_news_data"),
                    Lambda("get_blogs_data"),
                    Lambda("get_athletics_news"),
                    Lambda("get_clubs_data"),
                    Lambda("document_stream_handler"),
                    Lambda("es_hasher"),
                    Lambda("get_es_documents")
                ]

            with Cluster("Data Storage"):
                dynamodb = Dynamodb("DynamoDB")
                elasticsearch = Elasticache("Elasticsearch")
                s3 = S3("S3 Data Lake")

            lambdas[0] >> Edge(label="store data") >> dynamodb
            lambdas[1] >> Edge(label="store data") >> dynamodb
            lambdas[2] >> Edge(label="store data") >> dynamodb
            lambdas[3] >> Edge(label="store data") >> dynamodb
            lambdas[4] >> Edge(label="store data") >> dynamodb

            dynamodb >> Edge(label="stream updates") >> lambdas[5]
            lambdas[5] >> Edge(label="update ES index") >> elasticsearch

            lambdas[6] >> Edge(label="sync data") >> elasticsearch
            lambdas[7] >> Edge(label="query documents") >> elasticsearch

        cloudfront = CloudFront("CloudFront")
        sqs = SQS("Data Queue")

    ansible = Ansible("Infrastructure as Code")

    client >> nginx >> pwa
    pwa >> cognito
    pwa >> cloudfront >> lambdas
    lambdas >> sqs
    dynamodb >> s3

    ansible >> Edge(label="deploys") >> [nginx, lambdas, dynamodb, elasticsearch, s3, cognito]