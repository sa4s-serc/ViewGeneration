from diagrams import Diagram, Cluster
from diagrams.aws.compute import EKS, ECS, Lambda
from diagrams.aws.analytics import Kinesis
from diagrams.aws.database import Dynamodb
from diagrams.aws.storage import S3
from diagrams.aws.network import ELB
from diagrams.aws.ml import Sagemaker
from diagrams.aws.management import Cloudwatch
from diagrams.aws.integration import SQS
from diagrams.onprem.container import Docker
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.queue import Kafka
from diagrams.programming.language import Python
from diagrams.programming.framework import FastAPI

with Diagram("Benchmark AI System Architecture", show=False, direction="TB"):
    with Cluster("Client Layer"):
        client = Python("BAI Client")
        bai_bff = FastAPI("BFF Service")
    
    with Cluster("Event Bus"):
        kafka = Kafka("Kafka")
    
    with Cluster("Orchestration Layer"):
        with Cluster("Job Management"):
            executor = EKS("Executor")
            watcher = Cloudwatch("Watcher")
            sm_executor = Sagemaker("SageMaker Executor")
        
        with Cluster("Data Management"):
            fetcher_dispatcher = ECS("Fetcher Dispatcher")
            fetcher = Docker("Fetcher")
    
    with Cluster("Infrastructure"):
        with Cluster("AWS Resources"):
            s3 = S3("S3 Storage")
            dynamodb = Dynamodb("DynamoDB")
            eks = EKS("Kubernetes Cluster")
        
        with Cluster("Monitoring"):
            prometheus = Prometheus("Prometheus")
            grafana = Grafana("Grafana")
            cloudwatch = Cloudwatch("CloudWatch")
    
    with Cluster("Execution Engines"):
        kubernetes = EKS("Kubernetes Jobs")
        sagemaker = Sagemaker("SageMaker Jobs")
    
    with Cluster("Metrics Collection"):
        metrics_pusher = Docker("Metrics Pusher")
        metrics_extractor = Lambda("Metrics Extractor")
        client_lib = Python("Client Library")
    
    # Connections
    client >> bai_bff
    bai_bff >> kafka
    kafka >> executor
    kafka >> watcher
    kafka >> sm_executor
    kafka >> fetcher_dispatcher
    fetcher_dispatcher >> fetcher
    fetcher >> s3
    executor >> kubernetes
    sm_executor >> sagemaker
    kubernetes >> metrics_pusher
    sagemaker >> metrics_pusher
    metrics_pusher >> kafka
    kafka >> metrics_extractor
    metrics_extractor >> dynamodb
    client_lib >> metrics_pusher
    watcher >> kafka
    prometheus >> grafana
    cloudwatch >> grafana
    kubernetes >> prometheus
    sagemaker >> cloudwatch