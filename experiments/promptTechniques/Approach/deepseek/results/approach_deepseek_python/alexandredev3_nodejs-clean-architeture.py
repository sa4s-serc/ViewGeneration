from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import Postgresql
from diagrams.onprem.inmemory import Redis
from diagrams.programming.language import TypeScript
from diagrams.onprem.container import Docker
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.monitoring import Prometheus, Grafana
from diagrams.aws.network import APIGateway

with Diagram("User Authentication and Management API Architecture", show=False):
    with Cluster("Client Layer"):
        client = User("Web Client")

    with Cluster("API Gateway"):
        api_gateway = APIGateway("Express API")

    with Cluster("Application Layer"):
        with Cluster("User Module"):
            user_service = TypeScript("User Service")
            auth_service = TypeScript("Auth Service")
            list_users_service = TypeScript("List Users Service")

    with Cluster("Data Layer"):
        with Cluster("Database"):
            postgres = Postgresql("PostgreSQL")
        with Cluster("Cache"):
            redis = Redis("Redis")

    with Cluster("Infrastructure"):
        with Cluster("Containerization"):
            docker = Docker("Docker")
        with Cluster("CI/CD"):
            jenkins = Jenkins("Jenkins")
        with Cluster("Monitoring"):
            prometheus = Prometheus("Prometheus")
            grafana = Grafana("Grafana")

    client >> api_gateway
    api_gateway >> user_service
    api_gateway >> auth_service
    api_gateway >> list_users_service
    user_service >> postgres
    auth_service >> postgres
    list_users_service >> postgres
    user_service >> redis
    auth_service >> redis
    list_users_service >> redis
    docker >> jenkins
    prometheus >> grafana