from diagrams import Diagram, Cluster
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.queue import Kafka
from diagrams.onprem.database import PostgreSQL, Clickhouse
from diagrams.onprem.inmemory import Redis
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.onprem.storage import Ceph
from diagrams.programming.framework import FastAPI, Django
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.aws.security import Cognito
from diagrams.aws.cost import CostAndUsageReport
from diagrams.generic.network import Subnet

with Diagram("Streaming Service Microservices Architecture", show=False, direction="TB"):
    with Cluster("External Services"):
        stripe = CostAndUsageReport("Stripe")
        google_auth = Cognito("Google OAuth")
        client = Subnet("Client")

    with Cluster("Authentication Layer"):
        auth = FastAPI("movies_auth")

    with Cluster("API Gateway"):
        gateway = Nginx("API Gateway")

    with Cluster("Microservices"):
        with Cluster("Content Management"):
            admin = Django("movies_admin")
            streaming_admin = Django("movies_streaming_admin")

        with Cluster("Streaming Services"):
            async_api = FastAPI("movies_async_api")
            converter = FastAPI("movies_streaming_converter")
            etl = Airflow("movies_streaming_etl")

        with Cluster("User Generated Content"):
            ugc = FastAPI("movies_ugc")

        with Cluster("Billing"):
            billing = FastAPI("movies_billing")

    with Cluster("Data Layer"):
        with Cluster("Databases"):
            postgres = PostgreSQL("PostgreSQL")
            elastic = Elasticsearch("Elasticsearch")
            clickhouse = Clickhouse("ClickHouse")

        with Cluster("Caching"):
            redis = Redis("Redis")

        with Cluster("Message Queue"):
            kafka = Kafka("Kafka")

        with Cluster("Storage"):
            minio = Ceph("MinIO")

    with Cluster("Orchestration"):
        docker = Docker("Docker")

    client >> gateway
    gateway >> [auth, admin, streaming_admin, async_api, converter, ugc, billing]
    auth >> postgres
    admin >> postgres
    streaming_admin >> postgres
    async_api >> [elastic, redis]
    converter >> minio
    etl >> [minio, postgres]
    ugc >> [kafka, clickhouse]
    billing >> [stripe, postgres]
    kafka >> clickhouse
    google_auth >> auth
    stripe >> billing