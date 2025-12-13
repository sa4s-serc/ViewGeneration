from diagrams import Diagram, Cluster
from diagrams.onprem.client import User
from diagrams.onprem.compute import Server
from diagrams.onprem.database import PostgreSQL, MongoDB
from diagrams.onprem.network import Nginx
from diagrams.onprem.container import Docker
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.monitoring import Grafana, Prometheus
from diagrams.onprem.logging import Loki
from diagrams.onprem.vcs import Git
from diagrams.onprem.iac import Terraform
from diagrams.onprem.workflow import Airflow

with Diagram("BTCPay Server Architecture", show=False, direction="TB"):
    user = User("User")
    
    with Cluster("Frontend Layer"):
        nginx = Nginx("Nginx")
        vuepress = Server("VuePress")
    
    with Cluster("Application Layer"):
        with Cluster("Core Services"):
            btcpayserver = Server("BTCPay Server")
            nbxplorer = Server("NBXplorer")
            bitcoin_core = Server("Bitcoin Core")
            lnd = Server("LND")
        
        with Cluster("Database Layer"):
            postgres = PostgreSQL("PostgreSQL")
            mongodb = MongoDB("MongoDB")
    
    with Cluster("Development & Operations"):
        with Cluster("CI/CD"):
            jenkins = Jenkins("Jenkins")
            git = Git("Git")
        
        with Cluster("Monitoring"):
            prometheus = Prometheus("Prometheus")
            grafana = Grafana("Grafana")
            loki = Loki("Loki")
        
        with Cluster("Infrastructure"):
            docker = Docker("Docker")
            terraform = Terraform("Terraform")
            airflow = Airflow("Airflow")
    
    user >> nginx >> vuepress
    vuepress >> btcpayserver
    btcpayserver >> nbxplorer
    nbxplorer >> bitcoin_core
    btcpayserver >> lnd
    btcpayserver >> postgres
    btcpayserver >> mongodb
    
    jenkins >> git
    jenkins >> docker
    terraform >> docker
    airflow >> btcpayserver
    
    prometheus >> btcpayserver
    prometheus >> grafana
    loki >> btcpayserver