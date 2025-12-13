from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.programming.framework import React
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.container import Docker
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.logging import Loki
from diagrams.onprem.tracing import Jaeger
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Git
from diagrams.aws.storage import S3
from diagrams.aws.network import CloudFront
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.network import Route53

with Diagram("medlab_320-online-prototype Architecture", show=False, direction="TB"):
    user = User("End User")

    with Cluster("Frontend Layer"):
        cdn = CloudFront("CDN")
        react_app = React("React Application")
        with Cluster("React Features"):
            routing = React("React Router")
            forms = React("Ant Design Forms")
            state_management = React("Redux State")
            file_upload = React("File Upload")
        react_app >> routing
        react_app >> forms
        react_app >> state_management
        react_app >> file_upload

    with Cluster("Backend Layer"):
        with Cluster(".NET Core Services"):
            api_gateway = Nginx("API Gateway")
            with Cluster("Microservices"):
                auth_service = EC2("Auth Service")
                logging_service = EC2("Logging Service")
                file_service = EC2("File Service")
                business_service = EC2("Business Logic")

    with Cluster("Data Layer"):
        postgres = RDS("PostgreSQL")
        redis_cache = Redis("Redis Cache")
        minio = S3("MinIO Storage")

    with Cluster("Monitoring & Observability"):
        with Cluster("EFK Stack"):
            fluentd = Loki("Fluentd")
            elastic = Postgresql("Elasticsearch")
            kibana = Grafana("Kibana")
        tracing = Jaeger("Jaeger Tracing")

    with Cluster("CI/CD Pipeline"):
        jenkins = Jenkins("Jenkins")
        git_repo = Git("Git Repository")
        docker_registry = Docker("Docker Registry")

    user >> cdn >> react_app
    react_app >> api_gateway
    api_gateway >> auth_service
    api_gateway >> logging_service
    api_gateway >> file_service
    api_gateway >> business_service
    
    auth_service >> postgres
    business_service >> postgres
    business_service >> redis_cache
    file_service >> minio
    
    auth_service >> fluentd
    business_service >> fluentd
    file_service >> fluentd
    fluentd >> elastic >> kibana
    
    auth_service >> tracing
    business_service >> tracing
    
    git_repo >> jenkins
    jenkins >> docker_registry
    docker_registry >> api_gateway