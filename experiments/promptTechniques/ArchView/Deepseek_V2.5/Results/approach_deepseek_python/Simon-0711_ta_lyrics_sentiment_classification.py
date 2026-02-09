from diagrams import Diagram
from diagrams.onprem.client import User
from diagrams.programming.framework import React
from diagrams.programming.framework import FastAPI
from diagrams.elastic.elasticsearch import Elasticsearch
from diagrams.elastic.elasticsearch import Kibana
from diagrams.onprem.mlops import Mlflow
from diagrams.onprem.inmemory import Redis
from diagrams.onprem.container import Docker
from diagrams.onprem.network import Nginx
from diagrams.onprem.database import PostgreSQL
from diagrams.onprem.analytics import Spark
from diagrams.onprem.workflow import Airflow
from diagrams.onprem.monitoring import Grafana
from diagrams.onprem.monitoring import Prometheus
from diagrams.onprem.logging import Loki
from diagrams.onprem.ci import Jenkins
from diagrams.onprem.vcs import Git
from diagrams.onprem.iac import Terraform
from diagrams.onprem.compute import Server

with Diagram("Lyrics Sentiment Classification Architecture", show=False):
    user = User("User")
    
    with Diagram("Frontend Layer"):
        react_app = React("React Frontend")
    
    with Diagram("Backend Layer"):
        fastapi = FastAPI("FastAPI Backend")
        cnn_model = Mlflow("CNN Model")
        
    with Diagram("Data Layer"):
        elasticsearch = Elasticsearch("Elasticsearch")
        postgresql = PostgreSQL("PostgreSQL")
        redis = Redis("Redis Cache")
    
    with Diagram("External Services"):
        genius_api = Server("LyricsGenius API")
    
    with Diagram("Infrastructure"):
        docker = Docker("Docker")
        nginx = Nginx("Nginx")
        jenkins = Jenkins("Jenkins CI/CD")
        git = Git("Git")
        terraform = Terraform("Terraform")
    
    with Diagram("Monitoring"):
        grafana = Grafana("Grafana")
        prometheus = Prometheus("Prometheus")
        loki = Loki("Loki")
        kibana = Kibana("Kibana")
    
    with Diagram("Data Processing"):
        spark = Spark("Spark")
        airflow = Airflow("Airflow")
    
    # Define connections
    user >> react_app
    react_app >> fastapi
    fastapi >> cnn_model
    fastapi >> elasticsearch
    fastapi >> genius_api
    elasticsearch >> postgresql
    fastapi >> redis
    docker >> nginx
    jenkins >> git
    jenkins >> terraform
    prometheus >> grafana
    loki >> grafana
    spark >> airflow
    airflow >> elasticsearch