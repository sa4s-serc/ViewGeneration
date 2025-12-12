from diagrams import Diagram
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.network import Nginx
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.logging import Loki
from diagrams.onprem.tracing import Jaeger
from diagrams.onprem.container import Docker
from diagrams.onprem.iac import Terraform
from diagrams.onprem.workflow import Airflow

with Diagram("Architectural View", show=False):
    nginx = Nginx("Nginx")
    app_server = Server("Application Server")
    database = PostgreSQL("Database")
    ci_cd = Jenkins("CI/CD")
    monitoring = Grafana("Monitoring")
    logging = Loki("Logging")
    tracing = Jaeger("Tracing")
    container = Docker("Container")
    iac = Terraform("Infrastructure as Code")
    workflow = Airflow("Workflow")

    nginx >> app_server >> database
    ci_cd >> container
    monitoring << app_server
    logging << app_server
    tracing << app_server
    iac >> container
    workflow >> app_server