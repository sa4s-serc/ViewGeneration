from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.logging import Fluentbit
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.container import Docker
from diagrams.onprem.vcs import Git
from diagrams.onprem.iac import Terraform
from diagrams.programming.framework import Spring
from diagrams.programming.language import Java
from diagrams.programming.language import Python
from diagrams.aws.network import ELB
from diagrams.aws.security import IAM
from diagrams.aws.mobile import APIGateway
from diagrams.aws.integration import SQS
from diagrams.aws.compute import EC2
from diagrams.aws.database import RDS
from diagrams.aws.storage import S3

with Diagram("Microservices Architecture with Dapr", show=False, direction="TB"):
    user = User("End User")
    
    with Cluster("Frontend Layer"):
        cdn = Nginx("CDN")
        web_app = Spring("Blazor WebAssembly")
        
    with Cluster("API Gateway"):
        api_gateway = APIGateway("Kubernetes Ingress")
        
    with Cluster("Microservices Layer"):
        with Cluster("Identity Service"):
            identity_svc = Java("IdentityServer4")
            identity_db = PostgreSQL("Identity DB")
            
        with Cluster("Product Catalog Service"):
            product_svc = Java("ProductCatalogApi")
            product_db = PostgreSQL("Product DB")
            
        with Cluster("Inventory Service"):
            inventory_svc = Java("InventoryApi")
            inventory_db = PostgreSQL("Inventory DB")
            
        with Cluster("GraphQL Service"):
            graphql_svc = Python("GraphQL API")
            
    with Cluster("Dapr Components"):
        with Cluster("Service Mesh"):
            dapr_sidecar = EC2("Dapr Sidecar")
            
        with Cluster("Pub/Sub"):
            redis_pubsub = SQS("Redis Pub/Sub")
            
        with Cluster("State Management"):
            redis_state = RDS("Redis State")
            
    with Cluster("Infrastructure"):
        with Cluster("Monitoring"):
            grafana = Grafana("Grafana")
            fluentd = Fluentbit("Fluent Bit")
            zipkin = Airflow("Zipkin Tracing")
            
        with Cluster("CI/CD"):
            jenkins = Jenkins("GitHub Actions")
            git = Git("Git Repository")
            docker = Docker("Container Registry")
            
        with Cluster("Orchestration"):
            kubernetes = Terraform("Kubernetes")
            dapr_runtime = EC2("Dapr Runtime")
            
    # Connections
    user >> cdn >> web_app >> api_gateway
    
    api_gateway >> identity_svc
    api_gateway >> product_svc
    api_gateway >> inventory_svc
    api_gateway >> graphql_svc
    
    identity_svc >> identity_db
    product_svc >> product_db
    inventory_svc >> inventory_db
    
    # Dapr connections
    product_svc >> dapr_sidecar
    inventory_svc >> dapr_sidecar
    dapr_sidecar >> redis_pubsub
    dapr_sidecar >> redis_state
    
    # Event-driven communication
    product_svc >> redis_pubsub
    inventory_svc >> redis_pubsub
    
    # Monitoring connections
    product_svc >> fluentd
    inventory_svc >> fluentd
    identity_svc >> fluentd
    graphql_svc >> fluentd
    fluentd >> grafana
    dapr_sidecar >> zipkin
    
    # CI/CD connections
    git >> jenkins >> docker >> kubernetes
    kubernetes >> dapr_runtime